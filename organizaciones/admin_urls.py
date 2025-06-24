from django.urls import path
from . import admin_views
from . import views

urlpatterns = [
    path('', admin_views.admin_dashboard, name='admin_dashboard'),
    
    # Rutas para organizaciones
    path('organizaciones/', admin_views.admin_organizaciones, name='admin_organizaciones'),
    path('organizaciones/crear/', admin_views.crear_organizacion, name='crear_organizacion'),
    path('organizaciones/<int:org_id>/password/', admin_views.cambiar_password_organizacion, name='cambiar_password_organizacion'),
    path('organizaciones/<int:org_id>/toggle/', admin_views.toggle_estado_organizacion, name='toggle_estado_organizacion'),
    path('organizaciones/<int:org_id>/detalles/', admin_views.detalles_organizacion, name='detalles_organizacion'),
    path('organizaciones/<int:org_id>/editar/', admin_views.editar_organizacion, name='editar_organizacion'),
    path('organizaciones/<int:org_id>/eliminar/', admin_views.eliminar_organizacion, name='eliminar_organizacion'),
    
    # Rutas para usuarios
    path('usuarios/', admin_views.admin_usuarios, name='admin_usuarios'),
    path('usuarios/crear/', admin_views.crear_usuario, name='crear_usuario'),
    path('usuarios/<int:usuario_id>/detalles/', admin_views.detalles_usuario, name='detalles_usuario'),
    path('usuarios/<int:usuario_id>/editar/', admin_views.editar_usuario, name='editar_usuario'),
    path('usuarios/<int:usuario_id>/eliminar/', admin_views.eliminar_usuario, name='eliminar_usuario'),
    path('usuarios/<int:usuario_id>/password/', admin_views.restablecer_password_usuario, name='restablecer_password_usuario'),
    path('usuarios/<int:usuario_id>/toggle/', admin_views.toggle_estado_usuario, name='toggle_estado_usuario'),
]