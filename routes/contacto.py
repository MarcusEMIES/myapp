# routes/contacto.py
import os
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_mail import Mail, Message
from dotenv import load_dotenv
from config import Config
from models.mensajes import Contacto
from flask import current_app
from models import db
# Crear el Blueprint
pop = Blueprint('cliente_navegando', __name__, template_folder='templates')

# Cargar el archivo .env
load_dotenv()

# Inicializar Flask-Mail
mail = Mail()

@pop.route('/send_email', methods=['GET', 'POST'])
def send_email():
    if request.method == 'POST':
        # Recibir los datos del formulario de contacto
        nombre = request.form['nombre']
        email = request.form['email']
        telefono = request.form['telefono']
        asunto = request.form['asunto']
        mensaje = request.form['mensaje']

        # Crear el mensaje para enviarlo por correo
        msg = Message(
            subject=f"Nuevo mensaje de contacto: {asunto}",
            recipients=[current_app.config['MAIL_DEFAULT_SENDER']],  # Aquí va tu correo para recibir los mensajes
            body=f"""
            Nombre: {nombre}
            Correo: {email}
            Teléfono: {telefono}
            Asunto: {asunto}

            Mensaje:
            {mensaje}
            """
        )

        try:
            # Enviar el correo
            mail.send(msg)
            flash("Mensaje enviado con éxito, nos pondremos en contacto contigo pronto.", "success")

            # Guardar el mensaje en la base de datos
            nuevo_mensaje = Contacto(
                nombre=nombre,
                email=email,
                telefono=telefono,
                asunto=asunto,
                mensaje=mensaje
            )
            db.session.add(nuevo_mensaje)
            db.session.commit()

            return redirect(url_for('cliente_navegando.contacto'))  # Redirige al formulario de contacto

        except Exception as e:
            # Si ocurre un error al enviar el correo
            flash("Hubo un error al enviar el mensaje. Intenta nuevamente más tarde.", "danger")
            return redirect(url_for('cliente_navegando.contacto'))

    return render_template('contacto.html')  # Aquí renderizas tu formulario de contacto
