from models import db

class Reserva(db.Model):
    __tablename__ = 'reserva'
    __bind_key__ = 'reserva_db'  # Conexión a la base de datos correcta

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)  
    correo = db.Column(db.String(100), nullable=False)
    fecha_hora = db.Column(db.DateTime, nullable=False)  # Usamos un solo campo para fecha y hora
    creado_en = db.Column(db.DateTime, default=db.func.current_timestamp())
    lugar = db.Column(db.String(255), nullable=False)
    tipo_sesion = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    precio = db.Column(db.Float, nullable=False)
    disponibilidad = db.Column(db.Integer, default=0, nullable=False)
    image_url = db.Column(db.String(255), nullable=True)

    # Relación con el usuario
    user_id = db.Column(db.Integer, nullable=False)  

    def __repr__(self):
        return f"<Reserva {self.nombre} en {self.fecha_hora}>"
