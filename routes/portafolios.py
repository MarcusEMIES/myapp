from flask import Blueprint, render_template

portafolios = Blueprint('portafolios', __name__, template_folder='templates/portafolios')

@portafolios.route('/Coches')
def coches():
    return render_template('portafolios/coches.html')

@portafolios.route('/Retratos_Femeninos')
def retratosm():
    return render_template('portafolios/retratosm.html')

@portafolios.route('/Retratos_Masculinos')
def retratosh():
    return render_template('portafolios/retratosh.html')

@portafolios.route('/Comida')
def comida():
    return render_template('portafolios/comida.html')

@portafolios.route('/Bodas')
def bodas():
    return render_template('portafolios/bodas.html')

@portafolios.route('/Urbana')
def urbana():
    return render_template('portafolios/urbana.html')
