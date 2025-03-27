# Importamos el objeto db para interactuar con la base de datos de SQLAlchemy
from models import db

# Definimos la clase Product, que representará la tabla 'products' en la base de datos
class Product(db.Model):
    # Establecemos el nombre de la tabla que se utilizará en la base de datos
    __tablename__ = 'products'

    # Establecemos que esta tabla se almacenará en una base de datos específica 'products_db'
    __bind_key__ = 'products_db'

    # Definimos los campos (columnas) que estarán presentes en la tabla 'products'

    # id: Campo clave primaria que identifica de manera única cada producto
    id = db.Column(db.Integer, primary_key=True)

    # name: Nombre del producto, debe ser único y no puede ser nulo
    name = db.Column(db.String(100), unique=True, nullable=False)

    # description: Descripción del producto, puede ser nula si no hay descripción
    description = db.Column(db.Text, nullable=True)

    # price: El precio del producto, debe ser un valor numérico y no puede ser nulo
    price = db.Column(db.Float, nullable=False)

    # stock: El número de unidades disponibles del producto. Por defecto, se inicializa a 0 si no se especifica
    stock = db.Column(db.Integer, default=0, nullable=False)

    # image_url: La URL de la imagen del producto, si existe. Puede ser nula si no se proporciona una imagen
    image_url = db.Column(db.String(255), nullable=True)

    # Método especial para representar el objeto de forma legible en el registro de la base de datos
    def __repr__(self):
        return f"<Product {self.name}>"
