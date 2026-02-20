import React from 'react';
import { useAuth } from '../../hooks/useAuth'
import { Button } from '../../components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../components/ui/card';

const EstudianteDashboard = () => {
  const { user, logout } = useAuth();

  const handleLogout = async () => {
    await logout();
    window.location.href = '/login';
  };

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header con información del estudiante */}
      <header className="bg-white shadow">
        <div className="container mx-auto px-4 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gray-900">
            Panel de Estudiante
          </h1>
          <div className="flex items-center space-x-4">
            <span className="text-gray-600">
              {user?.first_name} {user?.last_name}
            </span>
            <Button variant="outline" onClick={handleLogout}>
              Cerrar Sesión
            </Button>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8">
        {/* Tarjetas de métricas académicas */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-gray-500">
                Cursos Inscritos
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-3xl font-bold">3</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-gray-500">
                Tareas Pendientes
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-3xl font-bold">2</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-gray-500">
                Promedio General
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-3xl font-bold">4.5</p>
            </CardContent>
          </Card>
        </div>

        {/* Lista de cursos del estudiante */}
        <Card className="mb-8">
          <CardHeader>
            <CardTitle>Mis Cursos</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex justify-between items-center p-3 bg-gray-50 rounded">
                <div>
                  <h3 className="font-medium">Matemáticas Avanzadas</h3>
                  <p className="text-sm text-gray-500">Prof. Juan Pérez</p>
                </div>
                <span className="px-2 py-1 bg-green-100 text-green-800 rounded text-sm">
                  En progreso
                </span>
              </div>
              <div className="flex justify-between items-center p-3 bg-gray-50 rounded">
                <div>
                  <h3 className="font-medium">Física Moderna</h3>
                  <p className="text-sm text-gray-500">Prof. Ana García</p>
                </div>
                <span className="px-2 py-1 bg-yellow-100 text-yellow-800 rounded text-sm">
                  Pendiente
                </span>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Actividad reciente del estudiante */}
        <Card>
          <CardHeader>
            <CardTitle>Actividad Reciente</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              <div className="text-sm">
                <span className="font-medium">📝 Tarea entregada:</span> Ejercicios de cálculo
                <span className="text-gray-500 ml-2">hace 2 horas</span>
              </div>
              <div className="text-sm">
                <span className="font-medium">📚 Curso completado:</span> Introducción a Python
                <span className="text-gray-500 ml-2">ayer</span>
              </div>
            </div>
          </CardContent>
        </Card>
      </main>
    </div>
  );
};

export default EstudianteDashboard;