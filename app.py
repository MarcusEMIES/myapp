from flask import Flask, render_template
from routes.auth import auth # Blueprint para autenticación
from routes.tareas import tasks  # Blueprint para tareas
from models import db
from config import Config  # Importar configuración
from flask_migrate import Migrate  # Importar Migrate para migraciones
from routes.portafolios import portafolios
from flask_login import LoginManager 
from models.users import User
from routes.admin import admin


# Inicialización de la aplicación
app = Flask(__name__)

# Cargar configuración desde el archivo config.py
app.config.from_object(Config) 

# Inicialización de la base de datos
db.init_app(app)
# Inicialización de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# Configura la ruta de login (para redirigir al usuario no autenticado)
login_manager.login_view = 'auth.login'
# Definir la función user_loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Inicialización de Flask-Migrate para migraciones
migrate = Migrate(app, db)

# Registrar los blueprints para las rutas de autenticación y tareas
app.register_blueprint(auth)
app.register_blueprint(tasks)
app.register_blueprint(portafolios)
app.register_blueprint(admin)

# Ruta principal
@app.route('/')
def index():
    return render_template('index.html')

# Ruta protegida para el dashboard
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


# # Activar para Eliminar todas las tablas de la base de datos
# db.drop_all()
# #Activar para crear la base de datos
# db.create_all()


# Ejecutar la aplicación en modo de desarrollo
if __name__ == '__main__':
    app.run(debug=True)
