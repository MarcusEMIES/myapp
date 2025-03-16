# models/users.py
from werkzeug.security import generate_password_hash, check_password_hash
from . import db  # Importa la instancia db desde __init__.py
from flask_login import UserMixin  # Importa UserMixin de flask_login

class User(UserMixin, db.Model):  # Heredamos de UserMixin para que tenga los métodos necesarios de Flask-Login
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='user')
    foto = db.Column(db.String(255), nullable=True)
    is_active = db.Column(db.Boolean, default=True)  # Añadimos el atributo is_active

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Puedes agregar otros métodos necesarios, si los requieres.
