import React from 'react'
import { useParams } from 'react-router-dom'
import { Factory, Activity, Settings, AlertTriangle } from 'lucide-react'

const EquipmentDetail = () => {
  const { id } = useParams<{ id: string }>()
  
  // Mock data
  const equipment = {
    id: id,
    name: 'Conveyor C-03',
    type: 'Belt Conveyor',
    zone: 'Zone 1 - Raw Material',
    status: 'operational',
    manufacturer: 'Siemens',
    model: 'SIMINE Conveyor',
    installDate: '2025-03-15',
    lastMaintenance: '2026-03-15',
    nextMaintenance: '2026-06-15',
    description: 'Conveyor utama untuk transport material ke EAF'
  }
  
  const sensorData = {
    vibration: { value: 4.2, unit: 'mm/s', status: 'normal' },
    temperature: { value: 68, unit: '°C', status: 'normal' },
    current: { value: 32.5, unit: 'A', status: 'normal' }
  }
  
  return (
    <div className="p-8">
      <header className="mb-8">
        <div className="flex items-center gap-3 mb-2">
          <Factory className="text-slate-400" size={32} />
          <h1 className="text-3xl font-bold text-white">{equipment.name}</h1>
        </div>
        <p className="text-slate-400">{equipment.zone}</p>
      </header>
      
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Info Card */}
        <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
          <h2 className="text-lg font-semibold text-white mb-4">Informasi Equipment</h2>
          
          <div className="space-y-3">
            <div className="flex justify-between">
              <span className="text-slate-400">ID</span>
              <span className="text-white">{equipment.id}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400">Tipe</span>
              <span className="text-white">{equipment.type}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400">Manufacturer</span>
              <span className="text-white">{equipment.manufacturer}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400">Model</span>
              <span className="text-white">{equipment.model}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400">Install Date</span>
              <span className="text-white">{equipment.installDate}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400">Last Maintenance</span>
              <span className="text-white">{equipment.lastMaintenance}</span>
            </div>
          </div>
        </div>
        
        {/* Sensor Data */}
        <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
          <h2 className="text-lg font-semibold text-white mb-4">Sensor Data Real-time</h2>
          
          <div className="space-y-4">
            {Object.entries(sensorData).map(([key, data]) => (
              <div key={key} className="flex items-center justify-between p-3 bg-slate-900 rounded-lg">
                <div className="flex items-center gap-3">
                  <Activity className="text-slate-400" size={20} />
                  <span className="text-slate-300 capitalize">{key}</span>
                </div>
                <div className="text-right">
                  <span className="text-white font-medium">{data.value}</span>
                  <span className="text-slate-400 text-sm ml-1">{data.unit}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
        
        {/* Actions */}
        <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
          <h2 className="text-lg font-semibold text-white mb-4">Aksi Cepat</h2>
          
          <div className="space-y-3">
            <button className="w-full flex items-center gap-3 p-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors">
              <Settings size={20} />
              <span>Schedule Maintenance</span>
            </button>
            
            <button className="w-full flex items-center gap-3 p-3 bg-slate-700 hover:bg-slate-600 text-white rounded-lg transition-colors">
              <Activity size={20} />
              <span>View History</span>
            </button>
            
            <button className="w-full flex items-center gap-3 p-3 bg-slate-700 hover:bg-slate-600 text-white rounded-lg transition-colors">
              <AlertTriangle size={20} />
              <span>Report Issue</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default EquipmentDetail
