from functools import wraps
from rest_framework.response import Response
from rest_framework import status
from django.contrib import messages
import logging

logger = logging.getLogger(__name__)

# Este decorador está diseñado específicamente para vistas basadas en clase de DRF.
# Notar que la función wrapper recibe 'self' (la instancia de la vista) y 'request'.
def rol_obligatorio(roles_permitidos=None):
    """
    Decorador para restringir acceso basado en roles.
    Funciona con vistas de DRF (APIView, ViewSet, etc.)
    
    Uso:
        @rol_obligatorio(roles_permitidos=["Admin", "Estudiante"])
        def get(self, request):
            ...
    
    Args:
        roles_permitidos: Lista de nombres de roles que pueden acceder.
    
    Returns:
        Response con error 403 si no tiene permisos,
        o ejecuta la vista si tiene el rol adecuado.
    """
    if roles_permitidos is None:
        roles_permitidos = []

    def decorator(view_func):
        @wraps(view_func)  # Mantiene los metadatos de la función original (nombre, docstring, etc.)
        def wrapper(self, request, *args, **kwargs):
            # Verificar si el usuario está autenticado
            if not request.user or not request.user.is_authenticated:
                logger.warning(f"Acceso denegado: usuario no autenticado")
                return Response(
                    {"error": "Debe iniciar sesión para acceder a este recurso"},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            # Verificar si el usuario tiene rol asignado
            # Esto es importante porque nuestro modelo permite usuarios sin rol (null=True)
            if not hasattr(request.user, 'rol_usuario') or not request.user.rol_usuario:
                logger.warning(f"Usuario {request.user.username} no tiene rol asignado")
                return Response(
                    {"error": "Usuario sin rol asignado. Contacte al administrador."},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            # Verificar si el rol del usuario está en la lista de permitidos
            rol_usuario = request.user.rol_usuario.name
            if rol_usuario not in roles_permitidos:
                logger.warning(
                    f"Usuario {request.user.username} con rol {rol_usuario} "
                    f"intentó acceder a recurso que requiere {roles_permitidos}"
                )
                return Response(
                    {
                        "error": "No tiene permisos suficientes para acceder a este recurso",
                        "required_roles": roles_permitidos,
                        "user_role": rol_usuario
                    },
                    status=status.HTTP_403_FORBIDDEN
                )
            
            # Todo OK, ejecutar la vista
            return view_func(self, request, *args, **kwargs)
        
        return wrapper
    return decorator


# Versión simplificada para usar en vistas basadas en función.
# No recibe 'self' porque no hay instancia de clase.
def rol_obligatorio_func(roles_permitidos=None):
    """
    Versión del decorador para vistas basadas en función.
    """
    if roles_permitidos is None:
        roles_permitidos = []

    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user or not request.user.is_authenticated:
                return Response(
                    {"error": "Debe iniciar sesión"},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            if not hasattr(request.user, 'rol_usuario') or not request.user.rol_usuario:
                return Response(
                    {"error": "Usuario sin rol asignado"},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            if request.user.rol_usuario.name not in roles_permitidos:
                return Response(
                    {"error": "No tiene permisos suficientes"},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            return view_func(request, *args, **kwargs)
        
        return wrapper
    return decorator