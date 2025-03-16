#Condifuracion de la base de datos models/__init__.py
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

# Instancia de la base de datos
db = SQLAlchemy()
# Inicializa las extensiones
