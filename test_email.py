from flask import Flask
from flask_mail import Mail, Message
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
mail = Mail(app)

with app.app_context():
    msg = Message("Prueba de correo", recipients=["tu_correo_real@gmail.com"])
    msg.body = "Este es un correo de prueba desde Flask-Mail."
    try:
        mail.send(msg)
        print("✅ ¡Correo enviado correctamente!")
    except Exception as e:
        print(f"❌ Error al enviar correo: {e}")


# Ese error (WinError 10060) indica que no se pudo establecer una conexión con el servidor SMTP.

# 🔎 Posibles causas y soluciones:
# 1️⃣ El servidor SMTP está mal configurado

# ¿Estás seguro de que MAIL_SERVER y MAIL_PORT son correctos?

# Prueba con TLS (MAIL_PORT=587) o SSL (MAIL_PORT=465)

# Si tu empresa usa Gmail u Outlook, los servidores serían:

# Gmail → smtp.gmail.com (puerto 587 con TLS)

# Outlook/Office365 → smtp.office365.com (puerto 587 con TLS)

# 2️⃣ Tu firewall o antivirus está bloqueando la conexión

# Prueba desactivar temporalmente el firewall y antivirus para ver si es eso.

# También puedes agregar una excepción en el firewall para permitir la conexión al puerto 587 o 465.

# 3️⃣ Tu proveedor de internet bloquea SMTP externo

# Algunas redes restringen las conexiones SMTP.

# Prueba conectarte a otra red o usa una VPN.

# 4️⃣ Faltan permisos en el servidor de correo

# Si usas un correo de empresa, revisa que el SMTP esté habilitado en la configuración del hosting.

