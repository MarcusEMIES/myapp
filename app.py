from flask import Flask, render_template, session, flash, redirect, url_for
from flask_mail import Mail  # ✅ Importa Mail correctamente
from config import Config, Mail  # ✅ Importa mail desde config.py
from models import db, login_manager
from routes import init_app
from models.users import User
from flask_migrate import Migrate
from datetime import datetime, timedelta
import os
from flask_login import current_user, login_required

# Crear carpetas necesarias si no existen
os.makedirs(Config.INSTANCE_FOLDER, exist_ok=True)
os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)

# Crea la aplicación
app = Flask(__name__)
app.config.from_object(Config)

# Inicializa las extensiones
db.init_app(app)
login_manager.init_app(app)
# 🔥 Inicializa Flask-Mail después de configurar la app
mail = Mail()  # ✅ Creamos la instancia aquí
mail.init_app(app)  # ✅ Ahora lo inicializamos con app después de definirla

# Inicializa Flask-Migrate
migrate = Migrate(app, db)

# Registra las rutas
init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    if 'expires' not in session and current_user.is_authenticated:
        session['expires'] = (datetime.now() + timedelta(minutes=2)).isoformat()
    return render_template('index.html')

@app.before_request
def check_session_expiration():
    if 'expires' in session:
        expiration_time = datetime.fromisoformat(session['expires'])
        if datetime.now() > expiration_time:
            flash("Tu sesión ha expirado.", "warning")
            return redirect(url_for('auth.login'))

@app.before_request
def make_session_permanent():
    session.permanent = True

# Crear la base de datos si no existe
with app.app_context():
    db.create_all()
with app.app_context():
    usuario = User.query.get(1)  # Obtener usuario con ID 1


if __name__ == '__main__':
    app.run(debug=True)
