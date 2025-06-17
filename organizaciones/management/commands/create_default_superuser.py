from django.core.management.base import BaseCommand
from organizaciones.models import Organizacion
from organizaciones.utils import decode_credentials

class Command(BaseCommand):
    help = 'Crea el superusuario predeterminado'

    def handle(self, *args, **options):
        # Obtener credenciales decodificadas
        email, password, nombre = decode_credentials()

        # Verificar si el superusuario ya existe
        if not Organizacion.objects.filter(email=email).exists():
            # Crear superusuario
            Organizacion.objects.create_superuser(
                nombre=nombre,
                email=email,
                password=password
            )
            self.stdout.write(self.style.SUCCESS('Superusuario creado exitosamente'))
        else:
            # Actualizar contraseña si ya existe
            superuser = Organizacion.objects.get(email=email)
            superuser.set_password(password)
            superuser.save()
            self.stdout.write(self.style.SUCCESS('Contraseña de superusuario actualizada exitosamente'))