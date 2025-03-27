# Importamos SQLAlchemy para interactuar con la base de datos de forma ORM
from flask_sqlalchemy import SQLAlchemy

# Importamos LoginManager para manejar la autenticación de usuarios con Flask-Login
from flask_login import LoginManager

# Instanciamos el objeto db que nos permitirá interactuar con la base de datos usando SQLAlchemy.
# Esto creará una conexión a la base de datos, y permitirá definir modelos (tablas), realizar consultas, insertar datos, etc.
db = SQLAlchemy()

# Inicializamos el manejador de Login, que es una herramienta que nos ayuda a gestionar la autenticación de usuarios.
# Flask-Login proporciona sesiones de usuario de manera sencilla y se encarga de muchas de las tareas relacionadas con el manejo de usuarios.
login_manager = LoginManager()

# Especificamos cuál es la vista que se debe mostrar cuando un usuario no autenticado intenta acceder a una página protegida.
# En este caso, se redirige a la vista 'auth.login', que generalmente corresponde a la página de inicio de sesión.
login_manager.login_view = 'auth.login'
