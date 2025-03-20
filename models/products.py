from models import db

class Product(db.Model):
    __tablename__ = 'products'
    __bind_key__ = 'products_db'  # Esto asegura que se almacenará en 'products.db'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0, nullable=False)
    image_url = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f"<Product {self.name}>"
