from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Instancia de la base de datos
db = SQLAlchemy()

# Inicializa el manejador de Login
login_manager = LoginManager()
login_manager.login_view = 'auth.login'  # Redirige a la vista de login
