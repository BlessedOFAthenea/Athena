from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Organizacion, Usuario
from .forms import NuevaOrganizacionForm

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
    organizaciones = Organizacion.objects.filter(activo=True).order_by('nombre')
    
    context = {
        'usuarios': usuarios,
        'organizaciones': organizaciones,
    }
    
    return render(request, 'admin/usuarios.html', context)

@login_required
@user_passes_test(is_superuser)
def crear_organizacion(request):
    """Vista para crear nueva organización via AJAX"""
    if request.method == 'POST':
        form = NuevaOrganizacionForm(request.POST)
        if form.is_valid():
            organizacion = form.save()
            return JsonResponse({
                'success': True,
                'message': 'Organización creada exitosamente',
                'organizacion': {
                    'id': organizacion.id,
                    'nombre': organizacion.nombre,
                    'email': organizacion.email,
                    'fecha_creacion': organizacion.fecha_creacion.strftime('%d/%m/%Y %H:%M')
                }
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            })
    
    return JsonResponse({'success': False, 'message': 'Método no permitido'})

@login_required
@user_passes_test(is_superuser)
def cambiar_password_organizacion(request, org_id):
    """Vista para cambiar contraseña de organización"""
    if request.method == 'POST':
        try:
            organizacion = Organizacion.objects.get(id=org_id)
            nueva_password = request.POST.get('nueva_password')
            
            if len(nueva_password) < 8:
                return JsonResponse({'success': False, 'message': 'La contraseña debe tener al menos 8 caracteres'})
            
            organizacion.set_password(nueva_password)
            organizacion.save()
            
            return JsonResponse({'success': True, 'message': 'Contraseña actualizada exitosamente'})
        except Organizacion.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Organización no encontrada'})
    
    return JsonResponse({'success': False, 'message': 'Método no permitido'})

@login_required
@user_passes_test(is_superuser)
def toggle_estado_organizacion(request, org_id):
    """Vista para habilitar/deshabilitar organización"""
    if request.method == 'POST':
        try:
            organizacion = Organizacion.objects.get(id=org_id)
            organizacion.activo = not organizacion.activo
            organizacion.save()
            
            estado = 'habilitada' if organizacion.activo else 'deshabilitada'
            return JsonResponse({
                'success': True, 
                'message': f'Organización {estado} exitosamente',
                'activo': organizacion.activo
            })
        except Organizacion.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Organización no encontrada'})
    
    return JsonResponse({'success': False, 'message': 'Método no permitido'})