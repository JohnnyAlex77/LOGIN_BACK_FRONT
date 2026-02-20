from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from usuarios.decorators import rol_obligatorio
from usuarios.models import Usuario
from usuarios.serializers import UsuarioSerializer
import logging

logger = logging.getLogger(__name__)


class EstudianteDashboardView(APIView):
    """
    Vista de ejemplo para el dashboard de estudiantes.
    Solo accesible para usuarios con rol 'Estudiante' o 'Admin'.
    """
    
    @rol_obligatorio(roles_permitidos=["Estudiante", "Admin"])
    def get(self, request):
        """
        Retorna información básica del dashboard del estudiante.
        Datos mock por ahora.
        """
        data = {
            "mensaje": "Bienvenido al dashboard de estudiante",
            "usuario": {
                "username": request.user.username,
                "nombre": f"{request.user.first_name} {request.user.last_name}",
                "email": request.user.email,
                "rol": request.user.rol_usuario.name
            },
            "estadisticas": {
                "cursos_inscritos": 3,
                "tareas_pendientes": 2,
                "promedio_notas": 4.5
            },
            "actividad_reciente": [
                {"fecha": "2025-02-18", "descripcion": "Inscrito en Matemáticas"},
                {"fecha": "2025-02-17", "descripcion": "Entregó tarea de Física"}
            ]
        }
        logger.info(f"Acceso a dashboard estudiante: {request.user.username}")
        return Response(data, status=status.HTTP_200_OK)


class PerfilEstudianteView(APIView):
    """
    Vista para ver/editar perfil de estudiante.
    A diferencia del dashboard, esta vista ya interactúa con datos reales del usuario.
    """
    
    @rol_obligatorio(roles_permitidos=["Estudiante", "Admin"])
    def get(self, request):
        """Obtener perfil del estudiante (datos reales del usuario autenticado)"""
        serializer = UsuarioSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @rol_obligatorio(roles_permitidos=["Estudiante", "Admin"])
    def patch(self, request):
        """
        Actualizar perfil parcialmente.
        Usamos PATCH porque permite enviar solo los campos que se quieren modificar.
        """
        serializer = UsuarioSerializer(
            request.user, 
            data=request.data, 
            partial=True  # partial=True indica que no todos los campos son obligatorios
        )
        if serializer.is_valid():
            serializer.save()
            logger.info(f"Perfil actualizado: {request.user.username}")
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)