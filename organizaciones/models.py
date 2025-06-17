from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class OrganizacionManager(BaseUserManager):
    """
    Manager personalizado para el modelo Organizacion.
    """
    def create_user(self, nombre, email, password=None, **extra_fields):
        """
        Crea y guarda una organización con el nombre, email y contraseña dados.
        """
        if not email:
            raise ValueError('El Email es obligatorio')
        email = self.normalize_email(email)
        organizacion = self.model(nombre=nombre, email=email, **extra_fields)
        organizacion.set_password(password)
        organizacion.save(using=self._db)
        return organizacion
    
    def create_superuser(self, nombre, email, password=None, **extra_fields):
        """
        Crea y guarda una organización superusuaria.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        return self.create_user(nombre, email, password, **extra_fields)

class Organizacion(AbstractUser):
    """
    Modelo para representar una organización en el sistema.
    Hereda de AbstractUser para aprovechar la autenticación de Django.
    """
    username = None  # No usamos username, usamos email para login
    nombre = models.CharField(max_length=100, verbose_name="Nombre de la Organización")
    email = models.EmailField(unique=True, verbose_name="Correo Electrónico")
    logo = models.ImageField(upload_to='logos/', null=True, blank=True, verbose_name="Logo")
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Registro")
    activo = models.BooleanField(default=True, verbose_name="Activo")
    
    # Agregar related_name para evitar conflictos con User
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='Los grupos a los que pertenece esta organización.',
        related_name='organizacion_set',
        related_query_name='organizacion',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Permisos específicos para esta organización.',
        related_name='organizacion_set',
        related_query_name='organizacion',
    )
    
    USERNAME_FIELD = 'email'  # Campo para identificar al usuario en el login
    REQUIRED_FIELDS = ['nombre']  # Campos requeridos al crear un superusuario
    
    objects = OrganizacionManager()
    
    class Meta:
        verbose_name = "Organización"
        verbose_name_plural = "Organizaciones"
    
    def __str__(self):
        return self.nombre

class Usuario(models.Model):
    """
    Modelo para representar un usuario que pertenece a una organización.
    """
    organizacion = models.ForeignKey(Organizacion, on_delete=models.CASCADE, related_name='usuarios', verbose_name="Organización")
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    apellido = models.CharField(max_length=100, verbose_name="Apellido")
    email = models.EmailField(verbose_name="Correo Electrónico")
    password = models.CharField(max_length=128, verbose_name="Contraseña")
    activo = models.BooleanField(default=True, verbose_name="Activo")
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Registro")
    
    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        unique_together = ['organizacion', 'email']  # Email único por organización
    
    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.organizacion.nombre}"