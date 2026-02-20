from django.apps import AppConfig

# Configuración de la aplicación 'empresas'.
# Este archivo es necesario para que Django reconozca esta carpeta como una aplicación.
class EmpresasConfig(AppConfig):
    # El nombre de la aplicación. Django lo usa internamente para referenciarla.
    # Debe coincidir con el nombre de la carpeta donde reside esta app.
    name = 'empresas'