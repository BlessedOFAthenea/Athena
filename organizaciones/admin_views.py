from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import hashlib
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
    organizaciones = Organizacion.objects.all().order_by('nombre')
    
    # Filtrar por organización si se selecciona una
    org_id = request.GET.get('organizacion')
    organizacion_seleccionada = None
    usuarios = []
    
    if org_id:
        try:
            organizacion_seleccionada = Organizacion.objects.get(id=org_id)
            usuarios = Usuario.objects.filter(organizacion=organizacion_seleccionada).order_by('-fecha_registro')
        except Organizacion.DoesNotExist:
            pass
    
    context = {
        'usuarios': usuarios,
        'organizaciones': organizaciones,
        'organizacion_seleccionada': organizacion_seleccionada,
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

@login_required
@user_passes_test(is_superuser)
def detalles_organizacion(request, org_id):
    """Vista para obtener detalles de una organización"""
    try:
        organizacion = Organizacion.objects.get(id=org_id)
        return JsonResponse({
            'success': True,
            'organizacion': {
                'id': organizacion.id,
                'nombre': organizacion.nombre,
                'email': organizacion.email,
                'nombre_encargado': organizacion.nombre_encargado,
                'tipo_giro': organizacion.tipo_giro,
                'telefono': organizacion.telefono,
                'rut': organizacion.rut,
                'direccion': organizacion.direccion,
                'comuna': organizacion.comuna,
                'region': organizacion.region,
                'fecha_registro': organizacion.fecha_registro.strftime('%d/%m/%Y %H:%M'),
                'activo': organizacion.activo,
                'usuarios_count': organizacion.usuarios.count()
            }
        })
    except Organizacion.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Organización no encontrada'})

@login_required
@user_passes_test(is_superuser)
def editar_organizacion(request, org_id):
    """Vista para editar una organización"""
    if request.method == 'POST':
        try:
            organizacion = Organizacion.objects.get(id=org_id)
            
            # Actualizar campos
            organizacion.nombre = request.POST.get('nombre')
            organizacion.email = request.POST.get('email')
            organizacion.nombre_encargado = request.POST.get('nombre_encargado')
            organizacion.tipo_giro = request.POST.get('tipo_giro')
            organizacion.telefono = request.POST.get('telefono')
            organizacion.rut = request.POST.get('rut')
            organizacion.direccion = request.POST.get('direccion')
            organizacion.comuna = request.POST.get('comuna')
            organizacion.region = request.POST.get('region')
            
            organizacion.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Organización actualizada exitosamente'
            })
        except Organizacion.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Organización no encontrada'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    
    return JsonResponse({'success': False, 'message': 'Método no permitido'})

@login_required
@user_passes_test(is_superuser)
def eliminar_organizacion(request, org_id):
    """Vista para eliminar una organización"""
    if request.method == 'POST':
        try:
            organizacion = Organizacion.objects.get(id=org_id)
            nombre = organizacion.nombre
            organizacion.delete()
            
            return JsonResponse({
                'success': True,
                'message': f'Organización "{nombre}" eliminada exitosamente'
            })
        except Organizacion.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Organización no encontrada'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error al eliminar: {str(e)}'})
    
    return JsonResponse({'success': False, 'message': 'Método no permitido'})

@login_required
@user_passes_test(is_superuser)
def crear_usuario(request):
    """Vista para crear un nuevo usuario"""
    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            org_id = request.POST.get('organizacion')
            nombre = request.POST.get('nombre')
            apellido = request.POST.get('apellido')
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            es_admin = request.POST.get('es_admin') == 'true'
            
            # Validaciones
            if not all([org_id, nombre, apellido, username, email, password]):
                return JsonResponse({'success': False, 'message': 'Todos los campos son obligatorios'})
            
            # Verificar que la organización existe
            try:
                organizacion = Organizacion.objects.get(id=org_id)
            except Organizacion.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'Organización no encontrada'})
            
            # Verificar que el username no exista en la organización
            if Usuario.objects.filter(organizacion=organizacion, username=username).exists():
                return JsonResponse({'success': False, 'message': 'El nombre de usuario ya existe en esta organización'})
            
            # Crear el usuario
            usuario = Usuario(
                organizacion=organizacion,
                nombre=nombre,
                apellido=apellido,
                username=username,
                email=email,
                password=hashlib.sha256(password.encode()).hexdigest(),
                es_admin=es_admin,
                cambio_password_requerido=True,
                password_temporal=True
            )
            usuario.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Usuario creado exitosamente',
                'usuario': {
                    'id': usuario.id,
                    'nombre': usuario.nombre,
                    'apellido': usuario.apellido,
                    'username': usuario.username,
                    'email': usuario.email,
                    'es_admin': usuario.es_admin
                }
            })
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error al crear usuario: {str(e)}'})
    
    return JsonResponse({'success': False, 'message': 'Método no permitido'})

