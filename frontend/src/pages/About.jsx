import React from 'react';
import { Link } from 'react-router-dom';
import { Button } from '../components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';

const About = () => {
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-12">
        {/* Botón para volver al inicio - mejora la navegación */}
        <div className="mb-8">
          <Link to="/">
            <Button variant="ghost">← Volver al inicio</Button>
          </Link>
        </div>

        <h1 className="text-4xl font-bold text-gray-900 mb-6">
          Acerca del Proyecto
        </h1>

        <div className="prose max-w-4xl">
          {/* Tarjeta de descripción general */}
          <Card className="mb-8">
            <CardHeader>
              <CardTitle>Descripción del Proyecto</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-gray-700 mb-4">
                Este es un sistema de autenticación y gestión por roles desarrollado como 
                proyecto demostrativo para validar conocimientos técnicos. Implementa 
                un backend en Django con API REST y un frontend en React con Vite.
              </p>
              <p className="text-gray-700">
                El sistema permite tres tipos de usuarios (Administrador, Estudiante, Empresa) 
                cada uno con su propio dashboard y funcionalidades específicas.
              </p>
            </CardContent>
          </Card>

          {/* Stack tecnológico detallado */}
          <Card className="mb-8">
            <CardHeader>
              <CardTitle>Stack Tecnológico</CardTitle>
              <CardDescription>Tecnologías utilizadas en el desarrollo</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid gap-4">
                <div>
                  <h3 className="font-semibold text-lg">Backend</h3>
                  <ul className="list-disc list-inside text-gray-600">
                    <li><span className="font-medium">Django 5+</span> - Framework principal</li>
                    <li><span className="font-medium">Django REST Framework</span> - API REST</li>
                    <li><span className="font-medium">SimpleJWT</span> - Autenticación JWT</li>
                    <li><span className="font-medium">SQLite</span> - Base de datos (desarrollo)</li>
                    <li><span className="font-medium">CORS Headers</span> - Seguridad</li>
                  </ul>
                </div>

                <div>
                  <h3 className="font-semibold text-lg">Frontend</h3>
                  <ul className="list-disc list-inside text-gray-600">
                    <li><span className="font-medium">React 18+</span> - Biblioteca UI</li>
                    <li><span className="font-medium">Vite</span> - Bundler y dev server</li>
                    <li><span className="font-medium">React Router DOM</span> - Enrutamiento</li>
                    <li><span className="font-medium">Axios</span> - Cliente HTTP</li>
                  </ul>
                </div>

                <div>
                  <h3 className="font-semibold text-lg">Estilos y UI</h3>
                  <ul className="list-disc list-inside text-gray-600">
                    <li><span className="font-medium">Tailwind CSS v4</span> - Framework CSS</li>
                    <li><span className="font-medium">shadcn/ui</span> - Componentes reutilizables</li>
                  </ul>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Diagrama de arquitectura en ASCII */}
          <Card className="mb-8">
            <CardHeader>
              <CardTitle>Arquitectura</CardTitle>
            </CardHeader>
            <CardContent>
              <pre className="bg-gray-900 text-gray-100 p-4 rounded-lg overflow-x-auto">
{`PROYECTO
├── BACKEND (Django - Puerto 8000)
│   ├── Modelos: Usuario, Rol
│   ├── Autenticación: JWT (access + refresh)
│   ├── Decoradores: @rol_obligatorio
│   └── Endpoints REST: /api/*
│
├── FRONTEND (React + Vite - Puerto 5173)
│   ├── Contexto: AuthContext
│   ├── Servicios: Axios + interceptores
│   ├── Rutas: Protegidas por rol
│   └── Componentes: shadcn/ui
│
└── COMUNICACIÓN
    ├── Access Token: Header Authorization
    ├── Refresh Token: Cookie HttpOnly
    └── CORS: Solo localhost:5173`}
              </pre>
            </CardContent>
          </Card>

          {/* Decisiones de seguridad explicadas */}
          <Card>
            <CardHeader>
              <CardTitle>Decisiones de Seguridad</CardTitle>
            </CardHeader>
            <CardContent>
              <ul className="list-disc list-inside text-gray-600 space-y-2">
                <li>
                  <span className="font-medium">JWT vs Sesiones:</span> Se eligió JWT por 
                  escalabilidad y separación frontend/backend
                </li>
                <li>
                  <span className="font-medium">Refresh Token:</span> Almacenado en cookie 
                  HttpOnly para prevenir XSS
                </li>
                <li>
                  <span className="font-medium">Access Token:</span> En memoria (no localStorage) 
                  para evitar XSS
                </li>
                <li>
                  <span className="font-medium">Doble validación:</span> Roles validados en 
                  backend (obligatorio) y frontend (UX)
                </li>
                <li>
                  <span className="font-medium">CSRF:</span> No aplica por usar JWT en headers
                </li>
              </ul>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default About;