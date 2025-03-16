from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from .users import User


# Instancias de las extensiones
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

# Función de carga de usuario (user_loader)
@login_manager.user_loader
def load_user(user_id):
    from models.users import User  # Importar el modelo User aquí para evitar importación circular
    return User.query.get(int(user_id))

# Función para inicializar las extensiones con la app
def init_app(app):
    db.init_app(app)  # Inicializar SQLAlchemy con la app
    login_manager.init_app(app)  # Inicializar Flask-Login con la app
    migrate.init_app(app, db)  # Inicializar Flask-Migrate con la app y la base de datos
