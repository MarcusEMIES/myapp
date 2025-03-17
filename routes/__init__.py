from .auth import auth
from .tareas import tasks
from .portafolios import portafolios
from .admin import admin

def init_app(app):
    """Registrar todos los blueprints en la aplicación."""
    app.register_blueprint(auth)
    app.register_blueprint(tasks)
    app.register_blueprint(portafolios)
    app.register_blueprint(admin)
