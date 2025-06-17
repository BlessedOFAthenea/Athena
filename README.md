# Proyecto Athenea

Sistema de gestión para organizaciones con negocios, desarrollado en Django.

## Características

- Sistema de autenticación por organización y usuarios
- Panel de administración para organizaciones
- Gestión de usuarios por organización
- Gestión de negocios por organización

## Requisitos

- Python 3.8+
- Django 5.1+
- Pillow (para manejo de imágenes)

## Instalación

1. Clonar el repositorio:
```
git clone <url-del-repositorio>
cd Athenea
```

2. Crear un entorno virtual e instalar dependencias:
```
python -m venv venv
venv\Scripts\activate  # En Windows
source venv/bin/activate  # En Linux/Mac
pip install -r requirements.txt
```

3. Realizar migraciones:
```
python manage.py makemigrations
python manage.py migrate
```

4. El superusuario se creará automáticamente durante las migraciones con las credenciales predefinidas.

5. Ejecutar el servidor de desarrollo:
```
python manage.py runserver
```

## Superusuario

El sistema incluye un superusuario predefinido. Las credenciales se proporcionan por separado por motivos de seguridad.

## Estructura del Proyecto

- `athenea/`: Configuración principal del proyecto
- `organizaciones/`: Aplicación para gestionar organizaciones y usuarios
- `templates/`: Plantillas HTML
- `static/`: Archivos estáticos (CSS, JS, imágenes)
- `media/`: Archivos subidos por los usuarios

## Uso

1. Acceder a la página principal: `http://localhost:8000/`
2. Iniciar sesión con las credenciales de organización
3. Gestionar usuarios y negocios desde el panel de administración

## Licencia

Este proyecto está bajo la Licencia MIT.