import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';

/**
 * Componente para proteger rutas basado en autenticación y roles
 * 
 * @param {Object} props
 * @param {ReactNode} props.children - Componente a renderizar si tiene acceso
 * @param {Array} props.allowedRoles - Roles permitidos (opcional)
 * @param {string} props.redirectTo - Ruta de redirección (default: '/login')
 */
const ProtectedRoute = ({ 
  children, 
  allowedRoles = [], 
  redirectTo = '/login' 
}) => {
  const { isAuthenticated, loading, hasAnyRole, userRole } = useAuth();

  // Mostrar nada mientras carga (o un spinner)
  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-blue-500 border-t-transparent rounded-full animate-spin mx-auto"></div>
          <p className="mt-4 text-gray-600">Cargando...</p>
        </div>
      </div>
    );
  }

  // Si no está autenticado, redirigir al login
  if (!isAuthenticated) {
    return <Navigate to={redirectTo} replace />;
  }

  // Si se especificaron roles y el usuario no tiene ninguno, redirigir
  if (allowedRoles.length > 0 && !hasAnyRole(allowedRoles)) {
    console.warn(
      `Acceso denegado: Usuario con rol "${userRole}" intentó acceder a ruta que requiere:`,
      allowedRoles
    );
    
    // Redirigir al dashboard que corresponde según su rol
    let dashboardRoute = '/';
    if (userRole === 'Admin') dashboardRoute = '/dashboard/admin';
    else if (userRole === 'Estudiante') dashboardRoute = '/dashboard/estudiante';
    else if (userRole === 'Empresa') dashboardRoute = '/dashboard/empresa';
    
    return <Navigate to={dashboardRoute} replace />;
  }

  // Todo bien, renderizar el componente
  return children;
};

export default ProtectedRoute;