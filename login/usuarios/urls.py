from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import LoginView, LogoutView, CurrentUserView

# Namespace para URLs de usuarios.
app_name = 'usuarios'

urlpatterns = [
    # Autenticación
    # POST /api/auth/login/ - Iniciar sesión
    path('auth/login/', LoginView.as_view(), name='login'),
    # POST /api/auth/logout/ - Cerrar sesión (requiere refresh token)
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    # POST /api/auth/refresh/ - Obtener nuevo access token usando refresh token
    # Esta vista ya viene incluida en simplejwt, no tuvimos que crearla.
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # GET /api/auth/me/ - Obtener datos del usuario autenticado
    path('auth/me/', CurrentUserView.as_view(), name='current_user'),
]