#users.py

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from models import db  # Asegúrate de que db esté configurado correctamente en tu app


# Definición de la clase User, que representa a un usuario en el sistema
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    # __bind_key__ = 'users_db'  # 🔥 Agrega esto para asegurarte de que usa la DB correcta

  

    # Definición de la columna 'id' que es la clave primaria de la tabla
    id = db.Column(db.Integer, primary_key=True)
    
    # Definición de la columna 'username' (nombre de usuario), que debe ser único y no puede ser nulo
    username = db.Column(db.String(80), unique=True, nullable=False)
    
    # Definición de la columna 'email' (correo electrónico), que debe ser único y no puede ser nulo
    email = db.Column(db.String(120), unique=True, nullable=False)
    
    # Definición de la columna 'password_hash' que guardará la contraseña cifrada del usuario
    password_hash = db.Column(db.String(128), nullable=False)

    # Campos opcionales que pueden ser editados más tarde
    nombre = db.Column(db.String(120), nullable=True)    # Nombre del usuario
    apellidos = db.Column(db.String(120), nullable=True)  # Apellidos del usuario
    telefono = db.Column(db.String(20), nullable=True)    # Teléfono del usuario
    direccion = db.Column(db.String(255), nullable=True)  # Dirección del usuario
    ciudad = db.Column(db.String(120), nullable=True)     # Ciudad del usuario
    pais = db.Column(db.String(120), nullable=True)       # País del usuario
    foto = db.Column(db.String(255), nullable=True)       # Foto del usuario (se guarda como ruta)
    role = db.Column(db.String(80), default='user', nullable=True)  # Rol del usuario, por defecto 'user'
    is_active = db.Column(db.Boolean, default=True, nullable=False)  # Estado del usuario (activo o no)

    # Método para representar la clase 'User' como un string
    def __repr__(self):
        return f'<User {self.username}>'

    # Método para establecer la contraseña cifrada del usuario
    def set_password(self, password):
        """Establece la contraseña cifrada."""
        self.password_hash = generate_password_hash(password)  # Usa la función para generar un hash de la contraseña

    # Método para verificar si la contraseña proporcionada coincide con el hash almacenado
    def check_password(self, password):
        """Verifica la contraseña cifrada."""
        return check_password_hash(self.password_hash, password)  # Compara la contraseña cifrada con el hash almacenado

    # Métodos de clase

    @classmethod
    def create_user(cls, username, email, password, **kwargs):
        """Crea un nuevo usuario y lo guarda en la base de datos."""
        user = cls(username=username, email=email)  # Crea una instancia de 'User' con el nombre de usuario y correo
        user.set_password(password)  # Establece la contraseña cifrada
        for key, value in kwargs.items():
            setattr(user, key, value)  # Asigna cualquier campo adicional que se pase en kwargs (como nombre, apellidos, etc.)
        db.session.add(user)  # Agrega el usuario a la sesión de la base de datos
        db.session.commit()  # Guarda los cambios en la base de datos
        return user  # Retorna el usuario creado

    @classmethod
    def get_user_by_id(cls, user_id):
        """Obtiene un usuario por ID."""
        return cls.query.get(user_id)  # Busca un usuario por su ID en la base de datos

    @classmethod
    def get_user_by_username(cls, username):
        """Obtiene un usuario por nombre de usuario."""
        return cls.query.filter_by(username=username).first()  # Busca un usuario por su nombre de usuario

    @classmethod
    def update_user(cls, user_id, **kwargs):
        """Actualiza los detalles del usuario."""
        user = cls.query.get(user_id)  # Busca el usuario por ID
        if user:
            for key, value in kwargs.items():
                setattr(user, key, value)  # Asigna los nuevos valores a los atributos del usuario
            db.session.commit()  # Guarda los cambios en la base de datos
            return user  # Retorna el usuario actualizado
        return None  # Si no encuentra el usuario, retorna None

    @classmethod
    def delete_user(cls, user_id):
        """Elimina un usuario."""
        user = cls.query.get(user_id)  # Busca el usuario por ID
        if user:
            db.session.delete(user)  # Elimina el usuario de la base de datos
            db.session.commit()  # Guarda los cambios en la base de datos
            return True  # Retorna True si se ha eliminado el usuario
        return False  # Retorna False si no se ha encontrado el usuario
