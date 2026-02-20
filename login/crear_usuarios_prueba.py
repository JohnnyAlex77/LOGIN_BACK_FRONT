# crear_usuarios_prueba.py
import os
import django

# Configurar el entorno de Django para poder usar los modelos
# Esto es necesario porque el script se ejecuta fuera del contexto del servidor
# Primero, indicamos qué archivo de settings debe usar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'login.settings')
# Luego, inicializamos Django para que cargue la configuración y los modelos
django.setup()

# Ahora que Django está configurado, podemos importar los modelos
from usuarios.models import Usuario, Rol

def crear_usuarios():
    """Crear un usuario de cada rol: Admin, Estudiante, Empresa"""
    
    print("=== INICIANDO CREACION DE USUARIOS ===\n")
    
    # Crear roles si no existen
    # Definimos los roles básicos del sistema
    roles_data = [
        {"name": "Admin", "descripcion": "Administrador del sistema"},
        {"name": "Estudiante", "descripcion": "Estudiante"},
        {"name": "Empresa", "descripcion": "Empresa"}
    ]
    
    # Diccionario para guardar los objetos Rol por su nombre
    roles = {}
    for rol_data in roles_data:
        # get_or_create es muy útil: intenta obtener el rol, si no existe lo crea
        # Devuelve (objeto, booleano) donde el booleano indica si se creó
        rol, created = Rol.objects.get_or_create(
            name=rol_data["name"],
            defaults={"descripcion": rol_data["descripcion"]}  # Solo se usa si se crea
        )
        roles[rol.name] = rol
        if created:
            print(f"  Rol creado: {rol.name}")
        else:
            print(f"  Rol existente: {rol.name}")
    
    # Eliminar usuarios sin rol (si existen)
    # Esta es una limpieza preventiva. Como el modelo permite null=True en rol_usuario,
    # pueden haber quedado usuarios sin rol de ejecuciones anteriores o errores.
    usuarios_sin_rol = Usuario.objects.filter(rol_usuario__isnull=True)
    if usuarios_sin_rol.exists():
        print(f"\n  Eliminando {usuarios_sin_rol.count()} usuario(s) sin rol...")
        usuarios_sin_rol.delete()
    
    # Datos de los usuarios a crear
    # Separamos admin del resto porque usa create_superuser en lugar de create_user
    usuarios_data = [
        {
            "username": "admin",
            "email": "admin@test.com",
            "password": "admin123",
            "first_name": "Admin",
            "last_name": "Principal",
            "rol": roles["Admin"],
            "is_superuser": True,  # Flag para identificar al admin
            "is_staff": True        # Necesario para acceder al panel de admin de Django
        },
        {
            "username": "estudiante1",
            "email": "estudiante@test.com",
            "password": "estudiante123",
            "first_name": "Estudiante",
            "last_name": "Uno",
            "rol": roles["Estudiante"]
        },
        {
            "username": "empresa1",
            "email": "empresa@test.com",
            "password": "empresa123",
            "first_name": "Empresa",
            "last_name": "Uno",
            "rol": roles["Empresa"]
        }
    ]
    
    # Listas para llevar el conteo de lo que se hizo
    usuarios_creados = []
    usuarios_existentes = []
    
    # Crear usuarios
    for data in usuarios_data:
        # Verificar si el usuario ya existe por username
        if not Usuario.objects.filter(username=data["username"]).exists():
            # Si tiene el flag is_superuser, usamos create_superuser
            # create_superuser es un método especial de Django que además de crear el usuario,
            # le da permisos de superusuario y staff, y hashea la contraseña correctamente
            if data.get("is_superuser"):
                usuario = Usuario.objects.create_superuser(
                    username=data["username"],
                    email=data["email"],
                    password=data["password"],
                    first_name=data["first_name"],
                    last_name=data["last_name"],
                    rol_usuario=data["rol"]  # Nuestro campo personalizado
                )
            else:
                # Para usuarios normales, usamos create_user (también hashea la password)
                usuario = Usuario.objects.create_user(
                    username=data["username"],
                    email=data["email"],
                    password=data["password"],
                    first_name=data["first_name"],
                    last_name=data["last_name"],
                    rol_usuario=data["rol"]
                )
            usuarios_creados.append(f"{data['username']} ({data['rol'].name})")
        else:
            # Si el usuario ya existe, actualizamos su rol por si acaso
            # Esto es útil cuando el script se ejecuta múltiples veces y los roles
            # han cambiado o el usuario estaba con rol incorrecto
            usuario = Usuario.objects.get(username=data["username"])
            if usuario.rol_usuario != data["rol"]:
                usuario.rol_usuario = data["rol"]
                usuario.save()
                print(f"  Rol actualizado: {data['username']} -> {data['rol'].name}")
            usuarios_existentes.append(f"{data['username']} ({data['rol'].name})")
    
    # Mostrar resultados
    print("\n=== RESULTADO ===")
    if usuarios_creados:
        print("  Usuarios creados:")
        for u in usuarios_creados:
            print(f"     - {u}")
    
    if usuarios_existentes:
        print("  Usuarios ya existentes:")
        for u in usuarios_existentes:
            print(f"     - {u}")
    
    # Mostrar todos los usuarios actuales para verificar el estado final
    print("\n=== USUARIOS EN SISTEMA ===")
    usuarios = Usuario.objects.all().order_by('rol_usuario__name')
    for u in usuarios:
        rol = u.rol_usuario.name if u.rol_usuario else "SIN ROL"
        superuser = "[ADMIN]" if u.is_superuser else "      "
        print(f"  {superuser} {u.username:15} | {u.email:25} | {rol}")

# Este bloque asegura que el script solo se ejecute si se llama directamente
# (no si se importa desde otro archivo)
if __name__ == "__main__":
    crear_usuarios()