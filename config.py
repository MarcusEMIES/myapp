import os
from datetime import timedelta
from dotenv import load_dotenv
import base64
from flask_mail import Mail

# Cargar las variables de configuración desde el archivo .env para mantener la información sensible fuera del código.
load_dotenv()

# Instancia de Flask-Mail global (debe inicializarse en app.py).
# Esta instancia se utilizará para enviar correos electrónicos en la aplicación.
mail = Mail()

class Config:
    """Clase base de configuración para la aplicación."""

    # 🔒 Clave secreta utilizada para firmar cookies y proteger la sesión del usuario.
    # Se obtiene del archivo .env o se establece un valor predeterminado.
    SECRET_KEY = os.environ.get('SECRET_KEY', 'Pa$$w0rd2024!')

    # 🔹 Configuración de claves para Stripe (usadas para pagos en línea).
    STRIPE_PUBLIC_KEY = os.environ.get("STRIPE_PUBLIC_KEY", "tu_public_key_aqui")
    STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY", "tu_secret_key_aqui")

    # 🔹 Configuración de REDSYS (para pagos con tarjeta o Bizum, usando el entorno de pruebas).
    @staticmethod
    def corregir_base64(clave):
        """Corrige el padding en una clave Base64 si es necesario."""
        faltante = len(clave) % 4  # Verifica si el padding de la clave Base64 está incompleto.
        if faltante:
            clave += "=" * (4 - faltante)  # Añade el padding necesario.
        return clave

    # Datos específicos de REDSYS, incluyendo la clave secreta (convertida en base64) y el código del comercio.
    REDSYS_MERCHANT_CODE = "123456789"  # Código del comercio para REDSYS.
    REDSYS_TERMINAL = "1"  # Terminal de REDSYS (especificado por el banco).
    REDSYS_SECRET_KEY = corregir_base64("TuClaveSecretaEnBase64")  # Clave secreta codificada en Base64.
    REDSYS_URL = "https://sis-t.redsys.es:25443/sis/realizarPago"  # URL de REDSYS para realizar el pago.

    # # 🔹 Configuración de sesiones (para manejar la sesión de usuario).
    # SESSION_TYPE = 'filesystem'  # El tipo de sesión se guardará en el sistema de archivos.
    # PERMANENT_SESSION_LIFETIME = timedelta(days=7)  # Duración de la sesión permanente de 7 días.
    # REMEMBER_COOKIE_DURATION = timedelta(days=7)  # Duración de la cookie "recordarme" (7 días).

    # 🔹 Configuración de correo electrónico (utiliza Flask-Mail para enviar correos).
    # Parámetros del servidor de correo, como el servidor SMTP y las credenciales de acceso.
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.mht.com')  # Servidor SMTP de tu dominio.
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))  # Puerto estándar para TLS (587).
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS') == 'True'  # Activa TLS para seguridad.
    MAIL_USERNAME = os.getenv('MAIL_USERNAME', 'admin@mht.com')  # Correo electrónico del usuario.
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')  # Contraseña del correo electrónico (se obtiene del archivo .env).
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', 'admin@mht.com')  # Correo por defecto del remitente.

    # 🔹 Configuración de rutas para subir archivos (por ejemplo, imágenes).
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # Directorio base del proyecto.
    INSTANCE_FOLDER = os.path.join(BASE_DIR, 'instance')  # Carpeta de instancia donde se almacenan archivos de configuración.
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')  # Carpeta para subir archivos como imágenes.

    # Especificamos las extensiones de archivo permitidas para las subidas.
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

    # Crea las carpetas necesarias si no existen (por ejemplo, 'instance' y 'uploads').
    os.makedirs(INSTANCE_FOLDER, exist_ok=True)
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    # 🔹 Configuración de base de datos con SQLAlchemy.
    # Se obtiene la URL de la base de datos desde el archivo .env (o se usa una base de datos SQLite local por defecto).
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL', f"sqlite:///{os.path.join(INSTANCE_FOLDER, 'usuarios.db')}"
    )  # URI de la base de datos principal.

    # Configuración de bases de datos adicionales (productos, reservas, mensajes).
    SQLALCHEMY_BINDS = {
        'products_db': f"sqlite:///{os.path.join(INSTANCE_FOLDER, 'products.db')}",  # Base de datos de productos.
        'reserva_db': f"sqlite:///{os.path.join(INSTANCE_FOLDER, 'reservas.db')}",  # Base de datos de reservas.
        'correo_db': f"sqlite:///{os.path.join(INSTANCE_FOLDER, 'correo.db')}",  # Base de datos de correos/contactos.
    }

    # Evitar el seguimiento de modificaciones en la base de datos (para optimizar rendimiento).
    SQLALCHEMY_TRACK_MODIFICATIONS = False
