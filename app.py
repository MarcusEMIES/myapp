from flask import Flask, render_template
from config import Config
from models import db, login_manager
from routes import init_app
from models.users import User
from flask_migrate import Migrate



app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
login_manager.init_app(app)
migrate = Migrate(app, db) 

init_app(app)

# Función user_loader que Flask-Login necesita para cargar al usuario
@login_manager.user_loader
def load_user(user_id):
    # Devuelve el usuario de la base de datos que tiene el id proporcionado
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

# Crear la base de datos si no existe
with app.app_context():
    db.create_all()  # Crea las tablas si no existen

if __name__ == '__main__':
    app.run(debug=True)
