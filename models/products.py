# Importamos el objeto db para interactuar con la base de datos de SQLAlchemy
from models import db

# Definimos la clase Product, que representará la tabla 'products' en la base de datos
class Product(db.Model):
    # Establecemos el nombre de la tabla que se utilizará en la base de datos
    __tablename__ = 'products'

    # Esta tabla se almacenará en la base de datos vinculada con el bind 'products_db'
    __bind_key__ = 'products_db'

    # id: Campo clave primaria que identifica de manera única cada producto
    id = db.Column(db.Integer, primary_key=True)

    # name: Nombre del producto, debe ser único y no puede ser nulo
    name = db.Column(db.String(100), unique=True, nullable=False)

    # description: Descripción del producto, puede ser nula si no hay descripción
    description = db.Column(db.Text, nullable=True)

    # price: El precio del producto, debe ser un valor numérico y no puede ser nulo
    price = db.Column(db.Float, nullable=False)

    # stock: Unidades disponibles. Por defecto, 0
    stock = db.Column(db.Integer, default=0, nullable=False)

    # image_url: URL de una imagen del producto (ya no obligatorio si usamos múltiples)
    image_url = db.Column(db.String(255), nullable=True)

    # video_url: URL de un video del producto (ya no obligatorio si usamos múltiples)
    video_url = db.Column(db.String(255), nullable=True)

    # user_id: Relación con el usuario al que se le asigna el producto
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # ✅ NUEVOS CAMPOS:

    # image_urls: Múltiples imágenes separadas por ';'
    image_urls = db.Column(db.Text, nullable=True)

    # video_urls: Múltiples videos separados por ';'
    video_urls = db.Column(db.Text, nullable=True)

    # contraseña_producto: Contraseña personalizada para acceder al portafolio del producto
    contraseña_producto = db.Column(db.String(255), nullable=True)

    # Representación legible del producto
    def __repr__(self):
        return f"<Product {self.name}>"
