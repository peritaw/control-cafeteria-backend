import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model

def create_superuser():
    User = get_user_model()
    username = 'admin'
    password = 'admin123'
    email = 'admin@admin.com'
    
    if not User.objects.filter(username=username).exists():
        print(f"Creando superusuario {username}...")
        User.objects.create_superuser(username, email, password)
        print("¡Superusuario creado exitosamente!")
    else:
        print("El superusuario ya existe.")

if __name__ == '__main__':
    create_superuser()
