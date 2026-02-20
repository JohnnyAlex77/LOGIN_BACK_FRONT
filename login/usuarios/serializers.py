from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import Usuario, Rol

class RolSerializer(serializers.ModelSerializer):
    """
    Serializador básico para el modelo Rol
    """
    class Meta:
        model = Rol
        fields = ['id', 'name', 'descripcion']


class UsuarioSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Usuario
    Incluye información del rol anidada y campo para escritura
    """
    rol_usuario = RolSerializer(read_only=True)
    rol_id = serializers.PrimaryKeyRelatedField(
        queryset=Rol.objects.all(),
        source='rol_usuario',
        write_only=True,
        required=True
    )
    
    class Meta:
        model = Usuario
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'telefono', 'fecha_nacimiento', 'fecha_contrato',
            'rol_usuario', 'rol_id', 'is_active', 'date_joined',
            'last_login'
        ]
        read_only_fields = ['id', 'date_joined', 'last_login']


class LoginSerializer(serializers.Serializer):
    """
    Serializador para el login
    Acepta username O email en el mismo campo
    """
    username_email = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate(self, data):
        username_email = data.get('username_email')
        password = data.get('password')

        if username_email and password:
            # Intentar autenticar como username
            user = authenticate(
                request=self.context.get('request'),
                username=username_email,
                password=password
            )
            
            # Si falla, probar como email
            if not user:
                try:
                    user_obj = Usuario.objects.get(email=username_email)
                    user = authenticate(
                        request=self.context.get('request'),
                        username=user_obj.username,
                        password=password
                    )
                except Usuario.DoesNotExist:
                    pass

            if not user:
                raise serializers.ValidationError(
                    "Credenciales inválidas. Verifica tu usuario/email y contraseña."
                )
            
            if not user.is_active:
                raise serializers.ValidationError("Usuario inactivo.")

            data['user'] = user
        else:
            raise serializers.ValidationError(
                "Debe proporcionar username/email y contraseña."
            )

        return data


class TokenResponseSerializer(serializers.Serializer):
    """
    Serializador para la respuesta del login
    """
    access = serializers.CharField()
    refresh = serializers.CharField()
    user = UsuarioSerializer()