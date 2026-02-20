from django.urls import path
from .views import EmpresaDashboardView, OfertasEmpresaView

app_name = 'empresas'

urlpatterns = [
    path('dashboard/', EmpresaDashboardView.as_view(), name='dashboard'),
    path('ofertas/', OfertasEmpresaView.as_view(), name='ofertas'),
]