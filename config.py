import os

class Config:
    """Clase base de configuración."""
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Deshabilitar la notificación de modificaciones de objetos
    SECRET_KEY = os.environ.get('SECRET_KEY', 'clave_secreta')  # Usa variable de entorno o valor por defecto
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}  # Extensiones permitidas para imágenes
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///usuarios.db')  # Permitir base de datos desde env

class MhtDesarrollo(Config):
    """Configuración para el entorno de desarrollo."""
    DEBUG = True  # Activar modo de depuración
    SQLALCHEMY_DATABASE_URI = 'sqlite:///usuarios.db'  # Usar SQLite en desarrollo

class MhtProduccion(Config):
    """Configuración para el entorno de producción."""
    DEBUG = False  # Desactivar depuración en producción
    # Aquí puedes agregar configuraciones específicas para producción, como la base de datos en la nube

# Diccionario para seleccionar el entorno
config = {
    'desarrollo': MhtDesarrollo,
    'produccion': MhtProduccion
}
