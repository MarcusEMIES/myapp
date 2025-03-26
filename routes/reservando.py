from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db
from models.reserva import Reserva
from datetime import datetime, timedelta

# Blueprint para la funcionalidad de reservamiento
reservamiento = Blueprint('reservamiento', __name__, template_folder='../templates/reservamiento')

@reservamiento.route('/reservar', methods=['GET', 'POST'])
@login_required
def reservar():
    if request.method == 'POST':
        # Obtener los datos del formulario
        fecha_hora_str = request.form.get('fecha_hora')  # Formato datetime-local
        lugar = request.form.get('lugar')
        tipo_sesion = request.form.get('tipo_sesion')

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

        # Verificar si ya existe una reserva para ese horario
        reserva_existente = db.session.query(Reserva).filter_by(fecha_hora=fecha_hora).first()
        if reserva_existente:
            flash('Ya existe una reserva en esa fecha y hora. Elige otra.', 'error')
            return redirect(url_for('reservamiento.reservar'))

        # Crear nueva reserva
        nueva_reserva = Reserva(
            user_id=current_user.id,
            nombre=current_user.nombre,
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
        return redirect(url_for('reservamiento.ver_reserva'))

    # Preparar el formulario para la fecha y hora
    ahora = datetime.now().strftime('%Y-%m-%dT%H:%M')  # Hora actual para el valor por defecto
    ahora_min = (datetime.now() + timedelta(hours=12)).strftime('%Y-%m-%dT%H:%M')  # Min 12 horas
    ahora_max = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%dT%H:%M')  # Máximo 30 días

    # Pasar nombre y correo del usuario autenticado al formulario
    return render_template(
        'reservas/reservar.html',
        nombre_usuario=current_user.nombre,
        correo_usuario=current_user.email,
        ahora=ahora,
        ahora_min=ahora_min,
        ahora_max=ahora_max
    )

@reservamiento.route('/ver_reserva')
@login_required
def ver_reserva():
    # Consulta correcta con el bind
    reservas = db.session.query(Reserva).filter_by(user_id=current_user.id).order_by(Reserva.fecha_hora.desc()).all()

    return render_template('reservas/ver_reservas.html', reservas=reservas)
