from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_mail import Message
import requests
from models.mensajes import Contacto

# Crear el Blueprint
cliente_navegando = Blueprint('cliente_navegando', __name__, template_folder='templates')

# Ruta para el portafolio
@cliente_navegando.route('/portafolio')
def portafolio():
    return render_template('portafolios/portafolio_cliente.html')

# Ruta para el formulario de contacto
@cliente_navegando.route('/contacto', methods=['POST'])
def contacto():
    if request.method == 'POST':
        datos = {
            "nombre": request.form.get('nombre'),
            "email": request.form.get('email'),
            "telefono": request.form.get('telefono', ''),
            "asunto": request.form.get('asunto'),
            "mensaje": request.form.get('mensaje')
        }

        # Enviar datos a una API externa (ejemplo: Google Sheets o CRM)
        url_api = "https://api.ejemplo.com/contacto"
        response = requests.post(url_api, json=datos)

        if response.status_code == 200:
            flash("¡Mensaje enviado correctamente!", "success")
        else:
            flash("Hubo un error al enviar el mensaje.", "error")

        return redirect(url_for('cliente_navegando.contacto'))

    return render_template('contacto.html')
