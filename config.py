#Configuracion de configuracion config.py para la aplicacion


import os

class Config:
    """Clase base de configuración."""

    # Deshabilita el seguimiento de modificaciones en las bases de datos para mejorar el rendimiento
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # La clave secreta de la aplicación, importante para sesiones y CSRF
    SECRET_KEY = os.environ.get('SECRET_KEY', 'Pa$$w0rd2024!')  # Utiliza variable de entorno (si existe) o un valor predeterminado

    # Carpeta de subida de archivos
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'uploads')

    # Extensiones permitidas para los archivos subidos
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

    # URI para la base de datos, utilizando SQLite por defecto. Se puede sobrescribir mediante la variable de entorno
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///usuarios.db')
