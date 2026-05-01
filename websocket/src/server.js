/**
 * AI Twin Factory - WebSocket Service
 * Real-time sensor data streaming
 */

const { Server } = require('socket.io');
const { createAdapter } = require('@socket.io/redis-adapter');
const Redis = require('ioredis');
const jwt = require('jsonwebtoken');
const winston = require('winston');
require('dotenv').config();

// Logger
const logger = winston.createLogger({
  level: 'info',
  format: winston.format.json(),
  transports: [
    new winston.transports.Console()
  ]
});

// Configuration
const PORT = process.env.PORT || 3000;
const REDIS_URL = process.env.REDIS_URL || 'redis://localhost:6379';
const JWT_SECRET = process.env.JWT_SECRET || 'your-secret-key';

// Redis clients
const pubClient = new Redis(REDIS_URL);
const subClient = pubClient.duplicate();

// Socket.IO server
const io = new Server({
  cors: {
    origin: ["http://localhost:5173", "http://localhost:3000"],
    methods: ["GET", "POST"],
    credentials: true
  }
});

// Use Redis adapter for scaling
io.adapter(createAdapter(pubClient, subClient));

// Authentication middleware
io.use(async (socket, next) => {
  try {
    const token = socket.handshake.auth.token;
    if (!token) {
      return next(new Error('Authentication required'));
    }
    
    const decoded = jwt.verify(token, JWT_SECRET);
    socket.userId = decoded.sub;
    socket.userRole = decoded.role || 'operator';
    next();
  } catch (err) {
    next(new Error('Invalid token'));
  }
});

// Connection handler
io.on('connection', (socket) => {
  logger.info(`Client connected: ${socket.id}, User: ${socket.userId}`);
  
  // Join equipment room
  socket.on('subscribe-equipment', (equipmentId) => {
    socket.join(`equipment:${equipmentId}`);
    logger.info(`User ${socket.userId} subscribed to ${equipmentId}`);
    
    // Send initial data
    socket.emit('subscribed', { equipmentId, status: 'success' });
  });
  
  // Join zone room
  socket.on('subscribe-zone', (zone) => {
    socket.join(`zone:${zone}`);
    logger.info(`User ${socket.userId} subscribed to zone ${zone}`);
    socket.emit('subscribed', { zone, status: 'success' });
  });
  
  // Unsubscribe
  socket.on('unsubscribe', (room) => {
    socket.leave(room);
    logger.info(`User ${socket.userId} unsubscribed from ${room}`);
  });
  
  // Disconnect
  socket.on('disconnect', () => {
    logger.info(`Client disconnected: ${socket.id}`);
  });
});

// Listen for sensor data from Redis
subClient.subscribe('sensor-data');
subClient.on('message', (channel, message) => {
  if (channel === 'sensor-data') {
    try {
      const data = JSON.parse(message);
      
      // Broadcast to equipment room
      io.to(`equipment:${data.equipmentId}`).emit('sensor-data', data);
      
      // Broadcast to zone room
      if (data.zone) {
        io.to(`zone:${data.zone}`).emit('zone-sensor-data', data);
      }
    } catch (err) {
      logger.error('Error parsing sensor data:', err);
    }
  }
});

// Listen for alerts from Redis
subClient.subscribe('alerts');
subClient.on('message', (channel, message) => {
  if (channel === 'alerts') {
    try {
      const alert = JSON.parse(message);
      
      // Broadcast alert to equipment room
      io.to(`equipment:${alert.equipmentId}`).emit('alert', alert);
      
      // Broadcast to zone
      if (alert.zone) {
        io.to(`zone:${alert.zone}`).emit('zone-alert', alert);
      }
      
      // Global broadcast for critical alerts
      if (alert.severity === 'CRITICAL') {
        io.emit('critical-alert', alert);
      }
    } catch (err) {
      logger.error('Error parsing alert:', err);
    }
  }
});

// Start server
io.listen(PORT);
logger.info(`WebSocket server running on port ${PORT}`);

// Health check endpoint (for load balancers)
const http = require('http');
const healthServer = http.createServer((req, res) => {
  if (req.url === '/health') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({
      status: 'healthy',
      service: 'websocket',
      connections: io.engine.clientsCount,
      uptime: process.uptime()
    }));
  } else {
    res.writeHead(404);
    res.end('Not found');
  }
});

healthServer.listen(3001, () => {
  logger.info('Health check server running on port 3001');
});
