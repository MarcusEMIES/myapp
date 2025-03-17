from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from models import db

# Definición de roles como constantes
ROLE_USER = 'user'
ROLE_ADMIN = 'admin'
ROLE_MODERATOR = 'moderator'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    # Campos opcionales que pueden ser editados más tarde
    nombre = db.Column(db.String(120), nullable=True)
    apellidos = db.Column(db.String(120), nullable=True)
    telefono = db.Column(db.String(20), nullable=True)
    direccion = db.Column(db.String(255), nullable=True)
    ciudad = db.Column(db.String(120), nullable=True)
    pais = db.Column(db.String(120), nullable=True)
    foto = db.Column(db.String(255), nullable=True)
    role = db.Column(db.String(80), default='user', nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    # Métodos adicionales
    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        """Establece la contraseña cifrada."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verifica la contraseña cifrada."""
        return check_password_hash(self.password_hash, password)
