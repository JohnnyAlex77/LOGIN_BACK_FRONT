# ver_usuarios.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'login.settings')
django.setup()

from usuarios.models import Usuario, Rol

def ver_usuarios():
    print("=" * 60)
    print("USUARIOS EN BASE DE DATOS")
    print("=" * 60)
    
    total = Usuario.objects.count()
    print(f"Total de usuarios: {total}\n")
    
    if total == 0:
        print("❌ No hay usuarios en la base de datos")
        return
    
    # Usuarios por rol
    roles = Rol.objects.all()
    for rol in roles:
        count = Usuario.objects.filter(rol_usuario=rol).count()
        print(f"📌 {rol.name}: {count} usuario(s)")
    
    print("\n" + "=" * 60)
    print("DETALLE DE USUARIOS")
    print("=" * 60)
    
    for usuario in Usuario.objects.all().order_by('rol_usuario__name', 'username'):
        print(f"\n📧 Username: {usuario.username}")
        print(f"   Email: {usuario.email}")
        print(f"   Nombre: {usuario.first_name} {usuario.last_name}")
        print(f"   Rol: {usuario.rol_usuario.name if usuario.rol_usuario else 'SIN ROL'}")
        print(f"   Activo: {usuario.is_active}")
        print(f"   Superusuario: {usuario.is_superuser}")
        print(f"   Fecha creación: {usuario.date_joined.strftime('%Y-%m-%d %H:%M')}")
        print("-" * 40)

if __name__ == "__main__":
    ver_usuarios()