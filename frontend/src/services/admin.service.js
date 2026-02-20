import api from './api';

class AdminService {
  /**
   * Obtener lista de usuarios con filtros
   */
  async getUsers(filters = {}) {
    try {
      const params = new URLSearchParams();
      
      if (filters.search) params.append('search', filters.search);
      if (filters.rol) params.append('rol', filters.rol);
      if (filters.activo !== undefined) params.append('activo', filters.activo);
      
      const response = await api.get(`/admin/usuarios/?${params.toString()}`);
      return {
        success: true,
        users: response.data.results,
        count: response.data.count
      };
    } catch (error) {
      console.error('Error obteniendo usuarios:', error);
      return {
        success: false,
        error: 'Error al cargar usuarios'
      };
    }
  }

  /**
   * Obtener un usuario por ID
   */
  async getUserById(id) {
    try {
      const response = await api.get(`/admin/usuarios/${id}/`);
      return {
        success: true,
        user: response.data
      };
    } catch (error) {
      console.error('Error obteniendo usuario:', error);
      return {
        success: false,
        error: 'Usuario no encontrado'
      };
    }
  }

  /**
   * Crear nuevo usuario
   */
  async createUser(userData) {
    try {
      const response = await api.post('/admin/usuarios/', userData);
      return {
        success: true,
        user: response.data,
        message: 'Usuario creado correctamente'
      };
    } catch (error) {
      console.error('Error creando usuario:', error);
      return {
        success: false,
        error: error.response?.data || 'Error al crear usuario'
      };
    }
  }

  /**
   * Actualizar usuario
   */
  async updateUser(id, userData) {
    try {
      const response = await api.put(`/admin/usuarios/${id}/`, userData);
      return {
        success: true,
        user: response.data,
        message: 'Usuario actualizado correctamente'
      };
    } catch (error) {
      console.error('Error actualizando usuario:', error);
      return {
        success: false,
        error: error.response?.data || 'Error al actualizar usuario'
      };
    }
  }

  /**
   * Actualización parcial de usuario
   */
  async partialUpdateUser(id, userData) {
    try {
      const response = await api.patch(`/admin/usuarios/${id}/`, userData);
      return {
        success: true,
        user: response.data,
        message: 'Usuario actualizado correctamente'
      };
    } catch (error) {
      console.error('Error actualizando usuario:', error);
      return {
        success: false,
        error: error.response?.data || 'Error al actualizar usuario'
      };
    }
  }

  /**
   * Eliminar usuario
   */
  async deleteUser(id) {
    try {
      await api.delete(`/admin/usuarios/${id}/`);
      return {
        success: true,
        message: 'Usuario eliminado correctamente'
      };
    } catch (error) {
      console.error('Error eliminando usuario:', error);
      return {
        success: false,
        error: error.response?.data?.error || 'Error al eliminar usuario'
      };
    }
  }

  /**
   * Activar/desactivar usuario
   */
  async toggleUserActive(id) {
    try {
      const response = await api.post(`/admin/usuarios/${id}/toggle-activo/`);
      return {
        success: true,
        is_active: response.data.is_active,
        message: response.data.message
      };
    } catch (error) {
      console.error('Error cambiando estado:', error);
      return {
        success: false,
        error: error.response?.data?.error || 'Error al cambiar estado'
      };
    }
  }

  /**
   * Obtener roles disponibles
   */
  async getRoles() {
    try {
      const response = await api.get('/admin/usuarios/roles/');
      return {
        success: true,
        roles: response.data
      };
    } catch (error) {
      console.error('Error obteniendo roles:', error);
      return {
        success: false,
        error: 'Error al cargar roles'
      };
    }
  }
}

const adminService = new AdminService();
export default adminService;