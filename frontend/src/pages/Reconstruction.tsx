import React, { useCallback, useState, useEffect, useRef } from 'react'
import { useDropzone } from 'react-dropzone'
import { Upload, Loader2, CheckCircle, Box, RotateCw, ZoomIn, ZoomOut, Move } from 'lucide-react'
import toast from 'react-hot-toast'
import * as THREE from 'three'

const RECONSTRUCTION_URL = '/models/manufacturing_layout.glb'
const LAYOUT_JSON_URL = '/models/manufacturing_layout.json'

interface LayoutObject {
  id: number
  name: string
  type: string
  center: number[]
  size: number[] | { radius: number; height: number }
  color: number[]
}

interface LayoutData {
  objects: LayoutObject[]
  metadata: {
    plant: string
    location: string
    capacity: string
    zones: string[]
  }
}

const ManufacturingViewer = () => {
  const containerRef = useRef<HTMLDivElement>(null)
  const sceneRef = useRef<{
    scene: THREE.Scene
    camera: THREE.PerspectiveCamera
    renderer: THREE.WebGLRenderer
    controls: any
    meshes: THREE.Mesh[]
  } | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!containerRef.current) return

    const container = containerRef.current
    const scene = new THREE.Scene()
    scene.background = new THREE.Color(0x1a1a2e)

    const camera = new THREE.PerspectiveCamera(
      60,
      container.clientWidth / container.clientHeight,
      0.1,
      1000
    )
    camera.position.set(30, 25, 30)
    camera.lookAt(0, 0, 0)

    const renderer = new THREE.WebGLRenderer({ antialias: true })
    renderer.setSize(container.clientWidth, container.clientHeight)
    renderer.setPixelRatio(window.devicePixelRatio)
    renderer.shadowMap.enabled = true
    container.appendChild(renderer.domElement)

    const ambientLight = new THREE.AmbientLight(0xffffff, 0.6)
    scene.add(ambientLight)

    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8)
    directionalLight.position.set(20, 30, 20)
    directionalLight.castShadow = true
    scene.add(directionalLight)

    const gridHelper = new THREE.GridHelper(100, 50, 0x444444, 0x222222)
    scene.add(gridHelper)

    const axesHelper = new THREE.AxesHelper(10)
    scene.add(axesHelper)

    const meshes: THREE.Mesh[] = []

    fetch(LAYOUT_JSON_URL)
      .then(res => res.json())
      .then((data: LayoutData) => {
        data.objects.forEach((obj) => {
          let geometry: THREE.BufferGeometry

          if (obj.type === 'box') {
            const [w, h, d] = obj.size as number[]
            geometry = new THREE.BoxGeometry(w, h, d)
          } else if (obj.type === 'cylinder') {
            const { radius, height } = obj.size as { radius: number; height: number }
            geometry = new THREE.CylinderGeometry(radius, radius, height, 24)
          } else if (obj.type === 'cone') {
            const { radius, height } = obj.size as { radius: number; height: number }
            geometry = new THREE.ConeGeometry(radius, height, 24)
          } else {
            geometry = new THREE.BoxGeometry(1, 1, 1)
          }

          const material = new THREE.MeshPhongMaterial({
            color: new THREE.Color(obj.color[0], obj.color[1], obj.color[2]),
            transparent: obj.color[3] < 1,
            opacity: obj.color[3],
          })

          const mesh = new THREE.Mesh(geometry, material)
          mesh.position.set(obj.center[0], obj.center[1], obj.center[2])
          mesh.castShadow = true
          mesh.receiveShadow = true
          mesh.userData = { name: obj.name, originalColor: obj.color }

          meshes.push(mesh)
          scene.add(mesh)
        })

        sceneRef.current = { scene, camera, renderer, controls: null, meshes }
        setLoading(false)
      })
      .catch(err => {
        console.error('Failed to load layout:', err)
        setError('Gagal memuat layout 3D')
        setLoading(false)
      })

    let animationId: number
    const animate = () => {
      animationId = requestAnimationFrame(animate)
      if (sceneRef.current) {
        sceneRef.current.renderer.render(scene, camera)
      }
    }
    animate()

    const handleResize = () => {
      if (!containerRef.current || !sceneRef.current) return
      const width = containerRef.current.clientWidth
      const height = containerRef.current.clientHeight
      sceneRef.current.camera.aspect = width / height
      sceneRef.current.camera.updateProjectionMatrix()
      sceneRef.current.renderer.setSize(width, height)
    }
    window.addEventListener('resize', handleResize)

    let isMouseDown = false
    let mouseX = 0, mouseY = 0
    let camAlpha = Math.PI / 4
    let camBeta = Math.PI / 4
    let camRadius = 50

    const updateCamera = () => {
      camera.position.x = camRadius * Math.sin(camBeta) * Math.cos(camAlpha)
      camera.position.y = camRadius * Math.cos(camBeta)
      camera.position.z = camRadius * Math.sin(camBeta) * Math.sin(camAlpha)
      camera.lookAt(0, 0, 0)
    }

    const onMouseDown = (e: MouseEvent) => {
      isMouseDown = true
      mouseX = e.clientX
      mouseY = e.clientY
    }

    const onMouseMove = (e: MouseEvent) => {
      if (!isMouseDown) return
      const deltaX = e.clientX - mouseX
      const deltaY = e.clientY - mouseY
      camAlpha -= deltaX * 0.01
      camBeta = Math.max(0.1, Math.min(Math.PI - 0.1, camBeta + deltaY * 0.01))
      mouseX = e.clientX
      mouseY = e.clientY
      updateCamera()
    }

    const onMouseUp = () => {
      isMouseDown = false
    }

    const onWheel = (e: WheelEvent) => {
      camRadius = Math.max(10, Math.min(200, camRadius + e.deltaY * 0.1))
      updateCamera()
    }

    container.addEventListener('mousedown', onMouseDown)
    container.addEventListener('mousemove', onMouseMove)
    container.addEventListener('mouseup', onMouseUp)
    container.addEventListener('mouseleave', onMouseUp)
    container.addEventListener('wheel', onWheel)

    return () => {
      cancelAnimationFrame(animationId)
      window.removeEventListener('resize', handleResize)
      container.removeEventListener('mousedown', onMouseDown)
      container.removeEventListener('mousemove', onMouseMove)
      container.removeEventListener('mouseup', onMouseUp)
      container.removeEventListener('mouseleave', onMouseUp)
      container.removeEventListener('wheel', onWheel)
      if (sceneRef.current?.renderer) {
        container.removeChild(sceneRef.current.renderer.domElement)
      }
    }
  }, [])

  return (
    <div className="bg-slate-900 rounded-lg overflow-hidden border border-slate-700">
      <div className="p-4 border-b border-slate-700 flex items-center justify-between">
        <div>
          <h3 className="text-white font-medium">Manufacturing Layout Preview</h3>
          <p className="text-slate-400 text-sm">Pabrik Baja Nirkarat - IMIP</p>
        </div>
        <div className="flex items-center gap-2 text-slate-400 text-sm">
          <Move size={14} />
          <span>Drag to rotate</span>
        </div>
      </div>
      <div ref={containerRef} className="h-96 bg-slate-950" />
      {loading && (
        <div className="absolute inset-0 flex items-center justify-center bg-slate-900/80">
          <Loader2 className="animate-spin text-blue-500" size={32} />
        </div>
      )}
      {error && (
        <div className="absolute inset-0 flex items-center justify-center bg-slate-900/80">
          <p className="text-red-400">{error}</p>
        </div>
      )}
    </div>
  )
}

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

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div>
          <ManufacturingViewer />

          <div className="mt-4 bg-slate-800 rounded-lg p-4 border border-slate-700">
            <h3 className="text-white font-medium mb-3">Equipment Zones</h3>
            <div className="grid grid-cols-2 gap-2 text-sm">
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded bg-red-800" />
                <span className="text-slate-300">EAF Furnaces</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded bg-amber-700" />
                <span className="text-slate-300">AOD Converter</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded bg-slate-500" />
                <span className="text-slate-300">Continuous Caster</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded bg-slate-600" />
                <span className="text-slate-300">Rolling Mill</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded bg-slate-400" />
                <span className="text-slate-300">Finishing</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded bg-slate-700" />
                <span className="text-slate-300">Control Room</span>
              </div>
            </div>
          </div>
        </div>

        <div>
          <div className="bg-slate-800 rounded-lg p-6 border border-slate-700 mb-6">
            <div {...getRootProps()} className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors ${isDragActive ? 'border-blue-500 bg-blue-500/10' : 'border-slate-600 hover:border-slate-500'}`}>
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
          </div>

          {jobId && (
            <div className="bg-slate-800 rounded-lg p-6 border border-slate-700 mb-6">
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

          <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
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
    </div>
  )
}

export default Reconstruction
