import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [react()],
    server: {
        port: 5173,
        proxy: {
            '/video_feed': {
                target: 'http://localhost:5005',
                changeOrigin: true
            },
            '/stats': {
                target: 'http://localhost:5005',
                changeOrigin: true
            },
            '/upload-image': {
                target: 'http://localhost:5005',
                changeOrigin: true
            },
            '/upload-video': {
                target: 'http://localhost:5005',
                changeOrigin: true
            },
            '/upload-multi': {
                target: 'http://localhost:5005',
                changeOrigin: true
            },
            '/results': {
                target: 'http://localhost:5005',
                changeOrigin: true
            },
            '/frames': {
                target: 'http://localhost:5005',
                changeOrigin: true
            }
        }
    }
})
