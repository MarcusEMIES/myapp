from flask import Flask, render_template
from models import db, init_app
from routes.auth import auth
from flask_login import login_required
from config import config
# Crear la aplicación Flask
app = Flask(__name__)

# Cargar configuración desde Config.py
app.config.from_object(config['desarrollo'])  # O 'produccion'

# Inicializar las extensiones y la base de datos
init_app(app)

# Registrar el Blueprint de autenticación
app.register_blueprint(auth)

# Ruta principal
@app.route('/')
def index():
    return render_template('index.html')


# Ruta protegida por login
@app.route('/dashboard')

def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)
