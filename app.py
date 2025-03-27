from flask import Flask, render_template, session, flash, redirect, url_for
from flask_mail import Mail  # ✅ Importa Mail correctamente
from config import Config, Mail  # ✅ Importa mail desde config.py
from models import db, login_manager  # Importa la instancia de base de datos y el manejador de login
from routes import init_app  # Importa la función que inicializa las rutas
from models.users import User  # Importa el modelo de usuario desde la carpeta 'models/users.py'
from flask_migrate import Migrate  # Importa la extensión para migraciones de base de datos
from datetime import datetime, timedelta  # Importa funciones para manejar fechas
import os  # Para manejar la creación de carpetas
from flask_login import current_user, login_required  # Para manejo de usuarios y control de sesiones

# Crear las carpetas necesarias si no existen
# Estas carpetas se usarán para almacenar archivos e instancias de la app, como bases de datos o archivos subidos
os.makedirs(Config.INSTANCE_FOLDER, exist_ok=True)
os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)

# Crea la aplicación Flask
app = Flask(__name__)
# Carga la configuración desde la clase Config (configura claves, bases de datos, etc.)
app.config.from_object(Config)

# Inicializa las extensiones de Flask
db.init_app(app)  # Configura la base de datos
login_manager.init_app(app)  # Inicializa el manejador de login

# 🔥 Inicializa Flask-Mail después de configurar la app
mail = Mail()  # ✅ Creamos la instancia aquí
mail.init_app(app)  # ✅ Ahora lo inicializamos con la app después de definirla

# Inicializa Flask-Migrate para manejar migraciones de la base de datos
migrate = Migrate(app, db)

# Registra las rutas de la aplicación, esto se hace en un archivo de rutas separado
init_app(app)

# Carga al usuario en base al ID cuando el usuario está autenticado
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



# Ruta para la página de inicio (index)
@app.route('/')
@login_required  # Esto asegura que solo los usuarios autenticados puedan acceder
def index():
    # Si el usuario está autenticado, se muestra la página principal
    return render_template('index.html', user=current_user)
# # Ruta principal de la aplicación
# @app.route('/')
# def index():
#     # Si no existe la clave 'expires' en la sesión y el usuario está autenticado,
#     # se establece un tiempo de expiración para la sesión (2 minutos en este caso).
#     if 'expires' not in session and current_user.is_authenticated:
#         session['expires'] = (datetime.now() + timedelta(minutes=2)).isoformat()
#     return render_template('index.html')

# # Verifica si la sesión ha expirado antes de cada solicitud
# @app.before_request
# def check_session_expiration():
#     # Si existe la clave 'expires' en la sesión, comprueba si la fecha de expiración es mayor que la hora actual
#     if 'expires' in session:
#         expiration_time = datetime.fromisoformat(session['expires'])
#         if datetime.now() > expiration_time:
#             flash("Tu sesión ha expirado.", "warning")
#             return redirect(url_for('auth.login'))  # Redirige al login si la sesión ha expirado

# # Establece la sesión como permanente antes de cada solicitud
# @app.before_request
# def make_session_permanent():
#     session.permanent = True  # Establece la duración de la sesión como permanente

# Crear la base de datos si no existe
# Se usa `app.app_context()` para acceder al contexto de la aplicación y crear las tablas de la base de datos
with app.app_context():
    db.create_all()  # Crea todas las tablas definidas en los modelos si no existen

# Obtiene un usuario con ID 1 (esto podría ser útil para comprobar si el usuario existe)
with app.app_context():
    usuario = User.query.get(1)  # Obtiene el primer usuario de la base de datos

# Si la aplicación se ejecuta directamente, lanza el servidor en modo de depuración
if __name__ == '__main__':
    app.run(debug=True)
