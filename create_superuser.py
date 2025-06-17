import os
import django
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configurar entorno Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'athenea.settings')
django.setup()

from organizaciones.models import Organizacion

# Obtener credenciales de variables de entorno
SUPERUSER_EMAIL = os.getenv('SUPERUSER_EMAIL')
SUPERUSER_PASSWORD = os.getenv('SUPERUSER_PASSWORD')
SUPERUSER_NAME = os.getenv('SUPERUSER_NAME', 'Administrador')

# Verificar si el superusuario ya existe
if not Organizacion.objects.filter(email=SUPERUSER_EMAIL).exists():
    # Crear superusuario
    superuser = Organizacion.objects.create_superuser(
        nombre=SUPERUSER_NAME,
        email=SUPERUSER_EMAIL,
        password=SUPERUSER_PASSWORD
    )
    print("Superusuario creado exitosamente.")
else:
    # Actualizar contraseña si ya existe
    superuser = Organizacion.objects.get(email=SUPERUSER_EMAIL)
    superuser.set_password(SUPERUSER_PASSWORD)
    superuser.save()
    print("Contraseña de superusuario actualizada exitosamente.")