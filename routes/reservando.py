from flask import Blueprint, render_template, request, redirect, url_for, flash, send_from_directory
from flask_login import login_required, current_user
from models import db
from models.reserva import Reserva
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
from config import Config
import os

# Blueprint para la funcionalidad de reservamiento
reservamiento = Blueprint('reservamiento', __name__, template_folder='../templates/reservas')


@reservamiento.route('/reservar', methods=['GET', 'POST'])
@login_required
def reservar():
    if request.method == 'POST':
        # Obtener los datos del formulario
        fecha_hora_str = request.form.get('fecha_hora')  # Formato datetime-local
        lugar = request.form.get('lugar')
        tipo_sesion = request.form.get('tipo_sesion')
        nombre = request.form.get('nombre')  # Valor del campo nombre (proporcionado por el usuario)

        # Validar que el campo fecha_hora no esté vacío
        if not fecha_hora_str:
            flash('Por favor, selecciona una fecha y hora válida.', 'error')
            return redirect(url_for('reservamiento.reservar'))

        # Convertir la fecha y hora de la cadena al formato datetime
        try:
            fecha_hora = datetime.strptime(fecha_hora_str, '%Y-%m-%dT%H:%M')
        except ValueError:
            flash('Formato de fecha y hora inválido.', 'error')
            return redirect(url_for('reservamiento.reservar'))

        # Validar que la reserva sea al menos 12 horas después
        ahora = datetime.now()
        if fecha_hora < ahora + timedelta(hours=12):
            flash('La reserva debe ser al menos 12 horas después de la hora actual.', 'error')
            return redirect(url_for('reservamiento.reservar'))

        # Validar que la reserva esté en horario laboral (9 AM - 6 PM)
        if fecha_hora.hour < 9 or fecha_hora.hour > 18:
            flash('Las reservas solo pueden realizarse entre las 9:00 AM y las 6:00 PM.', 'error')
            return redirect(url_for('reservamiento.reservar'))

        # Verificar si ya existe una reserva para ese horario
        reserva_existente = db.session.query(Reserva).filter_by(fecha_hora=fecha_hora).first()
        if reserva_existente:
            flash('Ya existe una reserva en esa fecha y hora. Elige otra.', 'error')
            return redirect(url_for('reservamiento.reservar'))

        # Crear nueva reserva, asegurándote de que 'nombre' proviene del formulario
        nueva_reserva = Reserva(
            user_id=current_user.id,
            nombre=nombre if nombre else current_user.username,  # Usar el valor de 'nombre' si es proporcionado, de lo contrario, usar el username
            correo=current_user.email,
            fecha_hora=fecha_hora,
            lugar=lugar,
            tipo_sesion=tipo_sesion,
            precio=100.0,  # Precio de ejemplo
            disponibilidad=10  # Ejemplo de stock disponible
        )
        db.session.add(nueva_reserva)
        db.session.commit()

        flash('Reserva realizada con éxito.', 'success')
        return redirect(url_for('tasks.dashboard'))

    # Preparar el formulario para la fecha y hora
    ahora = datetime.now().strftime('%Y-%m-%dT%H:%M')  # Hora actual para el valor por defecto
    ahora_min = (datetime.now() + timedelta(hours=12)).strftime('%Y-%m-%dT%H:%M')  # Min 12 horas
    ahora_max = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%dT%H:%M')  # Máximo 30 días

    # Pasar nombre y correo del usuario autenticado al formulario
    return render_template(
        'reservar.html',
        nombre_usuario=current_user.username,  # Pasamos el username automáticamente
        correo_usuario=current_user.email,
        ahora=ahora,
        ahora_min=ahora_min,
        ahora_max=ahora_max
    )


@reservamiento.route('/ver_reservas')
@login_required
def ver_reserva():
    # Verificar si el usuario tiene el rol 'admin'
    if current_user.role == 'admin':
        # Si es administrador, mostrar todas las reservas
        reservas = db.session.query(Reserva).order_by(Reserva.fecha_hora.desc()).all()
    else:
        # Si no es administrador, solo mostrar las reservas del usuario actual
        reservas = db.session.query(Reserva).filter_by(user_id=current_user.id).order_by(Reserva.fecha_hora.desc()).all()

    # Renderizar la plantilla con las reservas
    return render_template('ver_reservas.html', reservas=reservas)

@reservamiento.route('/editar_reserva/<int:reserva_id>', methods=['GET', 'POST'])
@login_required
def editar_reserva(reserva_id):
    # Obtener la reserva a editar
    reserva = Reserva.query.get_or_404(reserva_id)

    # Verificar si el usuario tiene permiso para editarla
    if reserva.user_id != current_user.id and current_user.role != 'admin':
        flash('No tienes permiso para editar esta reserva.', 'danger')
        return redirect(url_for('reservamiento.ver_reserva'))

    if request.method == 'POST':
        # Actualizar los datos de la reserva
        reserva.fecha_hora = request.form.get('fecha_hora', reserva.fecha_hora)
        reserva.lugar = request.form.get('lugar', reserva.lugar)
        reserva.tipo_sesion = request.form.get('tipo_sesion', reserva.tipo_sesion)
        reserva.precio = float(request.form.get('precio', reserva.precio))
        reserva.description = request.form.get('description', reserva.description)

        # Si se carga una nueva imagen de reserva
        image = request.files.get('image_url')
        if image and allowed_file(image.filename):  # Verificar si el archivo es válido
            filename = secure_filename(image.filename)  # Asegurarse de que el nombre del archivo sea seguro
            image.save(os.path.join(Config.UPLOAD_FOLDER, filename))  # Guardar la imagen en la carpeta configurada
            reserva.image_url = filename  # Actualizar la URL de la imagen de la reserva

        # Guardar los cambios en la base de datos
        db.session.commit()

        flash("Reserva actualizada exitosamente", "success")
        return redirect(url_for('reservamiento.ver_reserva'))

    return render_template('reservas/editar_reservas.html', reserva=reserva)
def allowed_file(filename):
    """Verifica si el archivo tiene una extensión permitida."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS
