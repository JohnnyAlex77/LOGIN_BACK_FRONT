from django.apps import AppConfig

# Esta clase configura la aplicación 'admin' de Django.
# Es necesaria para que Django reconozca esta carpeta como una aplicación.
class AdminConfig(AppConfig):
    # 'name' le dice a Django cuál es el nombre de la aplicación.
    # Este nombre se usa internamente para referenciar la app, por ejemplo,
    # en INSTALLED_APPS del settings.py. Al poner 'admin', Django buscará
    # los modelos, vistas, etc. dentro de esta carpeta.
    name = 'admin'