import React, { useState, useEffect, useCallback } from 'react';
import { useAuth } from '../../hooks/useAuth';
import adminService from '../../services/admin.service';
import { Button } from '../../components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/card';
import { Input } from '../../components/ui/input';
import { Label } from '../../components/ui/label';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '../../components/ui/select';
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from '../../components/ui/alert-dialog';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from '../../components/ui/dialog';
import { Alert, AlertDescription } from '../../components/ui/alert';
import { Loader2, Search, UserPlus, Edit, Trash2, ToggleLeft, ToggleRight } from 'lucide-react';

const UserManagement = () => {
  const { user: currentUser } = useAuth();
  
  // Estados
  const [users, setUsers] = useState([]);
  const [roles, setRoles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  
  // Filtros
  const [filters, setFilters] = useState({
    search: '',
    rol: 'all',
    activo: undefined
  });
  
  // Modal de usuario
  const [showUserModal, setShowUserModal] = useState(false);
  const [editingUser, setEditingUser] = useState(null);
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    first_name: '',
    last_name: '',
    telefono: '',
    fecha_nacimiento: '',
    rol_id: '',
    password: '',
    is_active: true
  });
  const [formErrors, setFormErrors] = useState({});
  
  // Diálogo de confirmación
  const [showDeleteDialog, setShowDeleteDialog] = useState(false);
  const [userToDelete, setUserToDelete] = useState(null);

  // Función para cargar roles
  const loadRoles = useCallback(async () => {
    try {
      const result = await adminService.getRoles();
      if (result.success) {
        setRoles(result.roles);
      }
    } catch (error) {
      console.error('Error cargando roles:', error);
    }
  }, []);

  // Función para cargar usuarios
  const loadUsers = useCallback(async () => {
    setLoading(true);
    setError(null);
    
    try {
      // Preparar filtros para enviar al backend
      const params = { ...filters };
      
      // Si rol es 'all', no enviarlo (todos los roles)
      if (params.rol === 'all') {
        delete params.rol;
      }
      
      const result = await adminService.getUsers(params);
      
      if (result.success) {
        setUsers(result.users);
      } else {
        setError(result.error || 'Error al cargar usuarios');
      }
    } catch (error) {
      console.error('Error cargando usuarios:', error);
      setError('Error de conexión con el servidor');
    } finally {
      setLoading(false);
    }
  }, [filters]);

  // Cargar roles al montar el componente
  useEffect(() => {
    loadRoles();
  }, [loadRoles]);

  // Cargar usuarios cuando cambian los filtros
  useEffect(() => {
    loadUsers();
  }, [loadUsers]);

  /**
   * Manejar cambios en formulario
   */
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    if (formErrors[name]) {
      setFormErrors(prev => ({ ...prev, [name]: null }));
    }
  };

  /**
   * Validar formulario
   */
  const validateForm = () => {
    const errors = {};
    
    if (!formData.username.trim()) {
      errors.username = 'El nombre de usuario es requerido';
    } else if (formData.username.length < 3) {
      errors.username = 'Mínimo 3 caracteres';
    }
    
    if (!formData.email.trim()) {
      errors.email = 'El email es requerido';
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      errors.email = 'Email no válido';
    }
    
    if (!formData.rol_id) {
      errors.rol_id = 'El rol es requerido';
    }
    
    if (!editingUser && !formData.password) {
      errors.password = 'La contraseña es requerida';
    } else if (formData.password && formData.password.length < 6) {
      errors.password = 'Mínimo 6 caracteres';
    }
    
    setFormErrors(errors);
    return Object.keys(errors).length === 0;
  };

  /**
   * Guardar usuario (crear o actualizar)
   */
  const handleSaveUser = async () => {
    if (!validateForm()) return;
    
    setLoading(true);
    setError(null);
    
    try {
      let result;
      if (editingUser) {
        result = await adminService.updateUser(editingUser.id, formData);
      } else {
        result = await adminService.createUser(formData);
      }
      
      if (result.success) {
        setSuccess(result.message);
        setShowUserModal(false);
        resetForm();
        loadUsers();
        setTimeout(() => setSuccess(null), 3000);
      } else {
        setError(typeof result.error === 'object' ? JSON.stringify(result.error) : result.error);
      }
    } catch (error) {
      console.error('Error guardando usuario:', error);
      setError('Error al guardar usuario');
    } finally {
      setLoading(false);
    }
  };

  /**
   * Eliminar usuario
   */
  const handleDeleteUser = async () => {
    if (!userToDelete) return;
    
    setLoading(true);
    setError(null);
    
    try {
      const result = await adminService.deleteUser(userToDelete.id);
      
      if (result.success) {
        setSuccess(result.message);
        setShowDeleteDialog(false);
        setUserToDelete(null);
        loadUsers();
        setTimeout(() => setSuccess(null), 3000);
      } else {
        setError(result.error);
      }
    } catch (error) {
      console.error('Error eliminando usuario:', error);
      setError('Error al eliminar usuario');
    } finally {
      setLoading(false);
    }
  };

  /**
   * Activar/desactivar usuario
   */
  const handleToggleActive = async (user) => {
    setLoading(true);
    
    try {
      const result = await adminService.toggleUserActive(user.id);
      
      if (result.success) {
        setSuccess(result.message);
        loadUsers();
        setTimeout(() => setSuccess(null), 3000);
      } else {
        setError(result.error);
      }
    } catch (error) {
      console.error('Error cambiando estado:', error);
      setError('Error al cambiar estado');
    } finally {
      setLoading(false);
    }
  };

  /**
   * Resetear formulario
   */
  const resetForm = () => {
    setEditingUser(null);
    setFormData({
      username: '',
      email: '',
      first_name: '',
      last_name: '',
      telefono: '',
      fecha_nacimiento: '',
      rol_id: '',
      password: '',
      is_active: true
    });
    setFormErrors({});
  };

  /**
   * Abrir modal para editar
   */
  const openEditModal = (user) => {
    setEditingUser(user);
    setFormData({
      username: user.username,
      email: user.email,
      first_name: user.first_name || '',
      last_name: user.last_name || '',
      telefono: user.telefono || '',
      fecha_nacimiento: user.fecha_nacimiento || '',
      rol_id: user.rol_usuario?.id || '',
      password: '',
      is_active: user.is_active
    });
    setShowUserModal(true);
  };

  /**
   * Manejar cambio en filtro de búsqueda
   */
  const handleSearchChange = (e) => {
    setFilters(prev => ({ ...prev, search: e.target.value }));
  };

  /**
   * Manejar cambio en filtro de rol
   */
  const handleRolChange = (value) => {
    setFilters(prev => ({ ...prev, rol: value }));
  };

  /**
   * Manejar cambio en filtro de estado
   */
  const handleActivoChange = (value) => {
    setFilters(prev => ({ 
      ...prev, 
      activo: value === 'all' ? undefined : value === 'true'
    }));
  };

  /**
   * Limpiar filtros
   */
  const clearFilters = () => {
    setFilters({ search: '', rol: 'all', activo: undefined });
  };

  // Renderizado condicional para cuando no hay roles cargados
  if (roles.length === 0 && !error) {
    return (
      <div className="flex justify-center items-center p-8">
        <Loader2 className="w-8 h-8 animate-spin text-gray-400" />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Mensajes de éxito/error */}
      {success && (
        <Alert className="bg-green-50 border-green-200">
          <AlertDescription className="text-green-800">{success}</AlertDescription>
        </Alert>
      )}
      
      {error && (
        <Alert variant="destructive">
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {/* Filtros y acciones */}
      <Card>
        <CardHeader>
          <div className="flex justify-between items-center">
            <CardTitle>Gestión de Usuarios</CardTitle>
            <Button onClick={() => {
              resetForm();
              setShowUserModal(true);
            }}>
              <UserPlus className="w-4 h-4 mr-2" />
              Nuevo Usuario
            </Button>
          </div>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="relative">
              <Search className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
              <Input
                placeholder="Buscar usuario..."
                className="pl-9"
                value={filters.search}
                onChange={handleSearchChange}
              />
            </div>
            
            <Select
              value={filters.rol}
              onValueChange={handleRolChange}
            >
              <SelectTrigger>
                <SelectValue placeholder="Todos los roles" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">Todos los roles</SelectItem>
                {roles.map(rol => (
                  <SelectItem key={rol.id} value={rol.id.toString()}>
                    {rol.name}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>

            <Select
              value={filters.activo === undefined ? 'all' : filters.activo.toString()}
              onValueChange={handleActivoChange}
            >
              <SelectTrigger>
                <SelectValue placeholder="Todos los estados" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">Todos los estados</SelectItem>
                <SelectItem value="true">Activos</SelectItem>
                <SelectItem value="false">Inactivos</SelectItem>
              </SelectContent>
            </Select>

            <Button variant="outline" onClick={clearFilters}>
              Limpiar Filtros
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Tabla de usuarios */}
      <Card>
        <CardContent className="p-0">
          {loading && users.length === 0 ? (
            <div className="flex justify-center items-center p-8">
              <Loader2 className="w-8 h-8 animate-spin text-gray-400" />
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="text-left p-3">Usuario</th>
                    <th className="text-left p-3">Email</th>
                    <th className="text-left p-3">Nombre</th>
                    <th className="text-left p-3">Rol</th>
                    <th className="text-left p-3">Estado</th>
                    <th className="text-left p-3">Fecha Registro</th>
                    <th className="text-left p-3">Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  {users.length === 0 ? (
                    <tr>
                      <td colSpan="7" className="text-center p-8 text-gray-500">
                        No hay usuarios para mostrar
                      </td>
                    </tr>
                  ) : (
                    users.map(user => (
                      <tr key={user.id} className="border-b hover:bg-gray-50">
                        <td className="p-3 font-medium">{user.username}</td>
                        <td className="p-3">{user.email}</td>
                        <td className="p-3">{`${user.first_name || ''} ${user.last_name || ''}`}</td>
                        <td className="p-3">
                          <span className="px-2 py-1 bg-blue-100 text-blue-800 rounded-full text-xs">
                            {user.rol_usuario?.name}
                          </span>
                        </td>
                        <td className="p-3">
                          <span className={`px-2 py-1 rounded-full text-xs ${
                            user.is_active 
                              ? 'bg-green-100 text-green-800' 
                              : 'bg-red-100 text-red-800'
                          }`}>
                            {user.is_active ? 'Activo' : 'Inactivo'}
                          </span>
                        </td>
                        <td className="p-3">
                          {new Date(user.date_joined).toLocaleDateString()}
                        </td>
                        <td className="p-3">
                          <div className="flex space-x-2">
                            <Button
                              variant="ghost"
                              size="sm"
                              onClick={() => openEditModal(user)}
                              title="Editar"
                            >
                              <Edit className="w-4 h-4" />
                            </Button>
                            
                            <Button
                              variant="ghost"
                              size="sm"
                              onClick={() => handleToggleActive(user)}
                              title={user.is_active ? 'Desactivar' : 'Activar'}
                              disabled={user.id === currentUser?.id}
                            >
                              {user.is_active ? (
                                <ToggleRight className="w-4 h-4 text-green-600" />
                              ) : (
                                <ToggleLeft className="w-4 h-4 text-gray-400" />
                              )}
                            </Button>
                            
                            <Button
                              variant="ghost"
                              size="sm"
                              className="text-red-600 hover:text-red-700"
                              onClick={() => {
                                setUserToDelete(user);
                                setShowDeleteDialog(true);
                              }}
                              disabled={user.id === currentUser?.id}
                              title="Eliminar"
                            >
                              <Trash2 className="w-4 h-4" />
                            </Button>
                          </div>
                        </td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Modal de creación/edición */}
      <Dialog open={showUserModal} onOpenChange={setShowUserModal}>
        <DialogContent className="max-w-2xl">
          <DialogHeader>
            <DialogTitle>
              {editingUser ? 'Editar Usuario' : 'Nuevo Usuario'}
            </DialogTitle>
          </DialogHeader>
          
          <div className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="username">
                  Usuario <span className="text-red-500">*</span>
                </Label>
                <Input
                  id="username"
                  name="username"
                  value={formData.username}
                  onChange={handleInputChange}
                  className={formErrors.username ? 'border-red-500' : ''}
                />
                {formErrors.username && (
                  <p className="text-sm text-red-500">{formErrors.username}</p>
                )}
              </div>

              <div className="space-y-2">
                <Label htmlFor="email">
                  Email <span className="text-red-500">*</span>
                </Label>
                <Input
                  id="email"
                  name="email"
                  type="email"
                  value={formData.email}
                  onChange={handleInputChange}
                  className={formErrors.email ? 'border-red-500' : ''}
                />
                {formErrors.email && (
                  <p className="text-sm text-red-500">{formErrors.email}</p>
                )}
              </div>

              <div className="space-y-2">
                <Label htmlFor="first_name">Nombre</Label>
                <Input
                  id="first_name"
                  name="first_name"
                  value={formData.first_name}
                  onChange={handleInputChange}
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="last_name">Apellido</Label>
                <Input
                  id="last_name"
                  name="last_name"
                  value={formData.last_name}
                  onChange={handleInputChange}
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="telefono">Teléfono</Label>
                <Input
                  id="telefono"
                  name="telefono"
                  value={formData.telefono}
                  onChange={handleInputChange}
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="fecha_nacimiento">Fecha Nacimiento</Label>
                <Input
                  id="fecha_nacimiento"
                  name="fecha_nacimiento"
                  type="date"
                  value={formData.fecha_nacimiento}
                  onChange={handleInputChange}
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="rol_id">
                  Rol <span className="text-red-500">*</span>
                </Label>
                <Select
                  value={formData.rol_id.toString()}
                  onValueChange={(value) => setFormData({ ...formData, rol_id: parseInt(value) })}
                >
                  <SelectTrigger className={formErrors.rol_id ? 'border-red-500' : ''}>
                    <SelectValue placeholder="Seleccionar rol" />
                  </SelectTrigger>
                  <SelectContent>
                    {roles.map(rol => (
                      <SelectItem key={rol.id} value={rol.id.toString()}>
                        {rol.name}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
                {formErrors.rol_id && (
                  <p className="text-sm text-red-500">{formErrors.rol_id}</p>
                )}
              </div>

              <div className="space-y-2">
                <Label htmlFor="password">
                  Contraseña {!editingUser && <span className="text-red-500">*</span>}
                </Label>
                <Input
                  id="password"
                  name="password"
                  type="password"
                  value={formData.password}
                  onChange={handleInputChange}
                  placeholder={editingUser ? "Dejar en blanco para no cambiar" : ""}
                  className={formErrors.password ? 'border-red-500' : ''}
                />
                {formErrors.password && (
                  <p className="text-sm text-red-500">{formErrors.password}</p>
                )}
              </div>
            </div>

            <div className="flex justify-end space-x-2 pt-4">
              <Button variant="outline" onClick={() => setShowUserModal(false)}>
                Cancelar
              </Button>
              <Button onClick={handleSaveUser} disabled={loading}>
                {loading && <Loader2 className="w-4 h-4 mr-2 animate-spin" />}
                {editingUser ? 'Actualizar' : 'Crear'}
              </Button>
            </div>
          </div>
        </DialogContent>
      </Dialog>

      {/* Diálogo de confirmación para eliminar */}
      <AlertDialog open={showDeleteDialog} onOpenChange={setShowDeleteDialog}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>¿Confirmar eliminación?</AlertDialogTitle>
            <AlertDialogDescription>
              Esta acción no se puede deshacer. Se eliminará permanentemente al usuario
              {userToDelete && (
                <span className="font-semibold"> "{userToDelete.username}"</span>
              )}.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>Cancelar</AlertDialogCancel>
            <AlertDialogAction 
              onClick={handleDeleteUser}
              className="bg-red-600 hover:bg-red-700"
            >
              {loading ? (
                <Loader2 className="w-4 h-4 animate-spin" />
              ) : (
                'Eliminar'
              )}
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </div>
  );
};

export default UserManagement;