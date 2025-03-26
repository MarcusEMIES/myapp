import os
from datetime import timedelta
from dotenv import load_dotenv
import base64
from flask_mail import Mail

# Cargar variables desde .env
load_dotenv()

# 🔹 Instancia de Flask-Mail global (debe inicializarse en app.py)
mail = Mail()

class Config:
    """Clase base de configuración para la aplicación."""

    # 🔒 Clave secreta
    SECRET_KEY = os.environ.get('SECRET_KEY', 'Pa$$w0rd2024!')

    # 🔹 Claves de Stripe (para pagos)
    STRIPE_PUBLIC_KEY = os.environ.get("STRIPE_PUBLIC_KEY", "tu_public_key_aqui")
    STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY", "tu_secret_key_aqui")

    # 🔹 Configuración de REDSYS (Modo Pruebas)
    @staticmethod
    def corregir_base64(clave):
        """Corrige el padding en una clave Base64 si es necesario."""
        faltante = len(clave) % 4
        if faltante:
            clave += "=" * (4 - faltante)
        return clave

    REDSYS_MERCHANT_CODE = "123456789"
    REDSYS_TERMINAL = "1"
    REDSYS_SECRET_KEY = corregir_base64("TuClaveSecretaEnBase64")
    REDSYS_URL = "https://sis-t.redsys.es:25443/sis/realizarPago"

    # 🔹 Configuración de sesiones
    SESSION_TYPE = 'filesystem'
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    REMEMBER_COOKIE_DURATION = timedelta(days=7)
    

    # Configuración del correo
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.mht.com')  # Servidor SMTP de tu dominio
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))  # Puerto estándar para TLS
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS') == 'True'  # Activa TLS
    MAIL_USERNAME = os.getenv('MAIL_USERNAME', 'admin@mht.com')  # Tu correo
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')  # Contraseña del correo
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', 'admin@mht.com')  # Email remitente

    
    # mail = Mail()  # No inicializamos con app aquí

    # 🔹 Configuración de rutas
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    INSTANCE_FOLDER = os.path.join(BASE_DIR, 'instance')
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}  # Extensiones permitidas

    os.makedirs(INSTANCE_FOLDER, exist_ok=True)
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    # 🔹 Configuración de base de datos
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL', f"sqlite:///{os.path.join(INSTANCE_FOLDER, 'usuarios.db')}"
    )     

    SQLALCHEMY_BINDS = {
        'products_db': f"sqlite:///{os.path.join(INSTANCE_FOLDER, 'products.db')}",
        'reserva_db': f"sqlite:///{os.path.join(INSTANCE_FOLDER, 'reservas.db')}",
        'correo_db': f"sqlite:///{os.path.join(INSTANCE_FOLDER, 'correo.db')}",
    }

    SQLALCHEMY_TRACK_MODIFICATIONS = False
