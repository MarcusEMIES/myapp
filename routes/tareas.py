from flask import Blueprint, render_template
from flask_login import login_required

tasks = Blueprint('tasks', __name__)

@tasks.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@tasks.route('/servicios')
def servicios():
    return render_template('servicios.html')

@tasks.route('/formacion')
def formacion():
    return render_template('formacion.html')

@tasks.route('/presets')
def presets():
    return render_template('presets.html')

@tasks.route('/zona_clientes')
@login_required
def zona_clientes():
    return render_template('zona_clientes.html')

@tasks.route("/FAQ's")
def preguntas_frecuentes():
    return render_template('preguntas_frecuentes.html')

@tasks.route("/politicas")
def politicas():
    return render_template('politicas.html')

@tasks.route("/about")
def about():
    return render_template('about.html')

@tasks.route("/Contacto")
def contacto():
    return render_template('contacto.html')

# @tasks.route("/cCches")
# def coches():
#     return render_template('portafolios/coches.html')

# @tasks.route("/Retrato_Masculino")
# def retratoh():
#     return render_template('portafolios/retratosh.html')

# @tasks.route("/Retrato_Femenino")
# def retratosm():
#     return render_template('portafolios/retratosm.html')

# @tasks.route("/Bodas")
# def bodas():
#     return render_template('portafolios/bodas.html')

# @tasks.route("/Urbana")
# def urbana():
#     return render_template('portafolios/urbana.html')

@tasks.route("/Portafolio")
def portafolio():
    return render_template('portafolio.html')
