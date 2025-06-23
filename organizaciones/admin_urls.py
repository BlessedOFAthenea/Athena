from django.urls import path
from . import admin_views

urlpatterns = [
    path('', admin_views.admin_dashboard, name='admin_dashboard'),
    path('organizaciones/', admin_views.admin_organizaciones, name='admin_organizaciones'),
    path('organizaciones/crear/', admin_views.crear_organizacion, name='crear_organizacion'),
    path('organizaciones/<int:org_id>/password/', admin_views.cambiar_password_organizacion, name='cambiar_password_organizacion'),
    path('organizaciones/<int:org_id>/toggle/', admin_views.toggle_estado_organizacion, name='toggle_estado_organizacion'),
    path('usuarios/', admin_views.admin_usuarios, name='admin_usuarios'),
]