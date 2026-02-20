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

logger = logging.getLogger(__name__)
User = get_user_model()

class AdminUsuarioViewSet(viewsets.ViewSet):
    """
    ViewSet para administración completa de usuarios.
    Solo accesible para usuarios con rol Admin.
    """
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Obtener queryset base con optimización"""
        return User.objects.all().select_related('rol_usuario').order_by('-date_joined')

    @rol_obligatorio(roles_permitidos=["Admin"])
    def list(self, request):
        """
        Listar todos los usuarios con filtros opcionales.
        GET /api/admin/usuarios/?search=...&rol=...&activo=...
        """
        queryset = self.get_queryset()
        
        # Filtros
        search = request.query_params.get('search', '')
        rol = request.query_params.get('rol', '')
        activo = request.query_params.get('activo', '')
        
        if search:
            queryset = queryset.filter(
                Q(username__icontains=search) |
                Q(email__icontains=search) |
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search)
            )
        
        if rol:
            queryset = queryset.filter(rol_usuario__id=rol)
        
        if activo.lower() in ['true', 'false']:
            is_active = activo.lower() == 'true'
            queryset = queryset.filter(is_active=is_active)
        
        serializer = UsuarioSerializer(queryset, many=True)
        
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
        # Validar que el rol existe
        rol_id = request.data.get('rol_id')
        if not rol_id:
            return Response(
                {'error': 'El rol es requerido'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            rol = Rol.objects.get(id=rol_id)
        except Rol.DoesNotExist:
            return Response(
                {'error': 'Rol no válido'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Crear usuario
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Establecer contraseña
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
            if user.id == request.user.id and request.data.get('rol_id'):
                # Permitir cambios pero con precaución
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
            
            # Evitar que un admin se elimine a sí mismo
            if user.id == request.user.id:
                return Response(
                    {'error': 'No puedes eliminarte a ti mismo'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            username = user.username
            user.delete()
            
            logger.info(f"Admin {request.user.username} eliminó usuario: {username}")
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
        """
        try:
            user = self.get_queryset().get(pk=pk)
            
            # Evitar que un admin se desactive a sí mismo
            if user.id == request.user.id:
                return Response(
                    {'error': 'No puedes desactivarte a ti mismo'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
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
        """
        roles = Rol.objects.all().values('id', 'name', 'descripcion')
        return Response(list(roles))