@login_required
@user_passes_test(is_superuser)
def detalles_usuario(request, usuario_id):
    """Vista para obtener detalles de un usuario"""
    try:
        usuario = Usuario.objects.get(id=usuario_id)
        return JsonResponse({
            'success': True,
            'usuario': {
                'id': usuario.id,
                'nombre': usuario.nombre,
                'apellido': usuario.apellido,
                'username': usuario.username,
                'email': usuario.email,
                'es_admin': usuario.es_admin,
                'activo': usuario.activo,
                'fecha_registro': usuario.fecha_registro.strftime('%d/%m/%Y %H:%M'),
                'organizacion': {
                    'id': usuario.organizacion.id,
                    'nombre': usuario.organizacion.nombre
                }
            }
        })
    except Usuario.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Usuario no encontrado'})

@login_required
@user_passes_test(is_superuser)
def editar_usuario(request, usuario_id):
    """Vista para editar un usuario"""
    if request.method == 'POST':
        try:
            usuario = Usuario.objects.get(id=usuario_id)
            
            # Actualizar campos
            usuario.nombre = request.POST.get('nombre')
            usuario.apellido = request.POST.get('apellido')
            usuario.email = request.POST.get('email')
            usuario.es_admin = request.POST.get('es_admin') == 'true'
            
            # Verificar si se está cambiando el username
            nuevo_username = request.POST.get('username')
            if nuevo_username != usuario.username:
                # Verificar que el nuevo username no exista en la organización
                if Usuario.objects.filter(organizacion=usuario.organizacion, username=nuevo_username).exists():
                    return JsonResponse({'success': False, 'message': 'El nombre de usuario ya existe en esta organización'})
                usuario.username = nuevo_username
            
            usuario.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Usuario actualizado exitosamente'
            })
        except Usuario.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Usuario no encontrado'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    
    return JsonResponse({'success': False, 'message': 'Método no permitido'})

@login_required
@user_passes_test(is_superuser)
def eliminar_usuario(request, usuario_id):
    """Vista para eliminar un usuario"""
    if request.method == 'POST':
        try:
            usuario = Usuario.objects.get(id=usuario_id)
            nombre_completo = f"{usuario.nombre} {usuario.apellido}"
            usuario.delete()
            
            return JsonResponse({
                'success': True,
                'message': f'Usuario "{nombre_completo}" eliminado exitosamente'
            })
        except Usuario.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Usuario no encontrado'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error al eliminar: {str(e)}'})
    
    return JsonResponse({'success': False, 'message': 'Método no permitido'})

@login_required
@user_passes_test(is_superuser)
def restablecer_password_usuario(request, usuario_id):
    """Vista para restablecer la contraseña de un usuario"""
    if request.method == 'POST':
        try:
            usuario = Usuario.objects.get(id=usuario_id)
            nueva_password = request.POST.get('nueva_password')
            
            if len(nueva_password) < 8:
                return JsonResponse({'success': False, 'message': 'La contraseña debe tener al menos 8 caracteres'})
            
            # Actualizar contraseña
            usuario.password = hashlib.sha256(nueva_password.encode()).hexdigest()
            usuario.cambio_password_requerido = True
            usuario.password_temporal = True
            usuario.save()
            
            return JsonResponse({'success': True, 'message': 'Contraseña restablecida exitosamente'})
        except Usuario.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Usuario no encontrado'})
    
    return JsonResponse({'success': False, 'message': 'Método no permitido'})

@login_required
@user_passes_test(is_superuser)
def toggle_estado_usuario(request, usuario_id):
    """Vista para activar/desactivar un usuario"""
    if request.method == 'POST':
        try:
            usuario = Usuario.objects.get(id=usuario_id)
            usuario.activo = not usuario.activo
            usuario.save()
            
            estado = 'activado' if usuario.activo else 'desactivado'
            return JsonResponse({
                'success': True, 
                'message': f'Usuario {estado} exitosamente',
                'activo': usuario.activo
            })
        except Usuario.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Usuario no encontrado'})
    
    return JsonResponse({'success': False, 'message': 'Método no permitido'})