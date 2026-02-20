from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class Rol(models.Model):
    """
    Modelo que representa los roles del sistema.
    Se relaciona con Usuario mediante una ForeignKey.
    """
    # name: nombre único del rol (Admin, Estudiante, Empresa)
    # Lo hacemos único para evitar duplicados y poder referenciarlo de forma fiable desde el código.
    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Nombre del Rol"
    )
    # Un campo de texto para describir el rol, no es obligatorio. Puede ser útil para mostrarlo en un tooltip en el frontend.
    descripcion = models.TextField(
        blank=True,
        null=True,
        verbose_name="Descripción"
    )

    def __str__(self):
        # Esta representación en texto es la que se verá en el panel de admin de Django y en los logs.
        # Es mucho más legible que mostrar "Rol object (1)".
        return self.name

    class Meta:
        # Personalizamos el nombre de la tabla en la BD y los nombres visibles en el admin.
        # Esto es una buena práctica para mantener la base de datos ordenada.
        db_table = 'roles'
        verbose_name = "Rol"
        verbose_name_plural = "Roles"


class Usuario(AbstractUser):
    """
    Modelo personalizado de usuario.
    Hereda de AbstractUser para mantener los campos por defecto
    (username, password, email, first_name, last_name, etc.)
    La razón principal para extender AbstractUser en lugar de usar el modelo por defecto es
    que necesitamos añadir campos personalizados (teléfono, rol, etc.) y tener un modelo
    de usuario que podamos modificar a futuro si el proyecto crece.
    """
    # Campos adicionales que no vienen en el AbstractUser por defecto.
    # Los hacemos opcionales (blank=True, null=True) para no complicar el registro inicial.
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
    # on_delete=models.PROTECT: Esta es una decisión clave de integridad de datos.
    # Con PROTECT, Django impedirá que se borre un rol (ej. "Admin") si hay usuarios que aún lo tienen asignado.
    # Esto evita que el sistema se quede sin admins o que los usuarios queden con un rol huérfano.
    # null=True está mal aquí (según el comentario dice "No permite usuarios sin rol", pero null=True SÍ lo permite).
    # Si no se debe permitir usuario sin rol, debería ser null=False (que es el valor por defecto).
    # El comentario es correcto en la intención, pero el código actual permite que un usuario no tenga rol, lo cual es un riesgo.
    rol_usuario = models.ForeignKey(
        Rol,
        on_delete=models.PROTECT,
        null=True,  # <<--- ¡OJO! Esto permite usuarios sin rol. El comentario dice que no debería.
        blank=False, # blank=False solo afecta formularios, no la BD.
        verbose_name="Rol"
    )

    class Meta:
        db_table = 'usuarios'
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def __str__(self):
        # En la representación incluimos el rol si existe, si no, lo indicamos.
        # Así es fácil identificar usuarios problemáticos sin rol.
        return f"{self.username} - {self.rol_usuario.name if self.rol_usuario else 'Sin rol'}"