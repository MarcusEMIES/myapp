# Importamos el objeto db para interactuar con la base de datos de SQLAlchemy
from models import db

# Definimos la clase Reserva, que representará la tabla 'reserva' en la base de datos
class Reserva(db.Model):
    __tablename__ = 'reserva'  # Nombre de la tabla en la base de datos
    __bind_key__ = 'reserva_db'  # Establecemos que esta tabla está asociada a la conexión de base de datos 'reserva_db'

    # Definimos los campos (columnas) que estarán presentes en la tabla 'reserva'

    # id: Campo clave primaria que identifica de manera única cada reserva
    id = db.Column(db.Integer, primary_key=True)

    # nombre: El nombre del usuario que realiza la reserva
    nombre = db.Column(db.String(100), nullable=False)  # No puede ser nulo

    # correo: El correo electrónico del usuario que realiza la reserva
    correo = db.Column(db.String(100), nullable=False)  # No puede ser nulo

    # fecha_hora: La fecha y hora de la reserva (campo de tipo DateTime)
    fecha_hora = db.Column(db.DateTime, nullable=False)  # No puede ser nulo

    # creado_en: Fecha en la que se creó la reserva, por defecto es el timestamp actual
    creado_en = db.Column(db.DateTime, default=db.func.current_timestamp())

    # lugar: El lugar donde se realizará la sesión (puede ser un estudio, un lugar en exterior, etc.)
    lugar = db.Column(db.String(255), nullable=False)  # No puede ser nulo

    # tipo_sesion: Tipo de sesión (puede ser "sesión en estudio", "sesión en exterior", etc.)
    tipo_sesion = db.Column(db.String(100), nullable=False)  # No puede ser nulo

    # description: Descripción adicional de la reserva (opcional)
    description = db.Column(db.Text, nullable=True)  # Puede ser nulo

    # precio: El precio de la reserva (por ejemplo, precio de la sesión)
    precio = db.Column(db.Float, nullable=False)  # No puede ser nulo

    # disponibilidad: Número de plazas disponibles para el servicio reservado
    disponibilidad = db.Column(db.Integer, default=0, nullable=False)  # Por defecto, la disponibilidad es 0 (sin plazas disponibles)

    # image_url: URL de la imagen asociada a la reserva (si corresponde)
    image_url = db.Column(db.String(255), nullable=True)  # Puede ser nulo

    # Relación con la tabla de usuarios, indicando qué usuario realizó la reserva
    user_id = db.Column(db.Integer, nullable=False)  # Referencia al ID del usuario que hizo la reserva

    # Método especial para representar el objeto de forma legible en el registro de la base de datos
    def __repr__(self):
        return f"<Reserva {self.nombre} en {self.fecha_hora}>"
