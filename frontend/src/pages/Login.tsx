import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Factory, Lock, User } from 'lucide-react'
import toast from 'react-hot-toast'

const Login = () => {
  const navigate = useNavigate()
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    
    // Mock login
    setTimeout(() => {
      toast.success('Login berhasil!')
      navigate('/')
      setLoading(false)
    }, 1000)
  }
  
  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-900">
      <div className="w-full max-w-md">
        <div className="bg-slate-800 rounded-xl p-8 border border-slate-700 shadow-2xl">
          <div className="text-center mb-8">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-blue-600 rounded-xl mb-4">
              <Factory className="text-white" size={32} />
            </div>
            <h1 className="text-2xl font-bold text-white">AI Twin Factory</h1>
            <p className="text-slate-400 mt-2">Login untuk mengakses sistem</p>
          </div>
          
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="block text-slate-300 text-sm font-medium mb-2">
                Username
              </label>
              <div className="relative">
                <User className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-400" size={20} />
                <input
                  type="text"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  className="w-full bg-slate-900 border border-slate-600 rounded-lg py-3 pl-10 pr-4 text-white placeholder-slate-500 focus:outline-none focus:border-blue-500"
                  placeholder="Masukkan username"
                  required
                />
              </div>
            </div>
            
            <div>
              <label className="block text-slate-300 text-sm font-medium mb-2">
                Password
              </label>
              <div className="relative">
                <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-400" size={20} />
                <input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full bg-slate-900 border border-slate-600 rounded-lg py-3 pl-10 pr-4 text-white placeholder-slate-500 focus:outline-none focus:border-blue-500"
                  placeholder="Masukkan password"
                  required
                />
              </div>
            </div>
            
            <button
              type="submit"
              disabled={loading}
              className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-3 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Loading...' : 'Login'}
            </button>
          </form>
          
          <div className="mt-6 text-center">
            <p className="text-slate-500 text-sm">
              Demo credentials: operator / operator123
            </p>
          </div>
        </div>
        
        <p className="text-center text-slate-500 text-sm mt-8">
          © 2026 AI Twin Factory - Hilirisasi Indonesia
        </p>
      </div>
    </div>
  )
}

export default Login
