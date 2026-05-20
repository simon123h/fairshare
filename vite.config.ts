import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  // For GitLab Pages deployment, set base to your repo name if needed:
  // base: '/fairshare/',
})
