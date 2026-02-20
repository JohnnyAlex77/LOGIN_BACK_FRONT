from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Ruta para el panel de admin nativo de Django (no confundir con nuestra API admin)
    # Útil para superusers, pero no para el día a día de la aplicación.
    path('admin/', admin.site.urls),
    
    # API endpoints
    # Todas las rutas de la API comienzan con /api/
    # Esto organiza y diferencia claramente las rutas de la API de otras posibles rutas.
    
    # Autenticación y usuarios base
    path('api/', include('usuarios.urls')),
    # Rutas específicas de estudiantes
    path('api/estudiantes/', include('estudiantes.urls')),
    # Rutas específicas de empresas
    path('api/empresas/', include('empresas.urls')),
    # Rutas de administración (CRUD de usuarios)
    path('api/admin/', include('admin.urls')),
]