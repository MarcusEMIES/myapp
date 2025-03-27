from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_required, current_user
from models.products import Product

portafolio = Blueprint('portafolio', __name__)

# Ruta para ingresar la contraseña y validarla
@portafolio.route('/ingresar_contraseña', methods=['GET', 'POST'])
@login_required
def ingresar_contraseña():
    if request.method == 'POST':
        contraseña = request.form.get('contraseña')
        
        # Validación de la contraseña (por ejemplo, comparar con una contraseña predefinida)
        if contraseña == "tu_contraseña_secreta":  # Cambia esto por tu lógica de contraseña
            session['acceso_granted'] = True
            flash('¡Acceso concedido! Ahora puedes ver el contenido.', 'success')
            return redirect(url_for('portafolio.ver_contenido'))  # Redirige a la página del contenido
        else:
            flash('Contraseña incorrecta. Intenta nuevamente.', 'danger')
            return redirect(url_for('portafolio.ingresar_contraseña'))  # Redirige al formulario de contraseña

    return render_template('portafolio_cliente.html')  # Aquí se renderiza el formulario de la contraseña

# Ruta para mostrar el contenido después de ingresar la contraseña
@portafolio.route('/ver_contenido')
@login_required
def ver_contenido():
    if not session.get('acceso_granted'):  # Si no se ha ingresado la contraseña correcta, denegar el acceso
        flash('Por favor ingresa la contraseña para acceder al contenido.', 'warning')
        return redirect(url_for('portafolio.ingresar_contraseña'))  # Redirige al formulario de contraseña

    # Obtener los archivos asociados al usuario actual
    archivos = Product.query.filter_by(user_id=current_user.id).all()  # Suponiendo que tienes un modelo 'Archivo'

    return render_template('contenido.html', archivos=archivos)  # Muestra los archivos en la página
