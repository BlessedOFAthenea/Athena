from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from .models import Organizacion, Usuario
import requests
from datetime import datetime
import pytz
import hashlib
import os
import subprocess
import django.db as db
from django.conf import settings

class OrganizacionLoginForm(AuthenticationForm):
    """
    Formulario para el inicio de sesión de organizaciones.
    """
    username = forms.EmailField(
        label="Correo Electrónico",
        widget=forms.EmailInput(attrs={'class': 'form-control text-white', 'placeholder': 'Correo electrónico'})
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control text-white', 'placeholder': 'Contraseña'})
    )
    remember_me = forms.BooleanField(
        label="Recordar contraseña",
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    class Meta:
        model = Organizacion
        fields = ['username', 'password', 'remember_me']

class OrganizacionPasswordResetForm(PasswordResetForm):
    """
    Formulario para recuperar contraseña de organizaciones.
    """
    email = forms.EmailField(
        label="Correo Electrónico",
        max_length=254,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'})
    )

class NuevaOrganizacionForm(forms.ModelForm):
    """
    Formulario para crear nueva organización.
    """
    class Meta:
        model = Organizacion
        fields = ['nombre', 'nombre_encargado', 'tipo_giro', 'email', 'telefono', 'rut', 'direccion', 'comuna', 'region']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la organización'}),
            'nombre_encargado': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del encargado'}),
            'tipo_giro': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tipo de giro'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@ejemplo.com'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+56 9 1234 5678'}),
            'rut': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '12.345.678-9'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dirección física'}),
            'comuna': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Comuna'}),
            'region': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Región'}),
        }
    
    def save(self, commit=True):
        organizacion = super().save(commit=False)
        organizacion.activo = False
        
        # Obtener fecha y hora de Chile
        try:
            response = requests.get('http://worldtimeapi.org/api/timezone/America/Santiago', timeout=5)
            if response.status_code == 200:
                data = response.json()
                organizacion.fecha_creacion = datetime.fromisoformat(data['datetime'].replace('Z', '+00:00'))
            else:
                raise Exception("API no disponible")
        except:
            # Fallback a hora local de Chile
            chile_tz = pytz.timezone('America/Santiago')
            organizacion.fecha_creacion = datetime.now(chile_tz)
        
        # Generar nombre de base de datos único
        db_name = f"org_{hashlib.md5(organizacion.nombre.encode()).hexdigest()[:8]}_{int(datetime.now().timestamp())}"
        organizacion.db_name = db_name
        
        if commit:
            organizacion.save()
            
            # Crear base de datos independiente
            self._crear_base_datos(db_name)
            
            # Crear usuario admin por defecto
            self._crear_usuario_admin(organizacion)
        
        return organizacion
    
    def _crear_base_datos(self, db_name):
        """Crea una base de datos independiente para la organización"""
        try:
            # Configuración para la nueva base de datos
            new_db = {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': os.path.join(settings.BASE_DIR, f'db_{db_name}.sqlite3'),
            }
            
            # Crear el archivo de base de datos
            connection = db.connections.create_connection(new_db)
            connection.close()
            
            # Registrar la nueva base de datos en settings
            settings.DATABASES[db_name] = new_db
            
            # Crear tablas básicas
            subprocess.run(['python', 'manage.py', 'migrate', '--database', db_name])
            
            return True
        except Exception as e:
            print(f"Error al crear base de datos: {str(e)}")
            return False
    
    def _crear_usuario_admin(self, organizacion):
        """Crea un usuario admin por defecto para la organización"""
        try:
            # Crear usuario admin
            admin_user = Usuario(
                organizacion=organizacion,
                nombre="Administrador",
                apellido="Sistema",
                email="admin@" + organizacion.email.split('@')[1],
                password=hashlib.sha256("admin".encode()).hexdigest(),  # En producción usar hash seguro
                es_admin=True,
                cambio_password_requerido=True,
                password_temporal=True
            )
            admin_user.save()
            
            return True
        except Exception as e:
            print(f"Error al crear usuario admin: {str(e)}")
            return False

class CambiarPasswordForm(forms.Form):
    """
    Formulario para cambiar contraseña de usuario.
    """
    password_actual = forms.CharField(
        label="Contraseña Actual",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    nueva_password = forms.CharField(
        label="Nueva Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        min_length=8
    )
    confirmar_password = forms.CharField(
        label="Confirmar Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    
    def clean(self):
        cleaned_data = super().clean()
        nueva_password = cleaned_data.get('nueva_password')
        confirmar_password = cleaned_data.get('confirmar_password')
        
        if nueva_password and confirmar_password and nueva_password != confirmar_password:
            self.add_error('confirmar_password', 'Las contraseñas no coinciden')
        
        return cleaned_data

class CambiarPasswordAdminForm(forms.Form):
    """
    Formulario para que el superusuario cambie la contraseña de un usuario admin.
    """
    nueva_password = forms.CharField(
        label="Nueva Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        min_length=8
    )
    confirmar_password = forms.CharField(
        label="Confirmar Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    
    def clean(self):
        cleaned_data = super().clean()
        nueva_password = cleaned_data.get('nueva_password')
        confirmar_password = cleaned_data.get('confirmar_password')
        
        if nueva_password and confirmar_password and nueva_password != confirmar_password:
            self.add_error('confirmar_password', 'Las contraseñas no coinciden')
        
        return cleaned_data