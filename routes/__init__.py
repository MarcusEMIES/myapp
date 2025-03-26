from .auth import auth
from .tareas import tasks
from .admin import admin
from routes.servicios import servicioso
from routes.pago import pago
from routes.clientes import cliente_navegando
from routes.reservando import reservamiento  

def init_app(app):
    """Registrar todos los blueprints en la aplicación."""
    app.register_blueprint(auth)
    app.register_blueprint(tasks)
    app.register_blueprint(admin)
    app.register_blueprint(servicioso, url_prefix='/servicios')
    app.register_blueprint(pago)
    app.register_blueprint(cliente_navegando)
    app.register_blueprint(reservamiento)
    