from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import datetime, timedelta
from models.reserva import Reserva  # Importar modelo de reservas
from models import db  # Importar la base de datos

reservamiento = Blueprint('reservamiento', __name__, template_folder='../templates/reservas')

@reservamiento.route('/reservar', methods=['GET', 'POST'])
@login_required
def reservar():
    if request.method == 'POST':
        fecha = request.form.get('fecha')
        hora = request.form.get('hora')
        lugar = request.form.get('lugar')
        tipo_sesion = request.form.get('tipo_sesion')

        if not fecha or not hora:
            flash('Debe seleccionar una fecha y hora válidas.', 'error')
            return redirect(url_for('reservamiento.reservar'))

        # Convertir fecha y hora a objeto datetime
        fecha_hora_str = f"{fecha}T{hora}"
        try:
            fecha_hora = datetime.strptime(fecha_hora_str, '%Y-%m-%dT%H:%M')
        except ValueError:
            flash('Formato de fecha y hora no válido.', 'error')
            return redirect(url_for('reservamiento.reservar'))

        # Validar que la fecha sea futura y con mínimo 3 horas de anticipación
        ahora = datetime.now()
        if fecha_hora < ahora + timedelta(hours=3):
            flash('No puedes reservar fechas pasadas o con menos de 3 horas de anticipación.', 'error')
            return redirect(url_for('reservamiento.reservar'))

        # Validar horarios no permitidos (21:00-06:00 y 11:00-14:00)
        hora_reserva = fecha_hora.hour
        if (hora_reserva >= 21 or hora_reserva < 6) or (11 <= hora_reserva < 14):
            flash('Las reservas no están permitidas entre 21:00-06:00 ni entre 11:00-14:00.', 'error')
            return redirect(url_for('reservamiento.reservar'))

        # Verificar si ya existe una reserva en esa fecha y hora
        reserva_existente = Reserva.query.filter_by(fecha_hora=fecha_hora).first()
        if reserva_existente:
            flash('Ya existe una reserva en esa fecha y hora. Elige otra.', 'error')
            return redirect(url_for('reservamiento.reservar'))

        # Crear y guardar la nueva reserva
        nueva_reserva = Reserva(
            user_id=current_user.id,
            fecha_hora=fecha_hora,
            lugar=lugar,
            tipo_sesion=tipo_sesion,
            duracion=timedelta(hours=3)
        )
        db.session.add(nueva_reserva)
        db.session.commit()

        flash('Reserva realizada con éxito.', 'success')
        return redirect(url_for('reservamiento.ver_reserva'))

    return render_template('reservas/reservar.html')

@reservamiento.route('/ver_reserva')
@login_required
def ver_reserva():
    reservas = Reserva.query.filter_by(user_id=current_user.id).order_by(Reserva.fecha_hora.desc()).all()
    return render_template('reservas/ver_reservas.html', reservas=reservas)
