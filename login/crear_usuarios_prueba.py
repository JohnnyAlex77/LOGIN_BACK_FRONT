# crear_usuarios_prueba.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'login.settings')
django.setup()

from usuarios.models import Usuario, Rol

def crear_usuarios():
    """Crear un usuario de cada rol: Admin, Estudiante, Empresa"""
    
    print("=== INICIANDO CREACIÓN DE USUARIOS ===\n")
    
    # Crear roles si no existen
    roles_data = [
        {"name": "Admin", "descripcion": "Administrador del sistema"},
        {"name": "Estudiante", "descripcion": "Estudiante"},
        {"name": "Empresa", "descripcion": "Empresa"}
    ]
    
    roles = {}
    for rol_data in roles_data:
        rol, created = Rol.objects.get_or_create(
            name=rol_data["name"],
            defaults={"descripcion": rol_data["descripcion"]}
        )
        roles[rol.name] = rol
        if created:
            print(f"  ✅ Rol creado: {rol.name}")
        else:
            print(f"  ℹ️  Rol existente: {rol.name}")
    
    # Eliminar usuarios sin rol (si existen)
    usuarios_sin_rol = Usuario.objects.filter(rol_usuario__isnull=True)
    if usuarios_sin_rol.exists():
        print(f"\n  ⚠️  Eliminando {usuarios_sin_rol.count()} usuario(s) sin rol...")
        usuarios_sin_rol.delete()
    
    # Datos de usuarios
    usuarios_data = [
        {
            "username": "admin",
            "email": "admin@test.com",
            "password": "admin123",
            "first_name": "Admin",
            "last_name": "Principal",
            "rol": roles["Admin"],
            "is_superuser": True,
            "is_staff": True
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
    
    # Crear usuarios
    usuarios_creados = []
    usuarios_existentes = []
    
    for data in usuarios_data:
        if not Usuario.objects.filter(username=data["username"]).exists():
            if data.get("is_superuser"):
                usuario = Usuario.objects.create_superuser(
                    username=data["username"],
                    email=data["email"],
                    password=data["password"],
                    first_name=data["first_name"],
                    last_name=data["last_name"],
                    rol_usuario=data["rol"]
                )
            else:
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
            # Actualizar rol del usuario existente por si acaso
            usuario = Usuario.objects.get(username=data["username"])
            if usuario.rol_usuario != data["rol"]:
                usuario.rol_usuario = data["rol"]
                usuario.save()
                print(f"  🔄 Rol actualizado: {data['username']} -> {data['rol'].name}")
            usuarios_existentes.append(f"{data['username']} ({data['rol'].name})")
    
    # Mostrar resultados
    print("\n=== RESULTADO ===")
    if usuarios_creados:
        print("  ✅ Usuarios creados:")
        for u in usuarios_creados:
            print(f"     • {u}")
    
    if usuarios_existentes:
        print("  ℹ️  Usuarios ya existentes:")
        for u in usuarios_existentes:
            print(f"     • {u}")
    
    # Mostrar todos los usuarios actuales
    print("\n=== USUARIOS EN SISTEMA ===")
    usuarios = Usuario.objects.all().order_by('rol_usuario__name')
    for u in usuarios:
        rol = u.rol_usuario.name if u.rol_usuario else "SIN ROL"
        superuser = "👑" if u.is_superuser else "  "
        print(f"  {superuser} {u.username:15} | {u.email:25} | {rol}")

if __name__ == "__main__":
    crear_usuarios()