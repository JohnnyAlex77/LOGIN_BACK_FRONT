from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AdminUsuarioViewSet

router = DefaultRouter()
router.register(r'usuarios', AdminUsuarioViewSet, basename='admin-usuarios')

urlpatterns = [
    path('', include(router.urls)),
]