from django.urls import path
from .views import EstudianteDashboardView, PerfilEstudianteView

app_name = 'estudiantes'

urlpatterns = [
    path('dashboard/', EstudianteDashboardView.as_view(), name='dashboard'),
    path('perfil/', PerfilEstudianteView.as_view(), name='perfil'),
]