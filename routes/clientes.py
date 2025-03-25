# clientes.py
from flask import Blueprint, render_template

# Crear el Blueprint
cliente_navegando = Blueprint('cliente_navegando', __name__, template_folder='templates')

# Definir la ruta para el portafolio
@cliente_navegando.route('/portafolio')
def portafolio():
    return render_template('portafolios/portafolio_cliente.html')
