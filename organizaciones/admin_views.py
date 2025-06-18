from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count
from .models import Organizacion, Usuario

def is_superuser(user):
    """Verifica si el usuario es superusuario"""
    return user.is_superuser

@login_required
@user_passes_test(is_superuser)
def admin_dashboard(request):
    """Dashboard principal para superusuarios"""
    # Obtener estadísticas
    total_organizaciones = Organizacion.objects.count()
    total_usuarios = Usuario.objects.count()
    organizaciones_activas = Organizacion.objects.filter(activo=True).count()
    
    # Organizaciones con más usuarios
    top_organizaciones = Organizacion.objects.annotate(
        num_usuarios=Count('usuarios')
    ).order_by('-num_usuarios')[:5]
    
    context = {
        'total_organizaciones': total_organizaciones,
        'total_usuarios': total_usuarios,
        'organizaciones_activas': organizaciones_activas,
        'top_organizaciones': top_organizaciones,
    }
    
    return render(request, 'admin/dashboard.html', context)

@login_required
@user_passes_test(is_superuser)
def admin_organizaciones(request):
    """Vista para gestionar organizaciones"""
    organizaciones = Organizacion.objects.all().order_by('-fecha_registro')
    
    context = {
        'organizaciones': organizaciones,
    }
    
    return render(request, 'admin/organizaciones.html', context)

@login_required
@user_passes_test(is_superuser)
def admin_usuarios(request):
    """Vista para gestionar usuarios de todas las organizaciones"""
    usuarios = Usuario.objects.all().select_related('organizacion').order_by('-fecha_registro')
    
    context = {
        'usuarios': usuarios,
    }
    
    return render(request, 'admin/usuarios.html', context)