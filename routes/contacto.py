# routes/contacto.py
import os
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_mail import Mail, Message  # Importa las clases necesarias para enviar correos electrónicos
from dotenv import load_dotenv  # Para cargar variables de entorno desde el archivo .env
from config import Config  # Importa las configuraciones de la app
from models.mensajes import Contacto  # Importa el modelo 'Contacto' para guardar los mensajes
from flask import current_app  # Para acceder a las configuraciones actuales de la aplicación
from models import db  # Importa la instancia de la base de datos para interactuar con ella

# Crear el Blueprint
# Un Blueprint en Flask permite organizar las rutas y funciones en módulos. En este caso, 'cliente_navegando' se refiere a las rutas para clientes navegando por el sitio.
pop = Blueprint('cliente_navegando', __name__, template_folder='templates')

# Cargar el archivo .env para cargar las variables de entorno (como las claves de correo)
load_dotenv()

# Inicializar Flask-Mail para enviar correos
mail = Mail()

@pop.route('/send_email', methods=['GET', 'POST'])
def send_email():
    """
    Esta función maneja la solicitud de envío del formulario de contacto.
    Si la solicitud es POST, se obtiene la información del formulario, 
    se envía un correo y se guarda el mensaje en la base de datos.
    """
    if request.method == 'POST':  # Si la solicitud es POST, se procesa el formulario
        # Recibir los datos del formulario de contacto
        nombre = request.form['nombre']
        email = request.form['email']
        telefono = request.form['telefono']
        asunto = request.form['asunto']
        mensaje = request.form['mensaje']

        # Crear el mensaje para enviarlo por correo
        msg = Message(
            subject=f"Nuevo mensaje de contacto: {asunto}",
            recipients=[current_app.config['MAIL_DEFAULT_SENDER']],  # Correo a donde se envía el mensaje (configurado en Config)
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
            # Enviar el correo con el mensaje
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
            db.session.add(nuevo_mensaje)  # Añade el mensaje a la sesión de la base de datos
            db.session.commit()  # Guarda los cambios en la base de datos

            return redirect(url_for('cliente_navegando.contacto'))  # Redirige al formulario de contacto después de enviar

        except Exception as e:
            # Si ocurre un error al enviar el correo
            flash("Hubo un error al enviar el mensaje. Intenta nuevamente más tarde.", "danger")
            return redirect(url_for('cliente_navegando.contacto'))  # Redirige al formulario de contacto en caso de error

    return render_template('contacto.html')  # Si la solicitud es GET, muestra el formulario de contacto
