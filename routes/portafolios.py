from flask import Blueprint, render_template

# Crear un Blueprint llamado "portafolios" con la ruta de la carpeta de plantillas correcta
portafolios = Blueprint('portafolios', __name__, template_folder='templates/portafolios')

# Rutas para cada portfolio
@portafolios.route('/Coches')
def coches():
    return render_template('coches.html')  # plantilla en templates/portafolios/coches.html

@portafolios.route('/Retratos')
def retratos():
    return render_template('retratos.html')  # plantilla en templates/portafolios/retratos.html

@portafolios.route('/Comida')
def comida():
    return render_template('comida.html')  # plantilla en templates/portafolios/comida.html

@portafolios.route('/Bodas')
def bodas():
    return render_template('bodas.html')  # plantilla en templates/portafolios/bodas.html

@portafolios.route('/Urbana')
def urbana():
    return render_template('urbana.html')  # plantilla en templates/portafolios/urbana.html
