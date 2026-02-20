from django.apps import AppConfig

# Configuración de la aplicación 'estudiantes'.
class EstudiantesConfig(AppConfig):
    # Importante: el nombre debe coincidir con la carpeta.
    # Un error común es poner 'estudiante' (singular) cuando la carpeta es 'estudiantes' (plural).
    name = 'estudiantes'