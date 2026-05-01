import React from 'react'
import { 
  Activity, 
  AlertTriangle, 
  Settings, 
  CheckCircle,
  TrendingUp 
} from 'lucide-react'

const Dashboard = () => {
  // Mock data
  const stats = [
    { label: 'Equipment Online', value: '142/150', icon: CheckCircle, color: 'text-green-500' },
    { label: 'Active Alerts', value: '3', icon: AlertTriangle, color: 'text-red-500' },
    { label: 'OEE', value: '87%', icon: TrendingUp, color: 'text-blue-500' },
    { label: 'Maintenance Due', value: '5', icon: Settings, color: 'text-yellow-500' },
  ]
  
  const recentAlerts = [
    { id: 'ALT-001', equipment: 'CONV-C03', severity: 'HIGH', message: 'Vibration tinggi', time: '5 menit lalu' },
    { id: 'ALT-002', equipment: 'EAF-01', severity: 'MEDIUM', message: 'Temperature naik', time: '15 menit lalu' },
    { id: 'ALT-003', equipment: 'PUMP-P07', severity: 'LOW', message: 'Pressure drop', time: '1 jam lalu' },
  ]
  
  return (
    <div className="p-8">
      <header className="mb-8">
        <h1 className="text-3xl font-bold text-white">Dashboard</h1>
        <p className="text-slate-400 mt-2">
          Pabrik Baja Nirkarat - IMIP, Sulawesi Tengah
        </p>
      </header>
      
      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {stats.map((stat) => {
          const Icon = stat.icon
          return (
            <div key={stat.label} className="bg-slate-800 rounded-lg p-6 border border-slate-700">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-slate-400 text-sm">{stat.label}</p>
                  <p className="text-2xl font-bold text-white mt-1">{stat.value}</p>
                </div>
                <Icon className={stat.color} size={32} />
              </div>
            </div>
          )
        })}
      </div>
      
      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* 3D Preview Placeholder */}
        <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
          <h2 className="text-lg font-semibold text-white mb-4">Digital Twin Preview</h2>
          <div className="aspect-video bg-slate-900 rounded-lg flex items-center justify-center">
            <p className="text-slate-500">3D Scene Viewer</p>
          </div>
        </div>
        
        {/* Recent Alerts */}
        <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
          <h2 className="text-lg font-semibold text-white mb-4">Recent Alerts</h2>
          <div className="space-y-3">
            {recentAlerts.map((alert) => (
              <div 
                key={alert.id}
                className="flex items-center justify-between p-3 bg-slate-900 rounded-lg"
              >
                <div className="flex items-center gap-3">
                  <AlertTriangle 
                    size={20} 
                    className={
                      alert.severity === 'HIGH' ? 'text-red-500' :
                      alert.severity === 'MEDIUM' ? 'text-yellow-500' :
                      'text-blue-500'
                    } 
                  />
                  <div>
                    <p className="text-white font-medium">{alert.equipment}</p>
                    <p className="text-slate-400 text-sm">{alert.message}</p>
                  </div>
                </div>
                <span className="text-slate-500 text-sm">{alert.time}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}

export default Dashboard
