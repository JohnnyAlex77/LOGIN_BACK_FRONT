import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import { Button } from '../components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';

const Home = () => {
  const { isAuthenticated, userRole } = useAuth();

  // Determinar dashboard según rol
  const getDashboardLink = () => {
    if (!isAuthenticated) return '/login';
    
    switch (userRole) {
      case 'Admin': return '/dashboard/admin';
      case 'Estudiante': return '/dashboard/estudiante';
      case 'Empresa': return '/dashboard/empresa';
      default: return '/login';
    }
  };

  return (
    <div className="min-h-screen bg-linear-to-b from-gray-50 to-gray-100">
      {/* Hero Section */}
      <div className="container mx-auto px-4 py-16">
        <div className="text-center">
          <h1 className="text-5xl font-bold text-gray-900 mb-4">
            Sistema de Gestión Educativa
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
            Plataforma integrada para estudiantes, empresas y administradores
          </p>
          
          <div className="space-x-4">
            <Link to="/about">
              <Button variant="outline" size="lg">
                Acerca de
              </Button>
            </Link>
            <Link to={getDashboardLink()}>
              <Button size="lg">
                {isAuthenticated ? 'Ir a Dashboard' : 'Iniciar Sesión'}
              </Button>
            </Link>
          </div>
        </div>

        {/* Stack Tecnológico */}
        <div className="mt-20">
          <h2 className="text-3xl font-semibold text-center mb-10">
            Stack Tecnológico
          </h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <Card>
              <CardHeader>
                <CardTitle>Django</CardTitle>
                <CardDescription>Backend</CardDescription>
              </CardHeader>
              <CardContent>
                <ul className="list-disc list-inside text-gray-600">
                  <li>Django REST Framework</li>
                  <li>Autenticación JWT</li>
                  <li>Modelos personalizados</li>
                  <li>SQLite</li>
                </ul>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>React</CardTitle>
                <CardDescription>Frontend</CardDescription>
              </CardHeader>
              <CardContent>
                <ul className="list-disc list-inside text-gray-600">
                  <li>Vite como bundler</li>
                  <li>React Router DOM</li>
                  <li>Context API</li>
                  <li>Axios</li>
                </ul>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Tailwind v4</CardTitle>
                <CardDescription>Estilos</CardDescription>
              </CardHeader>
              <CardContent>
                <ul className="list-disc list-inside text-gray-600">
                  <li>CSS utility-first</li>
                  <li>Diseño responsive</li>
                  <li>Personalizable</li>
                </ul>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>shadcn/ui</CardTitle>
                <CardDescription>Componentes</CardDescription>
              </CardHeader>
              <CardContent>
                <ul className="list-disc list-inside text-gray-600">
                  <li>Componentes accesibles</li>
                  <li>Copiados al proyecto</li>
                  <li>Personalizables</li>
                </ul>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;