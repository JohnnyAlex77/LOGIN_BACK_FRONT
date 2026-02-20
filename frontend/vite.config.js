import { defineConfig } from 'vite'  // Función helper de Vite para mejor autocompletado
import react from '@vitejs/plugin-react'  // Plugin para React (Fast Refresh, etc.)
import tailwindcss from '@tailwindcss/vite'  // Plugin para Tailwind CSS v4
import { fileURLToPath, URL } from 'node:url'  // Utilidades de Node para manejar rutas

export default defineConfig({
  // Plugins que Vite usa durante el desarrollo y build
  plugins: [
    react(),  // Habilita soporte para React y Fast Refresh
    tailwindcss(),  // Procesa Tailwind CSS (v4 ya no necesita archivo de config)
  ],
  
  // Configuración de resolución de módulos
  resolve: {
    alias: {
      // Definimos alias para importar módulos sin rutas relativas largas
      // Ejemplo: import api from '@/services/api' en lugar de '../../services/api'
      '@': fileURLToPath(new URL('./src', import.meta.url)),
      '@components': fileURLToPath(new URL('./src/components', import.meta.url)),
      '@pages': fileURLToPath(new URL('./src/pages', import.meta.url)),
      '@services': fileURLToPath(new URL('./src/services', import.meta.url)),
      '@contexts': fileURLToPath(new URL('./src/contexts', import.meta.url)),
      '@utils': fileURLToPath(new URL('./src/utils', import.meta.url)),
    }
  }
})