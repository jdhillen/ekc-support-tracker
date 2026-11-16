import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// In local dev, Vite proxies /api to the FastAPI server (npm run dev:api).
// In production, Vercel serves both from the same origin, so no CORS is needed.
export default defineConfig({
  plugins: [vue()],
  server: {
    proxy: { '/api': 'http://localhost:8000' },
  },
})
