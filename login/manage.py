#!/usr/bin/env python
# Shebang: indica al sistema operativo (en entornos Unix/Linux) que este script
# debe ejecutarse con el intérprete de Python. Útil si se hace el archivo ejecutable
# directamente (./manage.py en lugar de python manage.py)

"""Django's command-line utility for administrative tasks."""
# Docstring del módulo: describe brevemente qué hace este archivo

import os
import sys

# Importamos módulos estándar de Python:
# os: para interactuar con variables de entorno y el sistema operativo
# sys: para acceder a argumentos de línea de comandos y funciones del sistema


def main():
    """Run administrative tasks."""
    # Esta función es el corazón del script
    
    # Configurar la variable de entorno DJANGO_SETTINGS_MODULE
    # setdefault solo asigna el valor si la variable NO existe
    # Esto le dice a Django qué archivo de configuración debe usar
    # En nuestro caso, busca 'login.settings' (el archivo login/login/settings.py)
    # Es importante porque Django necesita saber dónde está la configuración
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'login.settings')
    
    try:
        # Intentamos importar la función execute_from_command_line de Django
        # Este import se hace dentro del try por dos razones:
        # 1. Para capturar el error si Django no está instalado
        # 2. Porque no necesitamos importarlo hasta que realmente se vaya a usar
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # Si falla la importación, Django no está instalado o no está en el entorno
        # Lanzamos un ImportError con un mensaje amigable que ayuda al desarrollador
        # a diagnosticar el problema (entorno virtual, instalación, etc.)
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    # Ejecutar el comando de Django
    # sys.argv contiene los argumentos de línea de comandos
    # Por ejemplo, si ejecutamos 'python manage.py runserver 8000'
    # sys.argv = ['manage.py', 'runserver', '8000']
    # execute_from_command_line procesa estos argumentos y llama al comando adecuado
    execute_from_command_line(sys.argv)


# Este bloque condicional es estándar en Python
# Solo ejecuta main() si el script se ejecuta directamente
# Si este archivo fuera importado desde otro, no se ejecutaría automáticamente
if __name__ == '__main__':
    main()