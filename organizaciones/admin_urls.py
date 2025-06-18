from django.urls import path
from . import admin_views

urlpatterns = [
    path('', admin_views.admin_dashboard, name='admin_dashboard'),
    path('organizaciones/', admin_views.admin_organizaciones, name='admin_organizaciones'),
    path('usuarios/', admin_views.admin_usuarios, name='admin_usuarios'),
]