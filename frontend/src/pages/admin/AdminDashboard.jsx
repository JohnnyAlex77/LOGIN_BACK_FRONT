import React, { useState } from 'react';
import { useAuth } from '../../hooks/useAuth';
import { Button } from '../../components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../../components/ui/tabs';
import UserManagement from './UserManagement';

const AdminDashboard = () => {
  const { user, logout } = useAuth();
  const [activeTab, setActiveTab] = useState('overview'); // Pestaña activa por defecto

  // Manejar cierre de sesión
  const handleLogout = async () => {
    await logout();
    window.location.href = '/login'; // Redirección completa, no solo navigate
  };

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header con información del usuario y botón de logout */}
      <header className="bg-white shadow">
        <div className="container mx-auto px-4 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gray-900">
            Panel de Administrador
          </h1>
          <div className="flex items-center space-x-4">
            <span className="text-gray-600">
              {user?.first_name} {user?.last_name} ({user?.rol_usuario?.name})
            </span>
            <Button variant="outline" onClick={handleLogout}>
              Cerrar Sesión
            </Button>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8">
        {/* Sistema de pestañas para organizar el contenido */}
        <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-4">
          <TabsList>
            <TabsTrigger value="overview">Resumen</TabsTrigger>
            <TabsTrigger value="users">Gestión de Usuarios</TabsTrigger>
            <TabsTrigger value="stats">Estadísticas</TabsTrigger>
          </TabsList>

          {/* Pestaña de resumen con tarjetas de métricas */}
          <TabsContent value="overview" className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <Card>
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm font-medium text-gray-500">
                    Total Usuarios
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-3xl font-bold">--</p>
                  <p className="text-xs text-gray-500">Cargando...</p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm font-medium text-gray-500">
                    Estudiantes
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-3xl font-bold">--</p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm font-medium text-gray-500">
                    Empresas
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-3xl font-bold">--</p>
                </CardContent>
              </Card>
            </div>

            <Card>
              <CardHeader>
                <CardTitle>Actividad Reciente</CardTitle>
                <CardDescription>
                  Últimas acciones en el sistema
                </CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-gray-500 text-center py-8">
                  Próximamente: Registro de actividad
                </p>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Pestaña de gestión de usuarios - componente separado */}
          <TabsContent value="users">
            <UserManagement />
          </TabsContent>

          {/* Pestaña de estadísticas - en desarrollo */}
          <TabsContent value="stats">
            <Card>
              <CardHeader>
                <CardTitle>Estadísticas del Sistema</CardTitle>
                <CardDescription>
                  Próximamente: Gráficos y métricas
                </CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-gray-500 text-center py-8">
                  Sección en desarrollo
                </p>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </main>
    </div>
  );
};

export default AdminDashboard;