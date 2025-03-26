from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db
from models.reserva import Reserva
from datetime import datetime

reservamiento = Blueprint('reservamiento', __name__, template_folder='../templates/reservas')

@reservamiento.route('/reservar', methods=['GET', 'POST'])
@login_required
def reservar():
    if request.method == 'POST':
        fecha = request.form.get('fecha')
        hora = request.form.get('hora')
        lugar = request.form.get('lugar')
        tipo_sesion = request.form.get('tipo_sesion')
        
        # Convertir fecha y hora en un objeto datetime
        fecha_hora = datetime.combine(datetime.strptime(fecha, '%Y-%m-%d').date(), datetime.strptime(hora, '%H:%M').time())
        
        # Validar que la fecha y hora sean válidas
        if fecha_hora < datetime.now():
            flash('La fecha y hora deben ser en el futuro.', 'error')
            return redirect(url_for('reservamiento.reservar'))
        
        # Verificar si ya existe una reserva en esa fecha y hora
        reserva_existente = Reserva.query.filter_by(fecha=fecha, hora=hora).first()
        if reserva_existente:
            flash('Ya existe una reserva en esa fecha y hora. Elige otra.', 'error')
            return redirect(url_for('reservamiento.reservar'))

        # Guardar la nueva reserva en la base de datos
        nueva_reserva = Reserva(
            user_id=current_user.id,
            fecha=fecha,
            hora=hora,
            lugar=lugar,
            tipo_sesion=tipo_sesion
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
