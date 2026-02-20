import React, { useState, useEffect } from 'react';
import { AuthContext } from '../contexts/AuthContext'; 
import authService from '../services/auth.service';
import { getAccessToken } from '../services/api';

export const AuthProvider = ({ children }) => {
  // Estado principal del usuario - null cuando no hay sesión
  const [user, setUser] = useState(null);
  // loading indica si estamos esperando respuestas del backend
  const [loading, setLoading] = useState(true);
  // error para mostrar mensajes cuando algo falla
  const [error, setError] = useState(null);

  /**
   * Iniciar sesión - conecta con el servicio de autenticación
   * Recibe usuario/email y contraseña, y si es exitoso guarda el usuario
   */
  const login = async (username_email, password) => {
    setLoading(true);
    setError(null);
    
    try {
      const result = await authService.login(username_email, password);
      
      if (result.success) {
        setUser(result.user);
        return { success: true, user: result.user };
      } else {
        setError(result.error);
        return { success: false, error: result.error };
      }
    } catch (err) {
      const errorMsg = err.message || 'Error inesperado';
      setError(errorMsg);
      return { success: false, error: errorMsg };
    } finally {
      setLoading(false);
    }
  };

  /**
   * Cerrar sesión - limpia el estado y llama al servicio
   * Notar que siempre limpiamos el usuario aunque falle el logout del backend
   */
  const logout = async () => {
    setLoading(true);
    
    try {
      await authService.logout();
      setUser(null);
    } catch (err) {
      console.error('Error en logout:', err);
      // Aunque falle, limpiamos al usuario localmente
      setUser(null);
    } finally {
      setLoading(false);
    }
  };

  /**
   * Verificar si hay sesión activa al cargar la app
   * Este useEffect se ejecuta una sola vez cuando el provider se monta
   */
  useEffect(() => {
    const checkAuth = async () => {
      setLoading(true);
      
      // Si hay un token en memoria, intentamos obtener los datos del usuario
      if (getAccessToken()) {
        const result = await authService.getCurrentUser();
        if (result.success) {
          setUser(result.user);
        } else {
          // Si el token no es válido, cerramos sesión
          await authService.logout();
        }
      }
      
      setLoading(false);
    };

    checkAuth();
  }, []); // El array vacío es importante - solo se ejecuta al montar

  /**
   * Refrescar datos del usuario - útil después de actualizar perfil
   */
  const refreshUser = async () => {
    const result = await authService.getCurrentUser();
    if (result.success) {
      setUser(result.user);
      return true;
    }
    return false;
  };

  /**
   * Verificar si el usuario tiene un rol específico
   * Útil para mostrar/ocultar elementos de UI según el rol
   */
  const hasRole = (roleName) => {
    return user?.rol_usuario?.name === roleName;
  };

  /**
   * Verificar si el usuario tiene alguno de los roles permitidos
   * Ideal para rutas que aceptan múltiples roles
   */
  const hasAnyRole = (roles) => {
    if (!user?.rol_usuario?.name) return false;
    return roles.includes(user.rol_usuario.name);
  };

  // Objeto con todo lo que estará disponible en el contexto
  const value = {
    user,                // Datos del usuario
    loading,             // Estado de carga
    error,               // Mensajes de error
    login,               // Función para iniciar sesión
    logout,              // Función para cerrar sesión
    refreshUser,         // Refrescar datos
    hasRole,             // Verificar rol específico
    hasAnyRole,          // Verificar múltiples roles
    isAuthenticated: !!user,  // Booleano: true si hay usuario
    userRole: user?.rol_usuario?.name  // Rol del usuario actual
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};