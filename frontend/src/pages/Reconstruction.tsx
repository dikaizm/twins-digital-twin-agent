import React, { useCallback, useState } from 'react'
import { useDropzone } from 'react-dropzone'
import { Upload, Loader2, CheckCircle } from 'lucide-react'
import toast from 'react-hot-toast'

const Reconstruction = () => {
  const [uploading, setUploading] = useState(false)
  const [jobId, setJobId] = useState<string | null>(null)
  const [progress, setProgress] = useState(0)
  
  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    if (acceptedFiles.length === 0) return
    
    setUploading(true)
    setProgress(0)
    
    const formData = new FormData()
    acceptedFiles.forEach((file) => {
      formData.append('files', file)
    })
    formData.append('name', 'Pabrik Baja Zone 1')
    formData.append('zone', 'Zone 1')
    
    try {
      const response = await fetch('/api/v1/reconstruction/upload', {
        method: 'POST',
        body: formData,
      })
      
      if (response.ok) {
        const data = await response.json()
        setJobId(data.job_id)
        toast.success('Upload berhasil! 3D reconstruction dimulai.')
        
        // Simulate progress
        const interval = setInterval(() => {
          setProgress((prev) => {
            if (prev >= 100) {
              clearInterval(interval)
              return 100
            }
            return prev + 10
          })
        }, 1000)
      } else {
        toast.error('Upload gagal. Silakan coba lagi.')
      }
    } catch (error) {
      toast.error('Terjadi kesalahan. Silakan coba lagi.')
    } finally {
      setUploading(false)
    }
  }, [])
  
  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png']
    },
    multiple: true
  })
  
  return (
    <div className="p-8">
      <header className="mb-8">
        <h1 className="text-3xl font-bold text-white">3D Reconstruction</h1>
        <p className="text-slate-400 mt-2">
          Upload foto equipment untuk generate 3D digital twin
        </p>
      </header>
      
      <div className="max-w-2xl">
        {/* Upload Area */}
        <div
          {...getRootProps()}
          className={`border-2 border-dashed rounded-lg p-12 text-center cursor-pointer transition-colors ${
            isDragActive 
              ? 'border-blue-500 bg-blue-500/10' 
              : 'border-slate-600 hover:border-slate-500'
          }`}
        >
          <input {...getInputProps()} />
          
          {uploading ? (
            <div className="flex flex-col items-center">
              <Loader2 className="animate-spin text-blue-500 mb-4" size={48} />
              <p className="text-white font-medium">Mengupload...</p>
            </div>
          ) : (
            <div className="flex flex-col items-center">
              <Upload className="text-slate-400 mb-4" size={48} />
              <p className="text-white font-medium mb-2">
                {isDragActive ? 'Drop foto di sini' : 'Drag & drop foto atau klik untuk memilih'}
              </p>
              <p className="text-slate-400 text-sm">
                Support: JPG, PNG (Maks 100MB)
              </p>
            </div>
          )}
        </div>
        
        {/* Progress */}
        {jobId && (
          <div className="mt-8 bg-slate-800 rounded-lg p-6 border border-slate-700">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-3">
                {progress < 100 ? (
                  <Loader2 className="animate-spin text-blue-500" size={24} />
                ) : (
                  <CheckCircle className="text-green-500" size={24} />
                )}
                <div>
                  <p className="text-white font-medium">
                    {progress < 100 ? 'Processing...' : 'Selesai!'}
                  </p>
                  <p className="text-slate-400 text-sm">Job ID: {jobId}</p>
                </div>
              </div>
              <span className="text-white font-medium">{progress}%</span>
            </div>
            
            <div className="w-full bg-slate-700 rounded-full h-2">
              <div 
                className="bg-blue-500 h-2 rounded-full transition-all duration-500"
                style={{ width: `${progress}%` }}
              />
            </div>
          </div>
        )}
        
        {/* Instructions */}
        <div className="mt-8 bg-slate-800 rounded-lg p-6 border border-slate-700">
          <h3 className="text-white font-medium mb-4">Petunjuk Upload</h3>
          <ul className="space-y-2 text-slate-400 text-sm">
            <li>• Ambil foto dari berbagai angle (depan, samping, atas)</li>
            <li>• Pastikan pencahayaan cukup terang</li>
            <li>• Minimal 5-10 foto per equipment</li>
            <li>• Upload juga floor plan/layout jika ada</li>
          </ul>
        </div>
      </div>
    </div>
  )
}

export default Reconstruction
