import React from 'react'
import { Factory, ChevronRight, Activity } from 'lucide-react'
import { Link } from 'react-router-dom'

const EquipmentList = () => {
  // Mock equipment data
  const zones = [
    {
      name: 'Zone 1 - Raw Material',
      equipment: [
        { id: 'CONV-C01', name: 'Conveyor C-01', type: 'conveyor', status: 'operational' },
        { id: 'CONV-C02', name: 'Conveyor C-02', type: 'conveyor', status: 'operational' },
        { id: 'CONV-C03', name: 'Conveyor C-03', type: 'conveyor', status: 'warning' },
      ]
    },
    {
      name: 'Zone 2 - EAF',
      equipment: [
        { id: 'EAF-01', name: 'Electric Arc Furnace 01', type: 'furnace', status: 'operational' },
        { id: 'EAF-02', name: 'Electric Arc Furnace 02', type: 'furnace', status: 'operational' },
        { id: 'EAF-03', name: 'Electric Arc Furnace 03', type: 'furnace', status: 'maintenance' },
      ]
    },
  ]
  
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'operational': return 'bg-green-500'
      case 'warning': return 'bg-yellow-500'
      case 'maintenance': return 'bg-blue-500'
      default: return 'bg-gray-500'
    }
  }
  
  return (
    <div className="p-8">
      <header className="mb-8">
        <h1 className="text-3xl font-bold text-white">Equipment</h1>
        <p className="text-slate-400 mt-2">
          Kelola dan monitor semua equipment pabrik
        </p>
      </header>
      
      <div className="space-y-6">
        {zones.map((zone) => (
          <div key={zone.name} className="bg-slate-800 rounded-lg border border-slate-700">
            <div className="p-4 border-b border-slate-700">
              <h2 className="text-lg font-semibold text-white">{zone.name}</h2>
            </div>
            
            <div className="divide-y divide-slate-700">
              {zone.equipment.map((eq) => (
                <Link
                  key={eq.id}
                  to={`/equipment/${eq.id}`}
                  className="flex items-center justify-between p-4 hover:bg-slate-700/50 transition-colors"
                >
                  <div className="flex items-center gap-4">
                    <div className={`w-3 h-3 rounded-full ${getStatusColor(eq.status)}`} />
                    <Factory className="text-slate-400" size={24} />
                    <div>
                      <p className="text-white font-medium">{eq.name}</p>
                      <p className="text-slate-400 text-sm">{eq.id}</p>
                    </div>
                  </div>
                  
                  <div className="flex items-center gap-4">
                    <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                      eq.status === 'operational' ? 'bg-green-500/20 text-green-400' :
                      eq.status === 'warning' ? 'bg-yellow-500/20 text-yellow-400' :
                      'bg-blue-500/20 text-blue-400'
                    }`}>
                      {eq.status}
                    </span>
                    <ChevronRight className="text-slate-500" size={20} />
                  </div>
                </Link>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default EquipmentList
