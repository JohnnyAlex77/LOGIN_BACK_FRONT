import React, { useState, useEffect } from 'react';
import { AuthContext } from '../contexts/AuthContext'; 
import authService from '../services/auth.service';
import { getAccessToken } from '../services/api';

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  /**
   * Iniciar sesión
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
   * Cerrar sesión
   */
  const logout = async () => {
    setLoading(true);
    
    try {
      await authService.logout();
      setUser(null);
    } catch (err) {
      console.error('Error en logout:', err);
      setUser(null);
    } finally {
      setLoading(false);
    }
  };

  /**
   * Verificar si hay sesión activa al cargar la app
   */
  useEffect(() => {
    const checkAuth = async () => {
      setLoading(true);
      
      if (getAccessToken()) {
        const result = await authService.getCurrentUser();
        if (result.success) {
          setUser(result.user);
        } else {
          await authService.logout();
        }
      }
      
      setLoading(false);
    };

    checkAuth();
  }, []);

  /**
   * Refrescar datos del usuario
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
   */
  const hasRole = (roleName) => {
    return user?.rol_usuario?.name === roleName;
  };

  /**
   * Verificar si el usuario tiene alguno de los roles permitidos
   */
  const hasAnyRole = (roles) => {
    if (!user?.rol_usuario?.name) return false;
    return roles.includes(user.rol_usuario.name);
  };

  const value = {
    user,
    loading,
    error,
    login,
    logout,
    refreshUser,
    hasRole,
    hasAnyRole,
    isAuthenticated: !!user,
    userRole: user?.rol_usuario?.name
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};