from .auth import auth  # Importa el blueprint 'auth' (autenticación)
from .tareas import tasks  # Importa el blueprint 'tasks' (tareas)
from .admin import admin  # Importa el blueprint 'admin' (administración)
from routes.servicios import servicioso  # Importa el blueprint 'servicioso' (servicios)
from routes.pago import pago  # Importa el blueprint 'pago' (pago)
from routes.clientes import cliente_navegando  # Importa el blueprint 'cliente_navegando' (clientes)
from routes.reservando import reservamiento  # Importa el blueprint 'reservamiento' (reservas)
from routes.portcliente import portafolio


# Aqui definimos los blueprints

def init_app(app):
    """Registrar todos los blueprints en la aplicación."""
    
    # Registra el blueprint 'auth' para manejar autenticación y sesiones de usuario
    app.register_blueprint(auth)
    
    # Registra el blueprint 'tasks' para manejar las tareas
    app.register_blueprint(tasks)
    
    # Registra el blueprint 'admin' para manejar las funcionalidades administrativas
    app.register_blueprint(admin)
    
    # Registra el blueprint 'servicioso' para manejar los servicios, con un prefijo de URL '/servicios'
    app.register_blueprint(servicioso, url_prefix='/servicios')
    
    # Registra el blueprint 'pago' para manejar el proceso de pago
    app.register_blueprint(pago)
    
    # Registra el blueprint 'cliente_navegando' para manejar la navegación de los clientes
    app.register_blueprint(cliente_navegando)
    
    # Registra el blueprint 'reservamiento' para manejar las reservas de los clientes
    app.register_blueprint(reservamiento)
    
    # Registra el blueprint 'portafolio' para manejar las cargas de prductos finales para los clientes
    app.register_blueprint(portafolio)
