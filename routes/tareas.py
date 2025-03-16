from flask import Blueprint, render_template
from flask_login import login_required

tasks = Blueprint('tasks', __name__)

# Ruta para dashboard


@tasks.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# Ruta para "servicios"


@tasks.route('/servicios')
def servicios():
    return render_template('servicios.html')

# Ruta para "formacion"


@tasks.route('/formacion')
def formacion():
    return render_template('formacion.html')

# Ruta para "portafolio"


@tasks.route('/portafolio')
def portafolio():
    return render_template('portafolio.html')

# Ruta para "presets"


@tasks.route('/presets')
def presets():
    return render_template('presets.html')

# Ruta para "zona_clientes"


@tasks.route('/zona_clientes')
def zona_clientes():
    return render_template('zona_clientes.html')
