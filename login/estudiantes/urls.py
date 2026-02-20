from django.urls import path
from .views import EstudianteDashboardView, PerfilEstudianteView

# Namespace para URLs de estudiantes.
app_name = 'estudiantes'

urlpatterns = [
    # Ruta para el dashboard: /api/estudiantes/dashboard/
    path('dashboard/', EstudianteDashboardView.as_view(), name='dashboard'),
    # Ruta para ver/editar perfil: /api/estudiantes/perfil/
    path('perfil/', PerfilEstudianteView.as_view(), name='perfil'),
]