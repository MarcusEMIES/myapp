from app import app
from models import db

# Crear un contexto de aplicación
with app.app_context():
    db.drop_all()  # Esto eliminará todas las tablas de la base de datos
    print("Base de datos eliminada correctamente.")


# Si quieres eliminar la base de datos ejecuta en la consola python eliminardb.py