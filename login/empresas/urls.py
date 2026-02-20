from django.urls import path
from .views import EmpresaDashboardView, OfertasEmpresaView

# app_name se usa para namespacing de URLs. Permite referenciar estas URLs de forma única
# en todo el proyecto usando 'empresas:dashboard' o 'empresas:ofertas'.
# Esto es muy útil cuando tienes varias apps y quieres evitar conflictos de nombres.
app_name = 'empresas'

# Definimos las rutas de la app.
# Cada ruta asocia un patrón de URL con una vista y le asigna un nombre único.
urlpatterns = [
    # Ruta para el dashboard: /api/empresas/dashboard/
    path('dashboard/', EmpresaDashboardView.as_view(), name='dashboard'),
    # Ruta para gestionar ofertas: /api/empresas/ofertas/
    path('ofertas/', OfertasEmpresaView.as_view(), name='ofertas'),
]