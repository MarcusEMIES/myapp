from models import db

class Reserva(db.Model):
    __tablename__ = 'reserva'
    __bind_key__ = 'reserva_db'  # Esto asegura que se almacenará en reserva.db
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0, nullable=False)
    image_url = db.Column(db.String(255), nullable=True)
    
    # Nuevos campos
    fecha = db.Column(db.Date, nullable=False)
    hora = db.Column(db.Time, nullable=False)
    lugar = db.Column(db.String(255), nullable=False)
    tipo_sesion = db.Column(db.String(100), nullable=False)
    
    def __repr__(self):
        return f"<Reserva {self.name}>"