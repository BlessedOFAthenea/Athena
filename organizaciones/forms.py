from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from .models import Organizacion

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