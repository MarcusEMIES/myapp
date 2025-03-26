#mensajes.py

from models import db

class Contacto(db.Model):
    __tablename__ ='correo'
    __bind_key__ ='correo_db' # Clave Foranea para conectar con la base de datos 
    
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20), nullable=True)
    asunto = db.Column(db.String(150), nullable=False)
    mensaje = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<Contacto {self.nombre} - {self.email}>"
