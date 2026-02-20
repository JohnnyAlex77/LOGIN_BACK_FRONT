from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from usuarios.decorators import rol_obligatorio
import logging

# Configuramos el logger para auditoría y depuración.
logger = logging.getLogger(__name__)


class EmpresaDashboardView(APIView):
    """
    Vista de ejemplo para el dashboard de empresas.
    Solo accesible para usuarios con rol 'Empresa' o 'Admin'.
    """
    # El decorador @rol_obligatorio es personalizado y verifica que el usuario
    # autenticado tenga uno de los roles especificados en la lista.
    # Aquí permitimos tanto a 'Empresa' como a 'Admin'. Esto es útil porque
    # quizás un admin necesita ver el dashboard de una empresa para depurar o asistir.
    @rol_obligatorio(roles_permitidos=["Empresa", "Admin"])
    def get(self, request):
        """
        Retorna información básica del dashboard de la empresa.
        Por ahora son datos de ejemplo (mock), pero en el futuro vendrán de la BD.
        """
        data = {
            "mensaje": "Bienvenido al dashboard de empresa",
            "usuario": {
                "username": request.user.username,
                "nombre": f"{request.user.first_name} {request.user.last_name}",
                "email": request.user.email,
                "rol": request.user.rol_usuario.name
            },
            "estadisticas": {
                "ofertas_activas": 5,
                "postulaciones_recibidas": 23,
                "entrevistas_pendientes": 4
            },
            "ofertas_recientes": [
                {"titulo": "Desarrollador Django", "postulaciones": 8},
                {"titulo": "Frontend React", "postulaciones": 12}
            ]
        }
        logger.info(f"Acceso a dashboard empresa: {request.user.username}")
        return Response(data, status=status.HTTP_200_OK)


class OfertasEmpresaView(APIView):
    """
    Vista para gestionar ofertas de la empresa.
    """
    
    @rol_obligatorio(roles_permitidos=["Empresa", "Admin"])
    def get(self, request):
        """Listar ofertas (datos simulados por ahora)"""
        # Simulación de datos. Esto es un placeholder hasta que tengamos el modelo Oferta.
        ofertas = [
            {"id": 1, "titulo": "Desarrollador Django", "estado": "activa"},
            {"id": 2, "titulo": "Frontend React", "estado": "activa"},
            {"id": 3, "titulo": "DevOps", "estado": "cerrada"}
        ]
        return Response(ofertas, status=status.HTTP_200_OK)
    
    @rol_obligatorio(roles_permitidos=["Empresa", "Admin"])
    def post(self, request):
        """Crear nueva oferta"""
        # Aquí iría la lógica para crear oferta, validar datos, guardar en BD, etc.
        return Response(
            {"mensaje": "Oferta creada exitosamente"},
            status=status.HTTP_201_CREATED
        )