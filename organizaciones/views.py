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
        # Si el usuario ya está autenticado, redirigir según su tipo
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return redirect('/panel/')
            elif request.session.get('usuario_autenticado'):
                return redirect('dashboard')
            else:
                return redirect('usuario_login_paso2', org_id=request.user.id)
        
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
                # Guardar la organización en la sesión para el segundo paso de autenticación
                request.session['org_authenticated'] = True
                # Redirigir a la página de login de usuarios internos
                return redirect('usuario_login_paso2', org_id=organizacion.id)
        
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
        # Limpiar todas las variables de sesión
        if 'org_authenticated' in request.session:
            del request.session['org_authenticated']
        if 'usuario_autenticado' in request.session:
            del request.session['usuario_autenticado']
        if 'usuario_id' in request.session:
            del request.session['usuario_id']
        if 'usuario_nombre' in request.session:
            del request.session['usuario_nombre']
        if 'organizacion_id' in request.session:
            del request.session['organizacion_id']
            
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
    # Verificar que la organización esté autenticada
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Si es superusuario, redirigir al panel de administración
    if request.user.is_superuser:
        return redirect('/panel/')
    
    # Verificar que el usuario interno también esté autenticado
    if not request.session.get('usuario_autenticado'):
        return redirect('usuario_login_paso2', org_id=request.user.id)
    
    # Obtener información del usuario interno
    usuario_id = request.session.get('usuario_id')
    try:
        usuario = request.user.usuarios.get(id=usuario_id)
    except:
        # Si no se encuentra el usuario, redirigir al login de usuario
        if 'usuario_autenticado' in request.session:
            del request.session['usuario_autenticado']
        if 'usuario_id' in request.session:
            del request.session['usuario_id']
        if 'usuario_nombre' in request.session:
            del request.session['usuario_nombre']
        return redirect('usuario_login_paso2', org_id=request.user.id)
    
    # Mostrar el dashboard con información del usuario y la organización
    return render(request, 'organizaciones/dashboard.html', {'usuario': usuario})

class UsuarioLoginView(View):
    """
    Vista para el inicio de sesión de usuarios internos de una organización (acceso externo).
    """
    template_name = 'organizaciones/usuario_login.html'
    
    def get(self, request, org_id):
        """
        Maneja las solicitudes GET mostrando el formulario de login.
        """
        try:
            organizacion = Organizacion.objects.get(id=org_id)
            return render(request, self.template_name, {'organizacion': organizacion})
        except Organizacion.DoesNotExist:
            return redirect('login')
    
    def post(self, request, org_id):
        """
        Maneja las solicitudes POST procesando el formulario de login.
        """
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            organizacion = Organizacion.objects.get(id=org_id)
            try:
                usuario = organizacion.usuarios.get(email=email, activo=True)
                # Verificar contraseña (en un sistema real usaríamos hash)
                if usuario.password == password:
                    # Guardar información del usuario en la sesión
                    request.session['usuario_id'] = usuario.id
                    request.session['usuario_nombre'] = f"{usuario.nombre} {usuario.apellido}"
                    request.session['organizacion_id'] = org_id
                    return redirect('usuario_dashboard')
            except:
                pass
            
            # Si la autenticación falla
            return render(request, self.template_name, {
                'organizacion': organizacion,
                'error': 'Credenciales inválidas'
            })
        except Organizacion.DoesNotExist:
            return redirect('login')

class UsuarioLoginPaso2View(View):
    """
    Vista para el segundo paso de autenticación después del login de organización.
    """
    template_name = 'organizaciones/usuario_login_paso2.html'
    
    def get(self, request, org_id):
        """
        Maneja las solicitudes GET mostrando el formulario de login de usuario.
        """
        # Verificar que la organización esté autenticada
        if not request.user.is_authenticated or not request.session.get('org_authenticated'):
            return redirect('login')
        
        # Verificar que el usuario autenticado sea la organización correcta
        if request.user.id != org_id:
            logout(request)
            return redirect('login')
        
        return render(request, self.template_name, {'organizacion': request.user})
    
    def post(self, request, org_id):
        """
        Maneja las solicitudes POST procesando el formulario de login de usuario.
        """
        # Verificar que la organización esté autenticada
        if not request.user.is_authenticated or not request.session.get('org_authenticated'):
            return redirect('login')
        
        # Verificar que el usuario autenticado sea la organización correcta
        if request.user.id != org_id:
            logout(request)
            return redirect('login')
        
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            usuario = request.user.usuarios.get(email=email, activo=True)
            # Verificar contraseña (en un sistema real usaríamos hash)
            if usuario.password == password:
                # Guardar información del usuario en la sesión
                request.session['usuario_id'] = usuario.id
                request.session['usuario_nombre'] = f"{usuario.nombre} {usuario.apellido}"
                request.session['organizacion_id'] = org_id
                # Marcar que el usuario interno está autenticado
                request.session['usuario_autenticado'] = True
                return redirect('dashboard')
        except:
            pass
        
        # Si la autenticación falla
        return render(request, self.template_name, {
            'organizacion': request.user,
            'error': 'Credenciales inválidas'
        })

def usuario_dashboard(request):
    """
    Vista para el dashboard de usuarios internos.
    """
    # Verificar si el usuario está autenticado
    if 'usuario_id' not in request.session:
        return redirect('login')
    
    # Obtener información del usuario y la organización
    usuario_id = request.session['usuario_id']
    org_id = request.session['organizacion_id']
    
    try:
        organizacion = Organizacion.objects.get(id=org_id)
        usuario = organizacion.usuarios.get(id=usuario_id)
        return render(request, 'organizaciones/usuario_dashboard.html', {
            'usuario': usuario,
            'organizacion': organizacion
        })
    except:
        # Si hay algún error, cerrar sesión
        if 'usuario_id' in request.session:
            del request.session['usuario_id']
        if 'usuario_nombre' in request.session:
            del request.session['usuario_nombre']
        if 'organizacion_id' in request.session:
            del request.session['organizacion_id']
        return redirect('login')

def usuario_logout(request):
    """
    Vista para cerrar sesión de usuarios internos.
    """
    if 'usuario_id' in request.session:
        del request.session['usuario_id']
    if 'usuario_nombre' in request.session:
        del request.session['usuario_nombre']
    if 'organizacion_id' in request.session:
        del request.session['organizacion_id']
    return redirect('login')

class SuperUserLoginView(LoginView):
    """
    Vista para el inicio de sesión de superusuarios.
    """
    template_name = 'organizaciones/superuser_login.html'
    form_class = AdminAuthenticationForm
    
    def get_success_url(self):
        """
        Redirige al panel personalizado después del login exitoso.
        """
        return '/panel/'
    
    def dispatch(self, request, *args, **kwargs):
        """
        Verifica que solo los superusuarios puedan acceder.
        """
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return redirect('/panel/')
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)