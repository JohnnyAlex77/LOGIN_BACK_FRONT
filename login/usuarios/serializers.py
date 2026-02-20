from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import Usuario, Rol

class RolSerializer(serializers.ModelSerializer):
    """
    Serializador básico para el modelo Rol
    ModelSerializer es una clase de DRF que automáticamente genera campos
    basándose en el modelo. Nos ahorra tener que definir campo por campo.
    """
    class Meta:
        model = Rol
        # Solo exponemos estos campos del rol. No incluimos, por ejemplo,
        # fechas de creación porque no existen en el modelo.
        fields = ['id', 'name', 'descripcion']


class UsuarioSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Usuario
    Incluye información del rol anidada y campo para escritura
    """
    # Este campo es de solo lectura y devuelve el objeto Rol completo serializado.
    # Cuando el frontend pida un usuario, en lugar de recibir solo un ID de rol,
    # recibirá algo como: "rol_usuario": {"id": 2, "name": "Estudiante", "descripcion": "..."}
    # Esto ahorra peticiones adicionales al frontend.
    rol_usuario = RolSerializer(read_only=True)
    
    # Este campo es de solo escritura. El frontend enviará 'rol_id' con el ID del rol.
    # Usamos PrimaryKeyRelatedField porque la relación es una ForeignKey.
    # El parámetro 'source' es clave: le dice a DRF que este campo corresponde al
    # atributo 'rol_usuario' del modelo. Así, cuando el frontend envía rol_id=2,
    # DRF asigna el objeto Rol con id=2 a usuario.rol_usuario.
    # required=True obliga a que siempre se envíe un rol al crear/actualizar.
    rol_id = serializers.PrimaryKeyRelatedField(
        queryset=Rol.objects.all(),  # Valida que el ID exista en la BD
        source='rol_usuario',         # Mapea al campo del modelo
        write_only=True,              # Solo para entrada, no para salida
        required=True
    )
    
    class Meta:
        model = Usuario
        # Lista completa de campos que expone el serializador.
        # Incluye campos del modelo original (username, email, etc.) y
        # los campos personalizados (rol_usuario, rol_id).
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'telefono', 'fecha_nacimiento', 'fecha_contrato',
            'rol_usuario', 'rol_id', 'is_active', 'date_joined',
            'last_login'
        ]
        # read_only_fields: campos que solo se devuelven, no se pueden modificar.
        # id es autoincremental, date_joined lo pone Django al crear, last_login lo gestiona JWT.
        read_only_fields = ['id', 'date_joined', 'last_login']


class LoginSerializer(serializers.Serializer):
    """
    Serializador para el login
    Acepta username O email en el mismo campo
    
    Nota: Este es un Serializer, no un ModelSerializer, porque no corresponde
    directamente a un modelo. Es para datos de entrada personalizados.
    """
    # write_only=True porque estos campos solo se envían, no se devuelven.
    username_email = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate(self, data):
        """
        Validación personalizada a nivel de objeto.
        Este método se llama después de validar campos individuales.
        Aquí es donde hacemos la lógica de autenticación.
        """
        username_email = data.get('username_email')
        password = data.get('password')

        if username_email and password:
            # Intentar autenticar como username
            # authenticate() es la función de Django que verifica credenciales
            user = authenticate(
                request=self.context.get('request'),  # Pasamos el request por si hay middlewares
                username=username_email,
                password=password
            )
            
            # Si falla como username, probar como email
            if not user:
                try:
                    # Buscar un usuario con ese email
                    user_obj = Usuario.objects.get(email=username_email)
                    # Si existe, intentar autenticar con su username y la password dada
                    user = authenticate(
                        request=self.context.get('request'),
                        username=user_obj.username,
                        password=password
                    )
                except Usuario.DoesNotExist:
                    # Si no hay usuario con ese email, simplemente ignoramos
                    # El usuario ya es None, y lanzaremos error después
                    pass

            # Si después de ambos intentos no hay usuario, credenciales inválidas
            if not user:
                raise serializers.ValidationError(
                    "Credenciales inválidas. Verifica tu usuario/email y contraseña."
                )
            
            # Verificar que el usuario esté activo
            if not user.is_active:
                raise serializers.ValidationError("Usuario inactivo.")

            # Si todo OK, añadimos el usuario a los datos validados
            # Esto estará disponible en serializer.validated_data['user']
            data['user'] = user
        else:
            # Si falta alguno de los campos
            raise serializers.ValidationError(
                "Debe proporcionar username/email y contraseña."
            )

        return data


class TokenResponseSerializer(serializers.Serializer):
    """
    Serializador para la respuesta del login
    No valida entrada, solo define la estructura de salida.
    Útil para documentación y para asegurar que siempre devolvemos lo mismo.
    """
    access = serializers.CharField()
    refresh = serializers.CharField()
    user = UsuarioSerializer()  # Anidamos el serializador de usuario