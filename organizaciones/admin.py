from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Organizacion, Usuario

@admin.register(Organizacion)
class OrganizacionAdmin(UserAdmin):
    """
    Configuración del admin para el modelo Organizacion.
    """
    list_display = ('nombre', 'email', 'fecha_registro', 'activo')
    list_filter = ('activo', 'fecha_registro')
    search_fields = ('nombre', 'email')
    ordering = ('nombre',)
    
    # Campos para el formulario de creación/edición
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Información de la Organización', {'fields': ('nombre', 'logo')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas importantes', {'fields': ('last_login', 'date_joined')}),
    )
    
    # Campos para el formulario de creación
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nombre', 'password1', 'password2'),
        }),
    )

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    """
    Configuración del admin para el modelo Usuario.
    """
    list_display = ('nombre', 'apellido', 'email', 'organizacion', 'activo', 'fecha_registro')
    list_filter = ('activo', 'fecha_registro', 'organizacion')
    search_fields = ('nombre', 'apellido', 'email', 'organizacion__nombre')
    ordering = ('organizacion', 'nombre')