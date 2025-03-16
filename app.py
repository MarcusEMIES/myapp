from flask import Flask, render_template
from routes.auth import auth  # Blueprint para autenticación
from routes.tareas import tasks  # Blueprint para tareas
from models import db  # Importar la base de datos
from config import Config  # Importar configuración
from flask_migrate import Migrate  # Importar Migrate para migraciones
from routes.portafolios import portafolios
# Inicialización de la aplicación
app = Flask(__name__)

# Cargar configuración desde el archivo config.py
app.config.from_object(Config) 

# Inicialización de la base de datos
db.init_app(app)

# Inicialización de Flask-Migrate para migraciones
migrate = Migrate(app, db)

# Registrar los blueprints para las rutas de autenticación y tareas
app.register_blueprint(auth)
app.register_blueprint(tasks)
app.register_blueprint(portafolios)

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
