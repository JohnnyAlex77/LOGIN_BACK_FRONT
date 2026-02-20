import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './providers/AuthProviders'
import ProtectedRoute from './utils/ProtectedRoute';

import Home from './pages/Home';
import About from './pages/About';
import Login from './pages/Login';
import AdminDashboard from './pages/admin/AdminDashboard';
import EstudianteDashboard from './pages/estudiante/EstudianteDashboard';
import EmpresaDashboard from './pages/empresa/EmpresaDashboard';

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/about" element={<About />} />
          <Route path="/login" element={<Login />} />

          <Route
            path="/dashboard/admin"
            element={
              <ProtectedRoute allowedRoles={['Admin']}>
                <AdminDashboard />
              </ProtectedRoute>
            }
          />

          <Route
            path="/dashboard/estudiante"
            element={
              <ProtectedRoute allowedRoles={['Estudiante', 'Admin']}>
                <EstudianteDashboard />
              </ProtectedRoute>
            }
          />

          <Route
            path="/dashboard/empresa"
            element={
              <ProtectedRoute allowedRoles={['Empresa', 'Admin']}>
                <EmpresaDashboard />
              </ProtectedRoute>
            }
          />

          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;