from flask import Blueprint, render_template
from flask_login import login_required

tasks = Blueprint('tasks', __name__)

# Ruta para dashboard
@tasks.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

# Ruta para "servicios"
@tasks.route('/servicios')
@login_required
def servicios():
    return render_template('servicios.html')

# Ruta para "formacion"
@tasks.route('/formacion')
@login_required
def formacion():
    return render_template('formacion.html')

# Ruta para "portafolio"
@tasks.route('/portafolio')
@login_required
def portafolio():
    return render_template('portafolio.html')

# Ruta para "presets"
@tasks.route('/presets')
@login_required
def presets():
    return render_template('presets.html')

# Ruta para "zona_clientes"
@tasks.route('/zona_clientes')
@login_required
def zona_clientes():
    return render_template('zona_clientes.html')
