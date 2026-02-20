import api, { setAccessToken, clearAccessToken, getAccessToken } from './api';

class AuthService {
  /**
   * Iniciar sesión
   * Envía credenciales al backend y si son válidas, guarda el token y datos del usuario
   * Acepta tanto username como email (el backend decide cómo interpretarlo)
   */
  async login(username_email, password) {
    try {
      const response = await api.post('/auth/login/', {
        username_email,
        password
      });

      // Si la respuesta incluye access token, guardamos y devolvemos éxito
      if (response.data.access) {
        setAccessToken(response.data.access);
        return {
          success: true,
          user: response.data.user,
          access: response.data.access
        };
      }
      
      // Respuesta inesperada (no debería pasar)
      return {
        success: false,
        error: 'Respuesta inválida del servidor'
      };
    } catch (error) {
      console.error('Error en login:', error);
      
      // Extraemos el mensaje de error de diferentes formatos posibles
      // Django REST Framework puede devolver errores en distintas estructuras
      const errorMsg = error.response?.data?.error || 
                      error.response?.data?.non_field_errors?.[0] ||
                      'Error al iniciar sesión';
      
      return {
        success: false,
        error: errorMsg
      };
    }
  }

  /**
   * Cerrar sesión
   * Limpia el token local y notifica al backend (opcional)
   * Notar que aunque falle la petición, limpiamos localmente
   */
  async logout() {
    try {
      clearAccessToken();  // Limpiamos primero por si acaso
      await api.post('/auth/logout/');
      return { success: true };
    } catch (error) {
      console.error('Error en logout:', error);
      clearAccessToken();  // Aseguramos limpieza
      return { success: true };  // Devolvemos éxito aunque falle el backend
    }
  }

  /**
   * Obtener datos del usuario actual
   * Se usa al recargar la página o para refrescar datos
   */
  async getCurrentUser() {
    try {
      const response = await api.get('/auth/me/');
      return {
        success: true,
        user: response.data
      };
    } catch (error) {
      console.error('Error obteniendo usuario:', error);
      return {
        success: false,
        error: 'No se pudo obtener información del usuario'
      };
    }
  }

  /**
   * Refrescar token manualmente
   * Normalmente lo hace el interceptor, pero podemos llamarlo explícitamente
   */
  async refreshToken() {
    try {
      const response = await api.post('/auth/refresh/');
      
      if (response.data.access) {
        setAccessToken(response.data.access);
        return {
          success: true,
          access: response.data.access
        };
      }
      
      return { success: false };
    } catch (error) {
      console.error('Error refrescando token:', error);
      return { success: false };
    }
  }

  /**
   * Verificar si hay token (sesión aparentemente activa)
   * Útil para decisiones rápidas en UI, aunque no garantiza que el token sea válido
   */
  isAuthenticated() {
    return !!getAccessToken();
  }
}

// Singleton - misma instancia para toda la app
const authService = new AuthService();
export default authService;