# Importación de módulos necesarios de Flask para gestionar rutas, plantillas y la sesión.
from flask import Blueprint, render_template
# Importación de las funciones necesarias de Flask-Login para gestionar sesiones de usuario.
from flask_login import login_required, logout_user
# Importación de 'datetime' para trabajar con tiempos y fechas, en este caso, para manejar la expiración de la sesión.
from datetime import datetime
# Importación de funciones para manejar redirecciones, URLs y flash messages (mensajes temporales).
from flask import redirect, url_for, session, flash

# Se crea un Blueprint para agrupar todas las rutas relacionadas con las "tareas" o secciones de la aplicación.
tasks = Blueprint('tasks', __name__)

# Ruta para el dashboard, donde solo los usuarios autenticados pueden acceder (gracias al decorador @login_required).
@tasks.route('/dashboard')
@login_required  # Este decorador asegura que solo los usuarios logueados puedan acceder a esta página.
def dashboard():
    # Renderiza la plantilla HTML llamada 'dashboard.html' cuando se accede a esta ruta.
    return render_template('dashboard.html')

# Ruta para la sección de 'servicios', disponible para todos los usuarios.
@tasks.route('/servicios')
def servicios():
    # Renderiza la plantilla 'servicios.html' cuando se accede a esta ruta.
    return render_template('servicios.html')

# Ruta para la sección de 'formación', disponible para todos los usuarios.
@tasks.route('/formacion')
def formacion():
    # Renderiza la plantilla 'formacion.html' cuando se accede a esta ruta.
    return render_template('formacion.html')

# Ruta para la sección de 'presets', disponible para todos los usuarios.
@tasks.route('/presets')
def presets():
    # Renderiza la plantilla 'presets.html' cuando se accede a esta ruta.
    return render_template('presets.html')

# Ruta para la zona de clientes, que solo está disponible para usuarios autenticados.
@tasks.route('/zona_clientes')
@login_required  # Este decorador asegura que solo los usuarios logueados puedan acceder a esta página.
def zona_clientes():
    # Renderiza la plantilla 'zona_clientes.html' cuando se accede a esta ruta.
    return render_template('zona_clientes.html')

# Ruta para las preguntas frecuentes (FAQ), disponible para todos los usuarios.
@tasks.route("/FAQ's")
def preguntas_frecuentes():
    # Renderiza la plantilla 'preguntas_frecuentes.html' cuando se accede a esta ruta.
    return render_template('preguntas_frecuentes.html')

# Ruta para las políticas de privacidad, disponible para todos los usuarios.
@tasks.route("/politicas")
def politicas():
    # Renderiza la plantilla 'politicas.html' cuando se accede a esta ruta.
    return render_template('politicas.html')

# Ruta para la sección "Sobre nosotros" (about), disponible para todos los usuarios.
@tasks.route("/about")
def about():
    # Renderiza la plantilla 'about.html' cuando se accede a esta ruta.
    return render_template('about.html')

# Ruta para la sección de contacto, disponible para todos los usuarios.
@tasks.route("/Contacto")
def contacto():
    # Renderiza la plantilla 'contacto.html' cuando se accede a esta ruta.
    return render_template('contacto.html')

# Ruta para la sección de portafolios, en este caso, para el portafolio de 'Coches'.
@tasks.route("/Coches")
def coches():
    # Renderiza la plantilla 'portafolios/coches.html' cuando se accede a esta ruta.
    return render_template('portafolios/coches.html')

# Ruta para la sección de portafolios, en este caso, para el 'Retrato Masculino'.
@tasks.route("/Retrato_Masculino")
def retratosh():
    # Renderiza la plantilla 'portafolios/retratosh.html' cuando se accede a esta ruta.
    return render_template('portafolios/retratosh.html')

# Ruta para la sección de portafolios, en este caso, para el 'Retrato Femenino'.
@tasks.route("/Retrato_Femenino")
def retratosm():
    # Renderiza la plantilla 'portafolios/retratosm.html' cuando se accede a esta ruta.
    return render_template('portafolios/retratosm.html')

# Ruta para la sección de portafolios, en este caso, para 'Bodas'.
@tasks.route("/Bodas")
def bodas():
    # Renderiza la plantilla 'portafolios/bodas.html' cuando se accede a esta ruta.
    return render_template('portafolios/bodas.html')

# Ruta para la sección de portafolios, en este caso, para 'Urbana'.
@tasks.route("/Urbana")
def urbana():
    # Renderiza la plantilla 'portafolios/urbana.html' cuando se accede a esta ruta.
    return render_template('portafolios/urbana.html')

# Ruta para la página principal del portafolio, disponible para todos los usuarios.
@tasks.route("/Portafolio")
def portafolio():
    # Renderiza la plantilla 'portafolio.html' cuando se accede a esta ruta.
    return render_template('portafolio.html')

# Ruta para la sección de 'Comida' en el portafolio, disponible para todos los usuarios.
@tasks.route("/comida")
def comida():
    # Renderiza la plantilla 'portafolios/comida.html' cuando se accede a esta ruta.
    return render_template('portafolios/comida.html')

# Ruta para los productos, en este caso, 'Mis Productos', disponible para todos los usuarios.
@tasks.route("/Mis Productos")
def productos():
    # Renderiza la plantilla 'productos/productos1.html' cuando se accede a esta ruta.
    return render_template('productos/productos1.html')

# Ruta para un video (aclog.html) que se muestra en esta página.
@tasks.route('/video')
def video():
    # Renderiza la plantilla 'aclog.html', que incluye el video.
    return render_template('aclog.html')

# Controlador de Sesiones: Función decoradora para verificar la expiración de la sesión.
# Este decorador es usado para comprobar si la sesión del usuario ha expirado antes de permitirle acceder a ciertas rutas.

def check_session_expiration(func):
    # Función que envuelve a la función original para añadir la verificación de la expiración de la sesión.
    def wrapper(*args, **kwargs):
        # Verifica si la clave 'expires' existe en la sesión.
        if 'expires' in session:
            # Convierte el valor de 'expires' (que debe estar en formato ISO) a un objeto datetime.
            expiration_time = datetime.fromisoformat(session['expires'])
            # Si la hora actual es mayor que la hora de expiración, se cierra la sesión.
            if datetime.now() > expiration_time:
                # Cierra la sesión del usuario.
                logout_user()
                # Muestra un mensaje flash indicando que la sesión ha expirado.
                flash("Tu sesión ha expirado. Por favor, inicia sesión de nuevo.", "danger")
                # Redirige al usuario al formulario de login si la sesión ha expirado.
                return redirect(url_for('auth.login'))  
        # Si la sesión no ha expirado, ejecuta la función original (la ruta correspondiente).
        return func(*args, **kwargs)
    return wrapper  # Retorna el decorador.
