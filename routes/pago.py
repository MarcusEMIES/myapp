# Importamos las librerías necesarias para el funcionamiento de la ruta de pago
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user  # Para manejar la sesión de usuario y asegurarse de que está autenticado.
import hashlib  # Para realizar operaciones de hash (SHA256).
import hmac  # Para generar la firma con HMAC (función de hash con clave secreta).
import base64  # Para trabajar con codificación y decodificación en base64.
from config import Config  # Importa la clase Config para acceder a las configuraciones del sistema.
from models.reserva import Reserva  # Importa el modelo Reserva en caso de que sea necesario

# Creamos el Blueprint para las rutas de pago
pago = Blueprint('pago', __name__)

# Diccionario que contiene los servicios disponibles y sus precios
SERVICIOS = {
    'sesiones_estudio': {'nombre': 'Sesión en Estudio', 'precio': 80},  # Servicio de sesión en estudio
    'sesiones_exterior': {'nombre': 'Sesión en Exterior', 'precio': 100},  # Servicio de sesión en exterior
    'formacion_fotografia': {'nombre': 'Curso de Fotografía', 'precio': 150},  # Curso de fotografía
}

def generar_redsys_params(servicio, bizum=False):
    """
    Genera los parámetros necesarios para realizar una transacción con Redsys.
    El pago puede ser normal o mediante Bizum.
    """
    # Si el servicio solicitado no existe en el diccionario, retorna None
    if servicio not in SERVICIOS:
        return None, None

    # Datos que se van a enviar a Redsys para realizar el pago
    datos = {
        "DS_MERCHANT_AMOUNT": str(SERVICIOS[servicio]['precio'] * 100),  # Monto en céntimos (por eso multiplicamos por 100)
        "DS_MERCHANT_CURRENCY": "978",  # Código de moneda para EUR (Euro)
        "DS_MERCHANT_ORDER": "123456789",  # Número de pedido único, en la práctica, debería ser dinámico
        "DS_MERCHANT_MERCHANTCODE": Config.REDSYS_MERCHANT_CODE,  # Código del comercio (configurado en el archivo de configuración)
        "DS_MERCHANT_TERMINAL": Config.REDSYS_TERMINAL,  # Terminal del comercio (configurado en el archivo de configuración)
        "DS_MERCHANT_TRANSACTIONTYPE": "0",  # Tipo de transacción: "0" para compra normal
        "DS_MERCHANT_URLOK": url_for("pago.pago_exitoso", servicio=servicio, _external=True),  # URL a la que Redsys redirige si el pago es exitoso
        "DS_MERCHANT_URLKO": url_for("pago.pago_fallido", _external=True),  # URL a la que Redsys redirige si el pago falla
    }

    # Si se está utilizando Bizum, se agrega el parámetro correspondiente
    if bizum:
        datos["DS_MERCHANT_BIZUM"] = "1"  # Activa el pago mediante Bizum

    # Corregir el padding de la clave secreta antes de decodificarla (para asegurar que tenga un tamaño adecuado)
    clave_secreta = Config.REDSYS_SECRET_KEY
    faltante = len(clave_secreta) % 4
    if faltante:
        clave_secreta += "=" * (4 - faltante)  # Agrega el padding necesario

    # Convertimos la clave secreta de base64 a bytes
    clave_bytes = base64.b64decode(clave_secreta)
    # Unimos todos los parámetros en un string, separados por "|"
    mensaje = '|'.join(datos.values()).encode()
    # Generamos la firma HMAC (hash) con la clave secreta y el mensaje concatenado
    signature = base64.b64encode(hmac.new(clave_bytes, mensaje, hashlib.sha256).digest()).decode()

    # Retorna los parámetros y la firma generada
    return datos, signature

