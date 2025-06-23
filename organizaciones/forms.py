from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from .models import Organizacion
import requests
from datetime import datetime
import pytz

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
        
        if commit:
            organizacion.save()
        return organizacion