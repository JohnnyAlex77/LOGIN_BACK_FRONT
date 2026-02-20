import { useContext } from 'react';
import { AuthContext } from '../contexts/AuthContext';

// Hook personalizado para usar el contexto de autenticación
// Lo creamos para no tener que estar importando useContext y AuthContext
// en todos los componentes que necesiten datos del usuario
export const useAuth = () => {
  // Obtenemos el valor actual del contexto
  const context = useContext(AuthContext);
  
  // Si no hay contexto, significa que estamos usando el hook fuera de un AuthProvider
  // Esto es un error común, así que lanzamos un mensaje claro
  if (!context) {
    throw new Error('useAuth debe usarse dentro de AuthProvider');
  }
  
  // Devolvemos el contexto (que contiene user, login, logout, etc.)
  return context;
};