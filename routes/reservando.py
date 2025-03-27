# Importaciones necesarias para manejar rutas, plantillas, formularios y base de datos en Flask.
from flask import Blueprint, render_template, request, redirect, url_for, flash, send_from_directory
from flask_login import login_required, current_user  # Para manejar sesiones de usuario y autenticación.
from models import db  # Importa la instancia de la base de datos.
from models.reserva import Reserva  # Importa el modelo 'Reserva' de la base de datos.
from datetime import datetime, timedelta  # Para manejar fechas y tiempos.
from werkzeug.utils import secure_filename  # Para asegurar que los nombres de los archivos sean seguros.
from config import Config  # Para acceder a la configuración (como las extensiones de archivo permitidas).
import os  # Para trabajar con el sistema de archivos.

# Crear el Blueprint para las funcionalidades de reservamiento.
reservamiento = Blueprint('reservamiento', __name__, template_folder='../templates/reservas')

@reservamiento.route('/reservar', methods=['GET', 'POST'])
@login_required
def reservar():
    if request.method == 'POST':  
        fecha_hora_str = request.form.get('fecha_hora')  
        lugar = request.form.get('lugar')  
        tipo_sesion = request.form.get('tipo_sesion')  
        nombre = request.form.get('nombre')  

        if not fecha_hora_str:
            flash('Por favor, selecciona una fecha y hora válida.', 'error')
            return redirect(url_for('reservamiento.reservar'))  # Redirige al formulario.

        try:
            fecha_hora = datetime.strptime(fecha_hora_str, '%Y-%m-%dT%H:%M') 
        except ValueError:
            flash('Formato de fecha y hora inválido.', 'error')
            return redirect(url_for('reservamiento.reservar'))  # Redirige si la fecha es incorrecta.

        ahora = datetime.now()
        if fecha_hora < ahora + timedelta(hours=12):
            flash('La reserva debe ser al menos 12 horas después de la hora actual.', 'error')
            return redirect(url_for('reservamiento.reservar'))

        if fecha_hora.hour < 9 or fecha_hora.hour > 18:
            flash('Las reservas solo pueden realizarse entre las 9:00 AM y las 6:00 PM.', 'error')
            return redirect(url_for('reservamiento.reservar'))

        reserva_existente = db.session.query(Reserva).filter_by(fecha_hora=fecha_hora).first()
        if reserva_existente:
            flash('Ya existe una reserva en esa fecha y hora. Elige otra.', 'error')
            return redirect(url_for('reservamiento.reservar'))

        nueva_reserva = Reserva(
            user_id=current_user.id,
            nombre=nombre if nombre else current_user.username,
            correo=current_user.email,
            fecha_hora=fecha_hora,
            lugar=lugar,
            tipo_sesion=tipo_sesion,
            precio=100.0,
            disponibilidad=10
        )
        db.session.add(nueva_reserva)
        db.session.commit()

        flash('Reserva realizada con éxito.', 'success')
        return redirect(url_for('tasks.dashboard'))  # Redirige al dashboard, no al formulario.

    ahora = datetime.now().strftime('%Y-%m-%dT%H:%M')
    ahora_min = (datetime.now() + timedelta(hours=12)).strftime('%Y-%m-%dT%H:%M')
    ahora_max = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%dT%H:%M')

    return render_template(
        'reservar.html',
        nombre_usuario=current_user.username,
        correo_usuario=current_user.email,
        ahora=ahora,
        ahora_min=ahora_min,
        ahora_max=ahora_max
    )
