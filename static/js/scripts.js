// Script para manejar el modal de recuperación de contraseña
document.addEventListener('DOMContentLoaded', function() {
    // Función para mostrar el modal de recuperación de contraseña
    const showPasswordResetModal = () => {
        const passwordResetModal = new bootstrap.Modal(document.getElementById('passwordResetModal'));
        passwordResetModal.show();
    };
    
    // Agregar evento al enlace de recuperación de contraseña
    const resetLink = document.querySelector('a[href*="password_reset"]');
    if (resetLink && document.getElementById('passwordResetModal')) {
        resetLink.addEventListener('click', function(e) {
            e.preventDefault();
            showPasswordResetModal();
        });
    }
    
    // Función para alternar la visibilidad del sidebar en dispositivos móviles
    const toggleSidebar = () => {
        const sidebar = document.getElementById('sidebar');
        if (sidebar) {
            sidebar.classList.toggle('show');
        }
    };
    
    // Agregar evento al botón de toggle del sidebar
    const sidebarToggle = document.getElementById('sidebarToggle');
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', toggleSidebar);
    }
});