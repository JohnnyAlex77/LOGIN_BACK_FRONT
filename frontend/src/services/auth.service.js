import api, { setAccessToken, clearAccessToken, getAccessToken } from './api';

class AuthService {
  async login(username_email, password) {
    try {
      const response = await api.post('/auth/login/', {
        username_email,
        password
      });

      if (response.data.access) {
        setAccessToken(response.data.access);
        return {
          success: true,
          user: response.data.user,
          access: response.data.access
        };
      }
      
      return {
        success: false,
        error: 'Respuesta inválida del servidor'
      };
    } catch (error) {
      console.error('Error en login:', error);
      
      const errorMsg = error.response?.data?.error || 
                      error.response?.data?.non_field_errors?.[0] ||
                      'Error al iniciar sesión';
      
      return {
        success: false,
        error: errorMsg
      };
    }
  }

  async logout() {
    try {
      clearAccessToken();
      await api.post('/auth/logout/');
      return { success: true };
    } catch (error) {
      console.error('Error en logout:', error);
      clearAccessToken();
      return { success: true };
    }
  }

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

  isAuthenticated() {
    return !!getAccessToken();
  }
}

const authService = new AuthService();
export default authService;