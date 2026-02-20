from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from django.db.models import Q
from usuarios.decorators import rol_obligatorio
from usuarios.serializers import UsuarioSerializer
from usuarios.models import Rol
import logging

# Configuramos un logger para este módulo. Esto nos permite registrar eventos
# (como creación, eliminación de usuarios) para auditoría o depuración.
# Es mucho mejor que usar print() porque se puede configurar su nivel (INFO, ERROR, etc.)
# y hacia dónde se envía (consola, archivo, etc.)
logger = logging.getLogger(__name__)
# Obtenemos el modelo de usuario personalizado que definimos en usuarios.models
User = get_user_model()

class AdminUsuarioViewSet(viewsets.ViewSet):
    """
    ViewSet para administración completa de usuarios.
    Solo accesible para usuarios con rol Admin.
    """
    # A nivel de clase, definimos que todas las acciones de este ViewSet requieren
    # que el usuario esté autenticado. Luego, con nuestro decorador personalizado
    # @rol_obligatorio, refinaremos el acceso a nivel de método para asegurar que
    # solo los admins puedan ejecutarlas.
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Obtener queryset base con optimización
        """
        # select_related es una optimización de base de datos. Como Usuario tiene
        # una ForeignKey a Rol, cada vez que accedamos a user.rol_usuario, Django haría
        # una consulta adicional. Con select_related, hacemos un JOIN y traemos todos
        # los datos en una sola consulta. Es una buena práctica cuando sabes que vas a
        # necesitar los datos relacionados.
        return User.objects.all().select_related('rol_usuario').order_by('-date_joined')

    @rol_obligatorio(roles_permitidos=["Admin"])
    def list(self, request):
        """
        Listar todos los usuarios con filtros opcionales.
        GET /api/admin/usuarios/?search=...&rol=...&activo=...
        """
        queryset = self.get_queryset()

        # Filtros: obtenemos los parámetros de la query string (lo que va después del ? en la URL)
        search = request.query_params.get('search', '')
        rol = request.query_params.get('rol', '')
        activo = request.query_params.get('activo', '')

        # Filtro de búsqueda textual. Usamos Q objects para poder hacer OR.
        # icontains hace una búsqueda case-insensitive (no distingue mayúsculas).
        if search:
            queryset = queryset.filter(
                Q(username__icontains=search) |
                Q(email__icontains=search) |
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search)
            )

        # Filtro por rol (asumimos que 'rol' es el ID del rol)
        if rol:
            queryset = queryset.filter(rol_usuario__id=rol)

        # Filtro por estado activo/inactivo.
        # Convertimos el string a booleano de forma segura.
        if activo.lower() in ['true', 'false']:
            is_active = activo.lower() == 'true'
            queryset = queryset.filter(is_active=is_active)

        # Serializamos el queryset (convertimos objetos Python a JSON) y devolvemos la respuesta.
        serializer = UsuarioSerializer(queryset, many=True)

        # Registramos la acción para auditoría.
        logger.info(f"Admin {request.user.username} listó usuarios")
        return Response({
            'count': queryset.count(),
            'results': serializer.data
        })

    @rol_obligatorio(roles_permitidos=["Admin"])
    def create(self, request):
        """
        Crear nuevo usuario.
        POST /api/admin/usuarios/
        """
        # Validar que el rol existe. El rol se envía como 'rol_id' en el cuerpo de la petición.
        rol_id = request.data.get('rol_id')
        if not rol_id:
            return Response(
                {'error': 'El rol es requerido'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Intentamos obtener el rol. Si no existe, la excepción se captura.
            rol = Rol.objects.get(id=rol_id)
        except Rol.DoesNotExist:
            return Response(
                {'error': 'Rol no válido'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Crear usuario. Usamos el serializer para validar los datos.
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            # Guardamos el usuario (sin contraseña aún, porque el serializer no la maneja directamente)
            user = serializer.save()

            # Establecer contraseña. Como usamos set_password, la contraseña se hashea.
            password = request.data.get('password')
            if password:
                user.set_password(password)
                user.save()

            logger.info(f"Admin {request.user.username} creó usuario: {user.username}")
            return Response(
                UsuarioSerializer(user).data,
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @rol_obligatorio(roles_permitidos=["Admin"])
    def retrieve(self, request, pk=None):
        """
        Obtener detalle de un usuario específico.
        GET /api/admin/usuarios/{id}/
        """
        try:
            user = self.get_queryset().get(pk=pk)
            serializer = UsuarioSerializer(user)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response(
                {'error': 'Usuario no encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )

    @rol_obligatorio(roles_permitidos=["Admin"])
    def update(self, request, pk=None):
        """
        Actualizar usuario completo.
        PUT /api/admin/usuarios/{id}/
        """
        try:
            user = self.get_queryset().get(pk=pk)

            # Verificar que no se está intentando modificar el propio admin
            # Esto es una medida de seguridad: permitimos que un admin se modifique a sí mismo,
            # pero lo registramos con un warning por si es un intento de auto-sabotaje.
            if user.id == request.user.id and request.data.get('rol_id'):
                logger.warning(f"Admin {request.user.username} se está modificando a sí mismo")

            serializer = UsuarioSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()

                # Actualizar contraseña si se proporciona
                password = request.data.get('password')
                if password:
                    user.set_password(password)
                    user.save()

                logger.info(f"Admin {request.user.username} actualizó usuario: {user.username}")
                return Response(serializer.data)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            return Response(
                {'error': 'Usuario no encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )

    @rol_obligatorio(roles_permitidos=["Admin"])
    def partial_update(self, request, pk=None):
        """
        Actualización parcial de usuario.
        PATCH /api/admin/usuarios/{id}/
        """
        try:
            user = self.get_queryset().get(pk=pk)

            serializer = UsuarioSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()

                # Actualizar contraseña si se proporciona
                password = request.data.get('password')
                if password:
                    user.set_password(password)
                    user.save()

                logger.info(f"Admin {request.user.username} actualizó parcialmente usuario: {user.username}")
                return Response(serializer.data)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            return Response(
                {'error': 'Usuario no encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )

    @rol_obligatorio(roles_permitidos=["Admin"])
    def destroy(self, request, pk=None):
        """
        Eliminar usuario.
        DELETE /api/admin/usuarios/{id}/
        """
        try:
            user = self.get_queryset().get(pk=pk)

            # Evitar que un admin se elimine a sí mismo. Esta es una protección crítica.
            # Si un admin pudiera eliminarse a sí mismo, podríamos quedar sin administradores
            # en el sistema, lo que sería un problema.
            if user.id == request.user.id:
                return Response(
                    {'error': 'No puedes eliminarte a ti mismo'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            username = user.username
            user.delete()

            logger.info(f"Admin {request.user.username} eliminó usuario: {username}")
            # 204 No Content es la respuesta estándar para DELETE exitoso.
            return Response(status=status.HTTP_204_NO_CONTENT)

        except User.DoesNotExist:
            return Response(
                {'error': 'Usuario no encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=['post'], url_path='toggle-activo')
    @rol_obligatorio(roles_permitidos=["Admin"])
    def toggle_active(self, request, pk=None):
        """
        Activar/desactivar usuario.
        POST /api/admin/usuarios/{id}/toggle-activo/
        El decorador @action nos permite añadir rutas personalizadas a un ViewSet.
        - detail=True: significa que la acción se aplica a un objeto específico (requiere un ID).
        - methods: los métodos HTTP permitidos (POST aquí).
        - url_path: la parte final de la URL (toggle-activo).
        """
        try:
            user = self.get_queryset().get(pk=pk)

            # Evitar que un admin se desactive a sí mismo. Igual que con eliminación,
            # es una protección para no perder el acceso al sistema.
            if user.id == request.user.id:
                return Response(
                    {'error': 'No puedes desactivarte a ti mismo'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Invertir el estado activo.
            user.is_active = not user.is_active
            user.save()

            estado = 'activado' if user.is_active else 'desactivado'
            logger.info(f"Admin {request.user.username} {estado} usuario: {user.username}")

            return Response({
                'is_active': user.is_active,
                'message': f'Usuario {estado} correctamente'
            })

        except User.DoesNotExist:
            return Response(
                {'error': 'Usuario no encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=['get'], url_path='roles')
    @rol_obligatorio(roles_permitidos=["Admin"])
    def list_roles(self, request):
        """
        Listar todos los roles disponibles.
        GET /api/admin/usuarios/roles/
        Este es un endpoint de utilidad para que el frontend pueda mostrar
        un select con los roles al crear/editar usuarios.
        """
        roles = Rol.objects.all().values('id', 'name', 'descripcion')
        return Response(list(roles))