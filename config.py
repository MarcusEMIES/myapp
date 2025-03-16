import os

class Config:
    """Clase base de configuración."""
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'clave_secreta')  # Utiliza variable de entorno
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///usuarios.db')

class MhtDesarrollo(Config):
    """Configuración para el entorno de desarrollo."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///usuarios.db'

class MhtProduccion(Config):
    """Configuración para el entorno de producción."""
    DEBUG = False

# Diccionario para seleccionar el entorno
config = {
    'desarrollo': MhtDesarrollo,
    'produccion': MhtProduccion
}
