# Importamos el objeto db para interactuar con la base de datos de SQLAlchemy
from models import db

# Definimos la clase Contacto, que representará la tabla 'correo' en la base de datos
class Contacto(db.Model):
    # Establecemos el nombre de la tabla que se utilizará en la base de datos
    __tablename__ = 'correo'

    # Establecemos que esta tabla se almacenará en una base de datos específica 'correo_db'
    __bind_key__ = 'correo_db'  # Clave foránea para conectar con la base de datos 'correo_db'

    # Definimos los campos (columnas) que estarán presentes en la tabla 'correo'

    # id: Campo clave primaria que identifica de manera única cada mensaje
    id = db.Column(db.Integer, primary_key=True)

    # nombre: Nombre de la persona que envió el mensaje. Este campo es obligatorio (no puede ser nulo)
    nombre = db.Column(db.String(100), nullable=False)

    # email: Dirección de correo electrónico de la persona que envió el mensaje. También es obligatorio.
    email = db.Column(db.String(100), nullable=False)

    # telefono: Número de teléfono del remitente, si lo proporcionan. Este campo puede ser nulo.
    telefono = db.Column(db.String(20), nullable=True)

    # asunto: Asunto del mensaje, que debe ser una cadena de texto y no puede estar vacío.
    asunto = db.Column(db.String(150), nullable=False)

    # mensaje: El contenido del mensaje, que puede tener texto largo. Este campo también es obligatorio.
    mensaje = db.Column(db.Text, nullable=False)

    # Método especial para representar el objeto de forma legible en el registro de la base de datos
    def __repr__(self):
        # Devolveremos una representación de la instancia con el nombre y el email del contacto
        return f"<Contacto {self.nombre} - {self.email}>"
