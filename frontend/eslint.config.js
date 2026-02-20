import js from '@eslint/js'
import globals from 'globals'
import reactHooks from 'eslint-plugin-react-hooks'
import reactRefresh from 'eslint-plugin-react-refresh'
import { defineConfig, globalIgnores } from 'eslint/config'

// defineConfig es la nueva forma de configurar ESLint (formato array)
export default defineConfig([
  // globalIgnores: archivos/carpetas que queremos que ESLint ignore completamente
  globalIgnores(['dist']),  // Ignoramos la carpeta de build

  // Configuración principal para archivos JS/JSX
  {
    files: ['**/*.{js,jsx}'],  // Aplica a todos los archivos .js y .jsx
    extends: [
      js.configs.recommended,           // Reglas recomendadas de JavaScript
      reactHooks.configs.flat.recommended,  // Reglas para React Hooks
      reactRefresh.configs.vite,         // Reglas para React Refresh (hot reload)
    ],
    languageOptions: {
      ecmaVersion: 2020,  // Usamos características de ECMAScript 2020
      globals: globals.browser,  // Define variables globales del navegador (window, document, etc.)
      parserOptions: {
        ecmaVersion: 'latest',  // Usar la última versión de ECMAScript
        ecmaFeatures: { jsx: true },  // Habilitar JSX
        sourceType: 'module',  // Usar módulos ES (import/export)
      },
    },
    rules: {
      // Personalización de reglas
      // 'no-unused-vars': error si hay variables sin usar
      // Pero ignoramos las que empiezan con mayúscula o guión bajo (convención para componentes)
      'no-unused-vars': ['error', { varsIgnorePattern: '^[A-Z_]' }],
    },
  },
])