# Función para verificar si un archivo tiene una extensión permitida
def allowed_file(filename):
    """Verifica si el archivo tiene una extensión permitida."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

# Ruta para ver todas las reservas realizadas por el usuario o por el admin
@reservamiento.route('/ver_reservas')
@login_required  # Solo accesible por usuarios autenticados
def ver_reservas():
    # Verificar si el usuario tiene el rol 'admin'
    if current_user.role == 'admin':
        # Si es administrador, mostrar todas las reservas
        reservas = db.session.query(Reserva).order_by(Reserva.fecha_hora.desc()).all()
    else:
        # Si no es administrador, mostrar solo las reservas del usuario actual
        reservas = db.session.query(Reserva).filter_by(user_id=current_user.id).order_by(Reserva.fecha_hora.desc()).all()

    # Renderizar la plantilla para mostrar las reservas
    return render_template('ver_reservas.html', reservas=reservas)

@reservamiento.route('/editar_reserva/<int:reserva_id>', methods=['GET', 'POST'])
@login_required
def editar_reserva(reserva_id):
    reserva = Reserva.query.get_or_404(reserva_id)

    if reserva.user_id != current_user.id and current_user.role != 'admin':
        flash('No tienes permiso para editar esta reserva.', 'danger')
        return redirect(url_for('reservamiento.ver_reservas'))  # Evitar redirecciones infinitas.

    if request.method == 'POST':
        fecha_hora_str = request.form.get('fecha_hora')
        if fecha_hora_str:
            try:
                fecha_hora = datetime.strptime(fecha_hora_str, '%Y-%m-%dT%H:%M')
                reserva.fecha_hora = fecha_hora  # Actualizar la fecha
            except ValueError:
                flash('Formato de fecha y hora inválido.', 'danger')
                return redirect(url_for('reservamiento.editar_reserva', reserva_id=reserva.id))

        reserva.lugar = request.form.get('lugar', reserva.lugar)
        reserva.tipo_sesion = request.form.get('tipo_sesion', reserva.tipo_sesion)
        reserva.precio = float(request.form.get('precio', reserva.precio))
        reserva.description = request.form.get('description', reserva.description)

        image = request.files.get('image_url')
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(Config.UPLOAD_FOLDER, filename))
            reserva.image_url = filename

        db.session.commit()

        flash("Reserva actualizada exitosamente", "success")
        return redirect(url_for('reservamiento.ver_reservas'))  # Redirige al listado de reservas.

    return render_template('reservas/editar_reservas.html', reserva=reserva)

@reservamiento.route('/eliminar_reserva/<int:reserva_id>', methods=['GET', 'POST'])
@login_required  # Requiere que el usuario esté autenticado
def eliminar_reserva(reserva_id):
    try:
        reserva = Reserva.query.get_or_404(reserva_id)  # Obtener la reserva por ID, 404 si no existe

        # Verificar si el usuario tiene el rol 'admin' o si el usuario es el creador de la reserva
        if current_user.role != 'admin' and reserva.user_id != current_user.id:
            flash("No tienes permiso para eliminar esta reserva.", "danger")
            return redirect(url_for('reservamiento.ver_reservas'))  # Redirigir si no tiene permisos

        db.session.delete(reserva)  # Eliminar la reserva de la base de datos
        db.session.commit()  # Confirmar los cambios

        flash("Reserva eliminada exitosamente", "success")  # Mensaje de éxito
    except Exception as e:
        db.session.rollback()  # Revertir cualquier cambio en caso de error
        flash(f"Hubo un error al eliminar la reserva: {str(e)}", "danger")  # Mostrar mensaje de error

    return redirect(url_for('reservamiento.ver_reservas'))  # Redirigir a la lista de reservas


# @reservamiento.route('/eliminar_reserva', methods=['POST'])
# @login_required
# def eliminar_reserva():
#     # Obtener los datos del formulario
#     nombre = request.form.get('nombre')
#     email = request.form.get('email')
#     fecha_str = request.form.get('fecha')
#     ciudad = request.form.get('ciudad')

#     # Validar que los parámetros esenciales están presentes
#     if not all([nombre, email, fecha_str, ciudad]):
#         flash("Todos los campos son necesarios.", "danger")
#         return redirect(url_for('reservamiento.ver_reservas'))

#     try:
#         # Convertir la fecha del formato string a datetime
#         fecha = datetime.strptime(fecha_str, '%Y-%m-%dT%H:%M')

#         # Buscar la reserva que coincida con los criterios proporcionados
#         reserva = Reserva.query.filter_by(nombre=nombre, correo=email, lugar=ciudad, fecha_hora=fecha).first()

#         if reserva:
#             # Verificar si el usuario tiene permiso para eliminar la reserva
#             if current_user.role != 'admin' and reserva.user_id != current_user.id:
#                 flash('No tienes permiso para eliminar esta reserva.', 'danger')
#                 return redirect(url_for('reservamiento.ver_reservas'))

#             # Eliminar la reserva
#             db.session.delete(reserva)
#             db.session.commit()
#             flash("Reserva eliminada exitosamente", "success")
#         else:
#             flash('No se encontró ninguna reserva con los criterios especificados.', 'danger')

#     except ValueError:
#         flash('Formato de fecha inválido. Asegúrate de que el formato sea correcto.', 'danger')

#     # Redirigir de vuelta a la vista de reservas
#     return redirect(url_for('reservamiento.ver_reservas'))
