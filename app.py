# app.py

from flask import Flask, render_template
from config import Config
from models import db, login_manager
from routes import init_app
from models.users import User
from flask_migrate import Migrate
import os

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
    return render_template('index.html')

# Asegúrate de que las migraciones estén configuradas correctamente
if __name__ == '__main__':
    app.run(debug=True)
