from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from django.contrib.auth import login
from .serializers import LoginSerializer, UsuarioSerializer, TokenResponseSerializer
from .models import Usuario
import logging

logger = logging.getLogger(__name__)


class LoginView(APIView):
    """
    Vista para autenticar usuarios.
    Acepta username/email + password y retorna tokens JWT + datos del usuario.
    Permite acceso sin autenticación (AllowAny).
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(
            data=request.data, 
            context={'request': request}
        )
        
        if serializer.is_valid():
            user = serializer.validated_data['user']
            
            # Generar tokens JWT
            refresh = RefreshToken.for_user(user)
            
            # Datos de respuesta
            response_data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UsuarioSerializer(user).data
            }
            
            # Opcional: Crear sesión en Django (si se necesita para admin)
            login(request, user)
            
            logger.info(f"Login exitoso: {user.username} ({user.rol_usuario.name})")
            
            return Response(response_data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """
    Vista para cerrar sesión.
    Invalida el refresh token (lo agrega a lista negra).
    Requiere autenticación.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()  # Requiere activar blacklist en settings
                logger.info(f"Logout exitoso: {request.user.username}")
                return Response(
                    {"message": "Sesión cerrada correctamente"},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"error": "Se requiere refresh token"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            logger.error(f"Error en logout: {str(e)}")
            return Response(
                {"error": "Error al cerrar sesión"},
                status=status.HTTP_400_BAD_REQUEST
            )


class CurrentUserView(APIView):
    """
    Vista para obtener los datos del usuario actual.
    Requiere autenticación.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UsuarioSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)