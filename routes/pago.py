from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
import hashlib
import hmac
import base64
from config import Config  # Importa la clase Config correctamente
from models.reserva import Reserva

pago = Blueprint('pago', __name__)

# Diccionario de servicios con sus precios
SERVICIOS = {
    'sesiones_estudio': {'nombre': 'Sesión en Estudio', 'precio': 80},
    'sesiones_exterior': {'nombre': 'Sesión en Exterior', 'precio': 100},
    'formacion_fotografia': {'nombre': 'Curso de Fotografía', 'precio': 150},
}

def generar_redsys_params(servicio, bizum=False):
    """Genera los parámetros para Redsys con o sin Bizum."""
    if servicio not in SERVICIOS:
        return None, None

    datos = {
        "DS_MERCHANT_AMOUNT": str(SERVICIOS[servicio]['precio'] * 100),  # En céntimos (€)
        "DS_MERCHANT_CURRENCY": "978",  # Código de moneda para EUR
        "DS_MERCHANT_ORDER": "123456789",  # Generar un número único para cada pedido
        "DS_MERCHANT_MERCHANTCODE": Config.REDSYS_MERCHANT_CODE,
        "DS_MERCHANT_TERMINAL": Config.REDSYS_TERMINAL,
        "DS_MERCHANT_TRANSACTIONTYPE": "0",  # Compra normal
        "DS_MERCHANT_URLOK": url_for("pago.pago_exitoso", servicio=servicio, _external=True),
        "DS_MERCHANT_URLKO": url_for("pago.pago_fallido", _external=True),
    }

    if bizum:
        datos["DS_MERCHANT_BIZUM"] = "1"  # Si es pago con Bizum

    # Corregir el padding de la clave secreta antes de decodificar
    clave_secreta = Config.REDSYS_SECRET_KEY
    faltante = len(clave_secreta) % 4
    if faltante:
        clave_secreta += "=" * (4 - faltante)

    clave_bytes = base64.b64decode(clave_secreta)
    mensaje = '|'.join(datos.values()).encode()  # Unir los datos con '|'
    signature = base64.b64encode(hmac.new(clave_bytes, mensaje, hashlib.sha256).digest()).decode()

    return datos, signature

# Ruta para la revisión del pago antes de proceder
@pago.route("/revisar_pago/<servicio>", methods=["GET"])
@login_required
def revisar_pago(servicio):
    """Muestra la página de revisión de la compra antes de proceder al pago."""
    if servicio not in SERVICIOS:
        flash("El servicio seleccionado no existe.", "danger")
        return redirect(url_for('tasks.servicios'))  # Redirigir a la página de servicios

    servicio_details = SERVICIOS.get(servicio)  # Detalles del servicio que el usuario está comprando
    return render_template("pago/pago.html", servicio=servicio_details)

# PAGO NORMAL POR TARJETA (Redsys)
@pago.route('/pago_redsys/<servicio>', methods=['GET'])
@login_required
def pagar_redsys(servicio):
    """Realiza el pago a través de Redsys con tarjeta."""
    params, firma = generar_redsys_params(servicio)
    if not params:
        flash("El servicio seleccionado no existe.", "danger")
        return redirect(url_for('tasks.servicios'))  # Redirigir a la página de servicios

    # Asegúrate de pasar el servicio a la plantilla
    servicio_details = SERVICIOS.get(servicio)
    return render_template("pago/pago_redsys.html", datos=params, firma=firma, url_redsys=Config.REDSYS_URL, servicio=servicio_details)

# PAGO CON BIZUM (Redsys)
@pago.route('/pago_bizum/<servicio>', methods=['GET'])
@login_required
def pagar_bizum(servicio):
    """Realiza el pago a través de Bizum."""
    params, firma = generar_redsys_params(servicio, bizum=True)
    if not params:
        flash("El servicio seleccionado no existe.", "danger")
        return redirect(url_for('tasks.servicios'))  # Redirigir a la página de servicios

    # Asegúrate de pasar el servicio a la plantilla
    servicio_details = SERVICIOS.get(servicio)
    return render_template("pago/pago_redsys.html", datos=params, firma=firma, url_redsys=Config.REDSYS_URL, servicio=servicio_details)

# CONFIRMAR PAGO (para cuando el pago es exitoso)
@pago.route("/confirmar_pago/<servicio>", methods=["POST"])
@login_required
def confirmar_pago(servicio):
    """Confirma el pago y redirige a la página de éxito."""
    if servicio not in SERVICIOS:
        flash("El servicio seleccionado no existe.", "danger")
        return redirect(url_for('tasks.servicios'))  # Redirigir a la página de servicios

    flash(f"Pago realizado con éxito para {SERVICIOS[servicio]['nombre']}!", "success")
    return redirect(url_for("pago.pago_exitoso", servicio=servicio))

# PÁGINA DE PAGO EXITOSO (cuando el pago se haya completado correctamente)
@pago.route("/pago_exitoso/<servicio>")
@login_required
def pago_exitoso(servicio):
    """Página de éxito cuando el pago se ha completado."""
    if servicio not in SERVICIOS:
        flash("El servicio seleccionado no existe.", "danger")
        return redirect(url_for('tasks.servicios'))  # Redirigir a la página de servicios

    detalles = SERVICIOS[servicio]
    return render_template("pago/pago_exitoso.html", usuario=current_user, servicio=detalles)

# PÁGINA DE PAGO FALLIDO (cuando el pago no se pudo completar)
@pago.route("/pago_fallido")
def pago_fallido():
    """Página cuando el pago falla."""
    flash("El pago no se pudo completar. Inténtalo nuevamente.", "danger")
    return redirect(url_for('tasks.servicios'))  # Redirigir a la página de servicios
