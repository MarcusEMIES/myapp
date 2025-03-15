from flask import Flask, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager  # Para manejar la autenticación de usuarios
from routes.auth import auth
from routes.tareas import tasks
from routes.admin import admin
from models import db
from config import Config  # Asegúrate de importar correctamente la configuración

# Inicializamos la aplicación Flask
app = Flask(__name__)

# Configurar la aplicación con las configuraciones de config.py
app.config.from_object(Config)

# Crear la instancia de LoginManager
login_manager = LoginManager()
login_manager.login_view = "auth.login"  # Redirige a 'auth.login' si no está autenticado

# Inicializamos la base de datos y el login_manager
db.init_app(app)
login_manager.init_app(app)

# Cargar el usuario a partir del ID
@login_manager.user_loader
def load_user(user_id):
    from models.users import User  # Importar User aquí para evitar un posible error de importación circular
    return User.query.get(int(user_id))  # Recuperar el usuario por su ID

# Importar los blueprints después de la inicialización
app.register_blueprint(auth)
app.register_blueprint(tasks)
app.register_blueprint(admin)

# -------------------------
# 📌 RUTA: PÁGINA PRINCIPAL
# -------------------------
@app.route('/')
def index():
    return render_template('index.html')

# -------------------------
# 📌 RUTA: CERRAR SESIÓN
# -------------------------
@app.route('/logout')
def logout():
    from flask_login import logout_user  # Usar logout_user de Flask-Login para manejar el cierre de sesión
    logout_user()  # Cierra la sesión del usuario
    return redirect(url_for('index'))


# 📌 EJECUTAR LA APLICACIÓN
# -------------------------
if __name__ == '__main__':
    app.run(debug=True)
