import React from 'react'
import { AlertTriangle, CheckCircle, Clock } from 'lucide-react'

const Alerts = () => {
  const alerts = [
    {
      id: 'ALT-001',
      equipment: 'CONV-C03',
      zone: 'Zone 1',
      severity: 'HIGH',
      title: 'Vibration Tinggi',
      description: 'Vibration RMS 12.5 mm/s (normal < 5 mm/s)',
      status: 'open',
      time: '5 menit lalu'
    },
    {
      id: 'ALT-002',
      equipment: 'EAF-01',
      zone: 'Zone 2',
      severity: 'MEDIUM',
      title: 'Temperature Naik',
      description: 'Motor temperature 85°C (normal < 75°C)',
      status: 'acknowledged',
      time: '15 menit lalu'
    },
    {
      id: 'ALT-003',
      equipment: 'PUMP-P07',
      zone: 'Zone 4',
      severity: 'LOW',
      title: 'Pressure Drop',
      description: 'Pressure 2.1 bar (normal 4.5 bar)',
      status: 'resolved',
      time: '1 jam lalu'
    },
  ]
  
  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'CRITICAL': return 'bg-red-500 text-red-400'
      case 'HIGH': return 'bg-orange-500 text-orange-400'
      case 'MEDIUM': return 'bg-yellow-500 text-yellow-400'
      default: return 'bg-blue-500 text-blue-400'
    }
  }
  
  return (
    <div className="p-8">
      <header className="mb-8">
        <h1 className="text-3xl font-bold text-white">Alerts</h1>
        <p className="text-slate-400 mt-2">
          Monitor dan kelola semua alert sistem
        </p>
      </header>
      
      <div className="space-y-4">
        {alerts.map((alert) => (
          <div 
            key={alert.id}
            className="bg-slate-800 rounded-lg p-6 border border-slate-700"
          >
            <div className="flex items-start justify-between">
              <div className="flex items-start gap-4">
                <div className={`w-12 h-12 rounded-lg ${getSeverityColor(alert.severity)} bg-opacity-20 flex items-center justify-center`}>
                  <AlertTriangle className={getSeverityColor(alert.severity).split(' ')[1]} size={24} />
                </div>
                
                <div>
                  <div className="flex items-center gap-3 mb-1">
                    <h3 className="text-white font-semibold">{alert.title}</h3>
                    <span className={`px-2 py-0.5 rounded text-xs font-medium ${getSeverityColor(alert.severity)} bg-opacity-20`}>
                      {alert.severity}
                    </span>
                  </div>
                  
                  <p className="text-slate-400 text-sm mb-2">{alert.description}</p>
                  
                  <div className="flex items-center gap-4 text-sm text-slate-500">
                    <span>{alert.equipment}</span>
                    <span>•</span>
                    <span>{alert.zone}</span>
                    <span>•</span>
                    <span>{alert.time}</span>
                  </div>
                </div>
              </div>
              
              <div className="flex items-center gap-2">
                {alert.status === 'open' && (
                  <button className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-sm transition-colors">
                    Acknowledge
                  </button>
                )}
                {alert.status === 'acknowledged' && (
                  <button className="px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg text-sm transition-colors">
                    Resolve
                  </button>
                )}
                {alert.status === 'resolved' && (
                  <span className="flex items-center gap-1 text-green-400 text-sm">
                    <CheckCircle size={16} />
                    Resolved
                  </span>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default Alerts
