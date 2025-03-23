import os
from models.products import Product
from datetime import timedelta

class Config:
    """Clase base de configuración para la aplicación."""

    # Clave secreta para la aplicación (cambiar en producción)
    SECRET_KEY = os.environ.get('SECRET_KEY', 'Pa$$w0rd2024!')
    
    
    # Aquí van otras configuraciones de tu app si las tienes
    SESSION_TYPE = 'filesystem'  # Usar sesiones en archivos
    # PERMANENT_SESSION_LIFETIME = timedelta(minutes=None)  # Expiración de sesión tras 2 minutos
    # REMEMBER_COOKIE_DURATION = timedelta(minutes=2)  # Duración del cookie "remember me"
    SESSION_TYPE = 'filesystem'  # Usar sesiones en archivos
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)  # Expiración de sesión en 7 días
    REMEMBER_COOKIE_DURATION = timedelta(days=7)  # Duración del cookie "remember me" por 7 días

    
    
    # Configuración de la carpeta de uploads y extensiones permitidas
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # Directorio base
    INSTANCE_FOLDER = os.path.join(BASE_DIR, 'instance')  # Carpeta para las bases de datos
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')  # Carpeta para subir archivos
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

    # Crear carpetas si no existen
    os.makedirs(INSTANCE_FOLDER, exist_ok=True)
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    # Configuración de la base de datos principal (usuarios.db)
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL', f"sqlite:///{os.path.join(INSTANCE_FOLDER, 'usuarios.db')}"
    )     

    # Configuración de bases de datos adicionales (products.db)
    SQLALCHEMY_BINDS = {
        'products_db': f"sqlite:///{os.path.join(INSTANCE_FOLDER, 'products.db')}"
    }

    # Deshabilitar el seguimiento de modificaciones para mejorar el rendimiento
    SQLALCHEMY_TRACK_MODIFICATIONS = False
