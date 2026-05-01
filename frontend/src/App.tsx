import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from 'react-query'
import { Toaster } from 'react-hot-toast'

import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import EquipmentList from './pages/EquipmentList'
import EquipmentDetail from './pages/EquipmentDetail'
import Alerts from './pages/Alerts'
import Reconstruction from './pages/Reconstruction'
import Login from './pages/Login'

import './index.css'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
})

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/" element={<Layout />}>
            <Route index element={<Dashboard />} />
            <Route path="equipment" element={<EquipmentList />} />
            <Route path="equipment/:id" element={<EquipmentDetail />} />
            <Route path="alerts" element={<Alerts />} />
            <Route path="reconstruction" element={<Reconstruction />} />
          </Route>
        </Routes>
      </Router>
      <Toaster position="top-right" />
    </QueryClientProvider>
  )
}

export default App
