from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AdminUsuarioViewSet

# DefaultRouter es una herramienta de DRF que automáticamente genera las rutas
# para un ViewSet. Por ejemplo, para un ViewSet que maneja usuarios, crea:
# - GET /usuarios/ (listar)
# - POST /usuarios/ (crear)
# - GET /usuarios/{id}/ (detalle)
# - PUT /usuarios/{id}/ (actualizar completo)
# - PATCH /usuarios/{id}/ (actualizar parcial)
# - DELETE /usuarios/{id}/ (eliminar)
router = DefaultRouter()
# Registramos nuestro ViewSet con el router.
# 'r'usuarios' será la URL base: /api/admin/usuarios/
# 'AdminUsuarioViewSet' es la vista que manejará las peticiones
# 'basename' es un identificador único para este conjunto de rutas
router.register(r'usuarios', AdminUsuarioViewSet, basename='admin-usuarios')

# La lista urlpatterns es la que Django usa para enrutar las peticiones.
# Incluimos todas las URLs que generó el router.
# Esto significa que si en el futuro queremos añadir más rutas personalizadas
# (que no sean CRUD), las añadiríamos aquí, fuera del include.
urlpatterns = [
    path('', include(router.urls)),
]