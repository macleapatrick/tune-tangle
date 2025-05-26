import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'
import tsconfigPaths from "vite-tsconfig-paths"

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: { '@': path.resolve(__dirname, './src') },
  },
  server: {
    proxy: {
      // any request starting /search → http://localhost:8000
      '/search': {
        target: 'http://13.217.233.161:8000',
        changeOrigin: true,
        secure: false,
      },
    },
  },
})
