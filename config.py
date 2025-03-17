import os

class Config:
    """Clase base de configuración."""
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Deshabilitar el seguimiento de cambios
    SECRET_KEY = os.environ.get('SECRET_KEY', 'Pa$$w0rd2024!')  # Clave secreta
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'uploads')  # Carpeta para uploads
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}  # Extensiones permitidas
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///usuarios.db')  # URI de la base de datos