# Ruta para revisar el pago antes de proceder (muestra un resumen de la compra)
@pago.route("/revisar_pago/<servicio>", methods=["GET"])
@login_required  # Asegura que el usuario esté autenticado antes de acceder
def revisar_pago(servicio):
    """Muestra la página de revisión de la compra antes de proceder al pago."""
    # Si el servicio no existe en el diccionario, redirige a la página de servicios
    if servicio not in SERVICIOS:
        flash("El servicio seleccionado no existe.", "danger")
        return redirect(url_for('tasks.servicios'))

    # Obtiene los detalles del servicio que el usuario está comprando
    servicio_details = SERVICIOS.get(servicio)
    # Renderiza la plantilla para la revisión del pago con los detalles del servicio
    return render_template("pago/pago.html", servicio=servicio_details)

# Ruta para realizar el pago con tarjeta mediante Redsys
@pago.route('/pago_redsys/<servicio>', methods=['GET'])
@login_required
def pagar_redsys(servicio):
    """Realiza el pago a través de Redsys con tarjeta."""
    # Generar los parámetros para el pago usando la función 'generar_redsys_params'
    params, firma = generar_redsys_params(servicio)
    if not params:
        flash("El servicio seleccionado no existe.", "danger")
        return redirect(url_for('tasks.servicios'))  # Redirige a la página de servicios si el servicio no existe

    # Obtener los detalles del servicio para pasarlos a la plantilla
    servicio_details = SERVICIOS.get(servicio)
    # Renderiza la plantilla para realizar el pago con los parámetros generados
    return render_template("pago/pago_redsys.html", datos=params, firma=firma, url_redsys=Config.REDSYS_URL, servicio=servicio_details)

# Ruta para realizar el pago con Bizum mediante Redsys
@pago.route('/pago_bizum/<servicio>', methods=['GET'])
@login_required
def pagar_bizum(servicio):
    """Realiza el pago a través de Bizum."""
    # Generar los parámetros para el pago con Bizum
    params, firma = generar_redsys_params(servicio, bizum=True)
    if not params:
        flash("El servicio seleccionado no existe.", "danger")
        return redirect(url_for('tasks.servicios'))  # Redirige a la página de servicios si el servicio no existe

    # Obtener los detalles del servicio para pasarlos a la plantilla
    servicio_details = SERVICIOS.get(servicio)
    # Renderiza la plantilla para realizar el pago con los parámetros generados para Bizum
    return render_template("pago/pago_redsys.html", datos=params, firma=firma, url_redsys=Config.REDSYS_URL, servicio=servicio_details)

# Ruta para confirmar que el pago fue exitoso
@pago.route("/confirmar_pago/<servicio>", methods=["POST"])
@login_required
def confirmar_pago(servicio):
    """Confirma el pago y redirige a la página de éxito."""
    # Verifica si el servicio existe en el diccionario
    if servicio not in SERVICIOS:
        flash("El servicio seleccionado no existe.", "danger")
        return redirect(url_for('tasks.servicios'))  # Redirige a la página de servicios si el servicio no existe

    # Mensaje de éxito si el pago se ha realizado correctamente
    flash(f"Pago realizado con éxito para {SERVICIOS[servicio]['nombre']}!", "success")
    # Redirige a la página de éxito del pago
    return redirect(url_for("pago.pago_exitoso", servicio=servicio))

# Ruta para mostrar la página de pago exitoso cuando el pago se ha completado
@pago.route("/pago_exitoso/<servicio>")
@login_required
def pago_exitoso(servicio):
    """Página de éxito cuando el pago se ha completado correctamente."""
    # Verifica si el servicio existe en el diccionario
    if servicio not in SERVICIOS:
        flash("El servicio seleccionado no existe.", "danger")
        return redirect(url_for('tasks.servicios'))  # Redirige a la página de servicios si el servicio no existe

    # Obtiene los detalles del servicio
    detalles = SERVICIOS[servicio]
    # Renderiza la plantilla de éxito con los detalles del servicio
    return render_template("pago/pago_exitoso.html", usuario=current_user, servicio=detalles)

# Ruta para mostrar la página de pago fallido cuando el pago no se completa
@pago.route("/pago_fallido")
def pago_fallido():
    """Página cuando el pago falla."""
    # Mensaje de error si el pago no se pudo completar
    flash("El pago no se pudo completar. Inténtalo nuevamente.", "danger")
    # Redirige a la página de servicios
    return redirect(url_for('tasks.servicios'))
