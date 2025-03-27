# Importación de módulos necesarios
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_mail import Message  # Se importa para el envío de correos si es necesario
import requests  # Se usa para hacer solicitudes HTTP, como el envío de datos a una API externa
from models.mensajes import Contacto  # Importa el modelo 'Contacto' para almacenar los mensajes en la base de datos

# Crear el Blueprint
# Un Blueprint permite organizar las rutas en un módulo. Aquí 'cliente_navegando' se utiliza para rutas relacionadas con los clientes.
cliente_navegando = Blueprint('cliente_navegando', __name__, template_folder='templates')

# Ruta para mostrar el portafolio
@cliente_navegando.route('/portafolio')
def portafolio():
    """
    Esta ruta se usa para mostrar el portafolio de la página web.
    Se renderiza una plantilla HTML ubicada en 'portafolios/portafolio_cliente.html'.
    """
    return render_template('portafolios/portafolio_cliente.html')

# Ruta para el formulario de contacto
@cliente_navegando.route('/contacto', methods=['POST'])
def contacto():
    """
    Esta ruta maneja el formulario de contacto. Si el formulario es enviado mediante POST, 
    recoge los datos, los envía a una API externa y muestra un mensaje de éxito o error.
    """
    if request.method == 'POST':  # Si el formulario es enviado mediante POST
        # Recoger los datos enviados desde el formulario
        datos = {
            "nombre": request.form.get('nombre'),
            "email": request.form.get('email'),
            "telefono": request.form.get('telefono', ''),  # Si no se proporciona un teléfono, se establece como cadena vacía
            "asunto": request.form.get('asunto'),
            "mensaje": request.form.get('mensaje')
        }

        # Enviar los datos a una API externa, en este caso un ejemplo de URL de API
        url_api = "https://api.ejemplo.com/contacto"
        response = requests.post(url_api, json=datos)  # Se realiza una solicitud POST a la API externa con los datos

        # Comprobar si la respuesta de la API es exitosa (status code 200)
        if response.status_code == 200:
            flash("¡Mensaje enviado correctamente!", "success")  # Muestra un mensaje de éxito en el formulario
        else:
            flash("Hubo un error al enviar el mensaje.", "error")  # Muestra un mensaje de error si la API devuelve un error

        # Redirigir al usuario de vuelta a la página de contacto
        return redirect(url_for('cliente_navegando.contacto'))

    # Si la solicitud es GET, simplemente renderiza el formulario de contacto
    return render_template('contacto.html')
