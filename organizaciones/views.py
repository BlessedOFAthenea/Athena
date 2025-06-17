from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.views import PasswordResetView, LoginView
from django.urls import reverse_lazy
from django.views import View
from django.contrib.admin.forms import AdminAuthenticationForm
from .forms import OrganizacionLoginForm, OrganizacionPasswordResetForm
from .models import Organizacion

class OrganizacionLoginView(View):
    """
    Vista para el inicio de sesión de organizaciones.
    """
    template_name = 'organizaciones/login.html'
    form_class = OrganizacionLoginForm
    
    def get(self, request):
        """
        Maneja las solicitudes GET mostrando el formulario de login.
        """
        # Si el usuario ya está autenticado, redirigir al dashboard
        if request.user.is_authenticated:
            return redirect('dashboard')
        
        form = self.form_class()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        """
        Maneja las solicitudes POST procesando el formulario de login.
        """
        form = self.form_class(data=request.POST)
        
        if form.is_valid():
            email = form.cleaned_data.get('username')  # El campo se llama username en el form pero es email
            password = form.cleaned_data.get('password')
            remember_me = form.cleaned_data.get('remember_me', False)
            
            # Autenticar la organización
            organizacion = authenticate(request, username=email, password=password)
            
            if organizacion is not None:
                # Si el usuario no quiere ser recordado, la sesión expirará cuando cierre el navegador
                if not remember_me:
                    request.session.set_expiry(0)
                
                login(request, organizacion)
                return redirect('dashboard')  # Redirigir al dashboard después del login
        
        # Si el formulario no es válido o la autenticación falla
        return render(request, self.template_name, {'form': form})

class OrganizacionLogoutView(View):
    """
    Vista para cerrar sesión de organizaciones.
    """
    def get(self, request):
        """
        Maneja las solicitudes GET para cerrar sesión.
        """
        logout(request)
        return redirect('login')  # Redirigir al login después de cerrar sesión

class OrganizacionPasswordResetView(PasswordResetView):
    """
    Vista para recuperar contraseña de organizaciones.
    """
    template_name = 'organizaciones/password_reset.html'
    form_class = OrganizacionPasswordResetForm
    email_template_name = 'organizaciones/password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')

def dashboard(request):
    """
    Vista para el dashboard de la organización.
    """
    # Aquí se mostrará el dashboard después del login
    return render(request, 'organizaciones/dashboard.html')

class SuperUserLoginView(LoginView):
    """
    Vista para el inicio de sesión de superusuarios.
    """
    template_name = 'organizaciones/superuser_login.html'
    form_class = AdminAuthenticationForm
    
    def get_success_url(self):
        """
        Redirige al admin después del login exitoso.
        """
        return '/admin/'
    
    def dispatch(self, request, *args, **kwargs):
        """
        Verifica que solo los superusuarios puedan acceder.
        """
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return redirect('admin:index')
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)