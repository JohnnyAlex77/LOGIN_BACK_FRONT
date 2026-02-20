import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './providers/AuthProviders'; // Provee el contexto de auth a toda la app
import ProtectedRoute from './utils/ProtectedRoute'; // Componente para proteger rutas según rol

// Importaciones de páginas
import Home from './pages/Home';
import About from './pages/About';
import Login from './pages/Login';
import AdminDashboard from './pages/admin/AdminDashboard';
import EstudianteDashboard from './pages/estudiante/EstudianteDashboard';
import EmpresaDashboard from './pages/empresa/EmpresaDashboard';

function App() {
  return (
    // AuthProvider envuelve todo para que cualquier componente hijo pueda usar useAuth()
    // Esto incluye el Router y todas las rutas
    <AuthProvider>
      {/* BrowserRouter habilita el enrutamiento en el navegador */}
      <BrowserRouter>
        {/* Routes define el conjunto de rutas (solo una se renderiza a la vez) */}
        <Routes>
          {/* Rutas públicas - accesibles sin autenticación */}
          <Route path="/" element={<Home />} />
          <Route path="/about" element={<About />} />
          <Route path="/login" element={<Login />} />

          {/* Rutas protegidas para Admin */}
          {/* ProtectedRoute verifica que el usuario tenga rol Admin */}
          <Route
            path="/dashboard/admin"
            element={
              <ProtectedRoute allowedRoles={['Admin']}>
                <AdminDashboard />
              </ProtectedRoute>
            }
          />

          {/* Ruta protegida para Estudiante - Notar que también permite Admin */}
          {/* Esto es útil para que el admin pueda previsualizar el dashboard de estudiante */}
          <Route
            path="/dashboard/estudiante"
            element={
              <ProtectedRoute allowedRoles={['Estudiante', 'Admin']}>
                <EstudianteDashboard />
              </ProtectedRoute>
            }
          />

          {/* Ruta protegida para Empresa - también permite Admin por la misma razón */}
          <Route
            path="/dashboard/empresa"
            element={
              <ProtectedRoute allowedRoles={['Empresa', 'Admin']}>
                <EmpresaDashboard />
              </ProtectedRoute>
            }
          />

          {/* Ruta comodín - cualquier URL no definida redirige al inicio */}
          {/* El 'replace' evita que la URL incorrecta quede en el historial */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;