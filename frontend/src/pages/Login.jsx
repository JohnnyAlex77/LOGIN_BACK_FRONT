import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '../components/ui/card';
import { Alert, AlertDescription } from '../components/ui/alert';

const Login = () => {
  const navigate = useNavigate();
  const { login, loading } = useAuth();
  
  const [formData, setFormData] = useState({
    username_email: '',
    password: ''
  });
  
  const [errors, setErrors] = useState({});
  const [loginError, setLoginError] = useState('');

  // Manejar cambios en el formulario
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    // Limpiar error del campo cuando el usuario escribe
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }));
    }
    // Limpiar error general
    if (loginError) setLoginError('');
  };

  // Validar formulario
  const validateForm = () => {
    const newErrors = {};
    
    if (!formData.username_email.trim()) {
      newErrors.username_email = 'Usuario o email es requerido';
    }
    
    if (!formData.password) {
      newErrors.password = 'Contraseña es requerida';
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  // Manejar envío del formulario
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) return;
    
    const result = await login(formData.username_email, formData.password);
    
    if (result.success) {
      // Redirigir según rol
      const role = result.user?.rol_usuario?.name;
      
      if (role === 'Admin') {
        navigate('/dashboard/admin');
      } else if (role === 'Estudiante') {
        navigate('/dashboard/estudiante');
      } else if (role === 'Empresa') {
        navigate('/dashboard/empresa');
      } else {
        navigate('/'); // Por defecto
      }
    } else {
      setLoginError(result.error || 'Error al iniciar sesión');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <Card className="w-full max-w-md">
        <CardHeader className="space-y-1">
          <CardTitle className="text-2xl font-bold text-center">
            Iniciar Sesión
          </CardTitle>
          <CardDescription className="text-center">
            Ingresa tu usuario/email y contraseña
          </CardDescription>
        </CardHeader>
        
        <CardContent>
          {loginError && (
            <Alert variant="destructive" className="mb-4">
              <AlertDescription>{loginError}</AlertDescription>
            </Alert>
          )}
          
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="username_email">
                Usuario o Email <span className="text-red-500">*</span>
              </Label>
              <Input
                id="username_email"
                name="username_email"
                type="text"
                placeholder="ej: admin o admin@example.com"
                value={formData.username_email}
                onChange={handleChange}
                disabled={loading}
                className={errors.username_email ? 'border-red-500' : ''}
              />
              {errors.username_email && (
                <p className="text-sm text-red-500">{errors.username_email}</p>
              )}
            </div>

            <div className="space-y-2">
              <Label htmlFor="password">
                Contraseña <span className="text-red-500">*</span>
              </Label>
              <Input
                id="password"
                name="password"
                type="password"
                placeholder="••••••••"
                value={formData.password}
                onChange={handleChange}
                disabled={loading}
                className={errors.password ? 'border-red-500' : ''}
              />
              {errors.password && (
                <p className="text-sm text-red-500">{errors.password}</p>
              )}
            </div>

            <Button 
              type="submit" 
              className="w-full"
              disabled={loading}
            >
              {loading ? 'Iniciando sesión...' : 'Iniciar Sesión'}
            </Button>
          </form>
        </CardContent>
        
        <CardFooter className="flex justify-center">
          <Link 
            to="/" 
            className="text-sm text-gray-600 hover:text-gray-900"
          >
            ← Volver al inicio
          </Link>
        </CardFooter>
      </Card>
    </div>
  );
};

export default Login;