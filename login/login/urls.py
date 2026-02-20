from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/', include('usuarios.urls')),
    path('api/estudiantes/', include('estudiantes.urls')),
    path('api/empresas/', include('empresas.urls')),
    path('api/admin/', include('admin.urls')),
]