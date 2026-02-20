from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class Rol(models.Model):
    """
    Modelo que representa los roles del sistema.
    Se relaciona con Usuario mediante una ForeignKey.
    """
    # name: nombre único del rol (Admin, Estudiante, Empresa)
    name = models.CharField(
        max_length=50, 
        unique=True, 
        verbose_name="Nombre del Rol"
    )
    descripcion = models.TextField(
        blank=True, 
        null=True, 
        verbose_name="Descripción"
    )

    def __str__(self):
        return self.name
    
    class Meta:
        # Nombre de la tabla en la base de datos (plural)
        db_table = 'roles'
        verbose_name = "Rol"
        verbose_name_plural = "Roles"


class Usuario(AbstractUser):
    """
    Modelo personalizado de usuario.
    Hereda de AbstractUser para mantener los campos por defecto
    (username, password, email, first_name, last_name, etc.)
    """
    # Campos adicionales
    telefono = models.CharField(
        max_length=15, 
        blank=True, 
        null=True,
        verbose_name="Teléfono"
    )
    fecha_nacimiento = models.DateField(
        blank=True, 
        null=True,
        verbose_name="Fecha de Nacimiento"
    )
    fecha_contrato = models.DateField(
        blank=True, 
        null=True,
        verbose_name="Fecha de Contrato"
    )

    # Relación con el modelo Rol
    # on_delete=models.PROTECT: evita eliminar un rol si hay usuarios asociados
    rol_usuario = models.ForeignKey(
        Rol, 
        on_delete=models.PROTECT,
        null=True,  # No permite usuarios sin rol
        blank=False,
        verbose_name="Rol"
    )

    class Meta:
        db_table = 'usuarios'
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def __str__(self):
        return f"{self.username} - {self.rol_usuario.name if self.rol_usuario else 'Sin rol'}"