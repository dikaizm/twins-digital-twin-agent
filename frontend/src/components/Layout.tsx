import React from 'react'
import { Outlet, Link, useLocation } from 'react-router-dom'
import { 
  LayoutDashboard, 
  Settings, 
  AlertTriangle, 
  Upload,
  LogOut,
  Factory
} from 'lucide-react'

const Layout = () => {
  const location = useLocation()
  
  const navItems = [
    { path: '/', icon: LayoutDashboard, label: 'Dashboard' },
    { path: '/equipment', icon: Factory, label: 'Equipment' },
    { path: '/alerts', icon: AlertTriangle, label: 'Alerts' },
    { path: '/reconstruction', icon: Upload, label: '3D Upload' },
  ]
  
  return (
    <div className="flex h-screen bg-slate-900">
      {/* Sidebar */}
      <aside className="w-64 bg-slate-800 border-r border-slate-700">
        <div className="p-6">
          <h1 className="text-xl font-bold text-white">
            AI Twin Factory
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Hilirisasi Indonesia
          </p>
        </div>
        
        <nav className="px-4 py-4">
          {navItems.map((item) => {
            const Icon = item.icon
            const isActive = location.pathname === item.path
            
            return (
              <Link
                key={item.path}
                to={item.path}
                className={`flex items-center gap-3 px-4 py-3 rounded-lg mb-1 transition-colors ${
                  isActive 
                    ? 'bg-blue-600 text-white' 
                    : 'text-slate-300 hover:bg-slate-700'
                }`}
              >
                <Icon size={20} />
                <span>{item.label}</span>
              </Link>
            )
          })}
        </nav>
        
        <div className="absolute bottom-0 w-64 p-4 border-t border-slate-700">
          <button className="flex items-center gap-3 text-slate-400 hover:text-white transition-colors">
            <LogOut size={20} />
            <span>Logout</span>
          </button>
        </div>
      </aside>
      
      {/* Main Content */}
      <main className="flex-1 overflow-auto">
        <Outlet />
      </main>
    </div>
  )
}

export default Layout
