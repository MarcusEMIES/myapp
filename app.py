# app.py

from flask import Flask, render_template, session, flash, redirect, url_for
from config import Config
from models import db, login_manager
from routes import init_app
from models.users import User
from flask_migrate import Migrate
from datetime import datetime, timedelta  # Corregido de "datatime" a "datetime"
from models.reserva import Reserva
from models.products import Product
# Importar el Blueprint
import os
from flask_login import current_user, login_required

# Crear carpetas necesarias si no existen
os.makedirs(Config.INSTANCE_FOLDER, exist_ok=True)
os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)

# Crea la aplicación
app = Flask(__name__)
app.config.from_object(Config)

# Inicializa la base de datos y login_manager
db.init_app(app)
login_manager.init_app(app)

# Inicializa Flask-Migrate para manejar las migraciones de la base de datos
migrate = Migrate(app, db)

# Registra las rutas
init_app(app)

# Función user_loader que Flask-Login necesita para cargar al usuario
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    # Si la sesión ya tiene un valor de expiración, usarlo. Si no, establecerlo.
    if 'expires' not in session and current_user.is_authenticated:
        session['expires'] = (datetime.now() + timedelta(minutes=2)).isoformat()  # 2 minutos de expiración
    return render_template('index.html')


@app.route('/update-session', methods=['POST'])
def update_session():
    """Actualizar la hora de expiración de la sesión"""
    session['expires'] = (datetime.now() + timedelta(minutes=2)).isoformat()  # Actualizar la expiración a 2 minutos
    return '', 204  # No devolver contenido
@app.before_request
def check_session_expiration():
    if 'expires' in session:
        expiration_time = datetime.fromisoformat(session['expires'])
        if datetime.now() > expiration_time:
            flash("Tu sesión ha expirado.", "warning")
            return redirect(url_for('auth.login'))
        
# Esto asegura que la sesión sea "permanente" mientras el usuario esté activo
@app.before_request
def make_session_permanent():
    session.permanent = True
    
# Crear la base de datos si no existe
with app.app_context():
    db.create_all()  # Crea las tablas si no existen





# Asegúrate de que las migraciones estén configuradas correctamente
if __name__ == '__main__':
    app.run(debug=True)
