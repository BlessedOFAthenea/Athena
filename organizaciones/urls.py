from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # URL para el login de organizaciones
    path('', views.OrganizacionLoginView.as_view(), name='login'),
    
    # URL para el login de superusuarios
    path('admin-login/', views.SuperUserLoginView.as_view(), name='admin_login'),
    
    # URL para el logout
    path('logout/', views.OrganizacionLogoutView.as_view(), name='logout'),
    
    # URLs para usuarios internos
    path('organizacion/<int:org_id>/login/', views.UsuarioLoginView.as_view(), name='usuario_login'),
    path('organizacion/<int:org_id>/usuario-login/', views.UsuarioLoginPaso2View.as_view(), name='usuario_login_paso2'),
    path('usuario/dashboard/', views.usuario_dashboard, name='usuario_dashboard'),
    path('usuario/logout/', views.usuario_logout, name='usuario_logout'),
    path('usuario/cambiar-password/', views.cambiar_password_obligatorio, name='cambiar_password_obligatorio'),
    
    # URLs para la recuperación de contraseña
    path('password-reset/', views.OrganizacionPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name='organizaciones/password_reset_done.html'), 
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name='organizaciones/password_reset_confirm.html'), 
         name='password_reset_confirm'),
    path('password-reset-complete/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='organizaciones/password_reset_complete.html'), 
         name='password_reset_complete'),
    
    # URL para el dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
]