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

# Ruta para la página de reservas. Permite a los usuarios hacer nuevas reservas.
@reservamiento.route('/reservar', methods=['GET', 'POST'])
@login_required  # Asegura que el usuario esté autenticado para acceder a esta ruta.
def reservar():
    if request.method == 'POST':  # Si el método HTTP es POST (cuando se envía el formulario)
        # Obtener los datos del formulario
        fecha_hora_str = request.form.get('fecha_hora')  # Fecha y hora en formato datetime-local
        lugar = request.form.get('lugar')  # Lugar de la reserva
        tipo_sesion = request.form.get('tipo_sesion')  # Tipo de sesión
        nombre = request.form.get('nombre')  # Nombre proporcionado por el usuario

        # Validación: asegurarse de que el campo 'fecha_hora' no esté vacío
        if not fecha_hora_str:
            flash('Por favor, selecciona una fecha y hora válida.', 'error')
            return redirect(url_for('reservamiento.reservar'))  # Redirige de nuevo al formulario.

        # Intentar convertir la cadena de fecha y hora a un objeto datetime
        try:
            fecha_hora = datetime.strptime(fecha_hora_str, '%Y-%m-%dT%H:%M')  # Convierte el formato de cadena a datetime
        except ValueError:
            flash('Formato de fecha y hora inválido.', 'error')
            return redirect(url_for('reservamiento.reservar'))

        # Validación: la reserva debe ser al menos 12 horas después del momento actual
        ahora = datetime.now()  # Hora actual
        if fecha_hora < ahora + timedelta(hours=12):
            flash('La reserva debe ser al menos 12 horas después de la hora actual.', 'error')
            return redirect(url_for('reservamiento.reservar'))  # Redirige si no cumple el requisito

        # Validación: la reserva debe estar en horario laboral (9 AM - 6 PM)
        if fecha_hora.hour < 9 or fecha_hora.hour > 18:
            flash('Las reservas solo pueden realizarse entre las 9:00 AM y las 6:00 PM.', 'error')
            return redirect(url_for('reservamiento.reservar'))  # Redirige si no está en el rango horario permitido

        # Verificar si ya existe una reserva para el mismo horario
        reserva_existente = db.session.query(Reserva).filter_by(fecha_hora=fecha_hora).first()
        if reserva_existente:
            flash('Ya existe una reserva en esa fecha y hora. Elige otra.', 'error')
            return redirect(url_for('reservamiento.reservar'))  # Redirige si ya hay una reserva existente

        # Crear una nueva reserva
        nueva_reserva = Reserva(
            user_id=current_user.id,  # Asociar la reserva al usuario actual
            nombre=nombre if nombre else current_user.username,  # Usar el nombre proporcionado o el nombre de usuario
            correo=current_user.email,  # Correo del usuario autenticado
            fecha_hora=fecha_hora,  # Fecha y hora de la reserva
            lugar=lugar,  # Lugar de la reserva
            tipo_sesion=tipo_sesion,  # Tipo de sesión (fotografía, video, etc.)
            precio=100.0,  # Precio de la reserva (valor de ejemplo)
            disponibilidad=10  # Stock disponible (valor de ejemplo)
        )
        db.session.add(nueva_reserva)  # Añadir la reserva a la base de datos
        db.session.commit()  # Guardar los cambios

        flash('Reserva realizada con éxito.', 'success')  # Mensaje de éxito
        return redirect(url_for('tasks.dashboard'))  # Redirige a la página del dashboard

    # Preparar los valores por defecto del formulario para la fecha y hora
    ahora = datetime.now().strftime('%Y-%m-%dT%H:%M')  # Hora actual
    ahora_min = (datetime.now() + timedelta(hours=12)).strftime('%Y-%m-%dT%H:%M')  # 12 horas después
    ahora_max = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%dT%H:%M')  # Máximo 30 días

    # Renderizar la plantilla para mostrar el formulario de reservas
    return render_template(
        'reservar.html',
        nombre_usuario=current_user.username,  # Pasa el nombre de usuario actual al formulario
        correo_usuario=current_user.email,  # Pasa el correo del usuario actual al formulario
        ahora=ahora,  # Pasa la hora actual como valor por defecto
        ahora_min=ahora_min,  # Pasa la fecha mínima (12 horas después) como valor por defecto
        ahora_max=ahora_max  # Pasa la fecha máxima (30 días después) como valor por defecto
    )


# Ruta para ver todas las reservas realizadas por el usuario o por el admin
@reservamiento.route('/ver_reservas')
@login_required  # Solo accesible por usuarios autenticados
def ver_reserva():
    # Verificar si el usuario tiene el rol 'admin'
    if current_user.role == 'admin':
        # Si es administrador, mostrar todas las reservas
        reservas = db.session.query(Reserva).order_by(Reserva.fecha_hora.desc()).all()
    else:
        # Si no es administrador, mostrar solo las reservas del usuario actual
        reservas = db.session.query(Reserva).filter_by(user_id=current_user.id).order_by(Reserva.fecha_hora.desc()).all()

    # Renderizar la plantilla para mostrar las reservas
    return render_template('ver_reservas.html', reservas=reservas)


# Ruta para editar una reserva específica
@reservamiento.route('/editar_reserva/<int:reserva_id>', methods=['GET', 'POST'])
@login_required  # Solo accesible por usuarios autenticados
def editar_reserva(reserva_id):
    # Obtener la reserva que se va a editar
    reserva = Reserva.query.get_or_404(reserva_id)  # Busca la reserva por su ID o devuelve un error 404 si no existe

    # Verificar si el usuario tiene permiso para editar la reserva
    if reserva.user_id != current_user.id and current_user.role != 'admin':
        flash('No tienes permiso para editar esta reserva.', 'danger')  # Mensaje de error
        return redirect(url_for('reservamiento.ver_reservas'))  # Redirige a la lista de reservas

    if request.method == 'POST':  # Si el formulario es enviado (método POST)
        # Actualizar los datos de la reserva
        fecha_hora_str = request.form.get('fecha_hora')
        if fecha_hora_str:
            try:
                fecha_hora = datetime.strptime(fecha_hora_str, '%Y-%m-%dT%H:%M')
                reserva.fecha_hora = fecha_hora  # Actualizar la fecha y hora de la reserva
            except ValueError:
                flash('Formato de fecha y hora inválido.', 'danger')  # Mensaje de error
                return redirect(url_for('reservamiento.editar_reserva', reserva_id=reserva.id))

        # Actualizar otros campos de la reserva
        reserva.lugar = request.form.get('lugar', reserva.lugar)
        reserva.tipo_sesion = request.form.get('tipo_sesion', reserva.tipo_sesion)
        reserva.precio = float(request.form.get('precio', reserva.precio))
        reserva.description = request.form.get('description', reserva.description)

        # Si se carga una nueva imagen para la reserva
        image = request.files.get('image_url')
        if image and allowed_file(image.filename):  # Verificar que el archivo tiene una extensión permitida
            filename = secure_filename(image.filename)  # Asegurarse de que el nombre del archivo sea seguro
            image.save(os.path.join(Config.UPLOAD_FOLDER, filename))  # Guardar la imagen en la carpeta configurada
            reserva.image_url = filename  # Actualizar la URL de la imagen

        # Guardar los cambios en la base de datos
        db.session.commit()

        flash("Reserva actualizada exitosamente", "success")  # Mensaje de éxito
        return redirect(url_for('reservamiento.ver_reserva'))  # Redirige a la vista de reservas

    # Si el método es GET, mostrar el formulario con los datos actuales de la reserva
    return render_template('reservas/editar_reservas.html', reserva=reserva)


# Función para verificar si un archivo tiene una extensión permitida
def allowed_file(filename):
    """Verifica si el archivo tiene una extensión permitida."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS


# Ruta para eliminar una reserva
@reservamiento.route('/eliminar_reserva', methods=['POST'])
@login_required  # Solo accesible por usuarios autenticados
def eliminar_reserva():
    # Obtener los datos del formulario para la eliminación
    nombre = request.form.get('nombre')
    email = request.form.get('email')
    fecha_str = request.form.get('fecha')
    ciudad = request.form.get('ciudad')

    try:
        # Convertir la fecha de string a datetime
        fecha = datetime.strptime(fecha_str, '%Y-%m-%dT%H:%M')

        # Buscar la reserva con los criterios proporcionados
        reserva = Reserva.query.filter_by(nombre=nombre, email=email, lugar=ciudad, fecha_hora=fecha).first()

        if reserva:
            # Verificar si el usuario tiene permiso para eliminar la reserva
            if current_user.role != 'admin' and (reserva.user_id != current_user.id):
                flash('No tienes permiso para eliminar esta reserva.', 'danger')  # Mensaje de error
                return redirect(url_for('reservamiento.ver_reservas'))

            # Eliminar la reserva
            db.session.delete(reserva)
            db.session.commit()

            flash("Reserva eliminada exitosamente", "success")  # Mensaje de éxito
        else:
            flash('No se encontró ninguna reserva con los criterios especificados.', 'danger')

    except ValueError:
        flash('Formato de fecha inválido. Asegúrate de que el formato sea correcto.', 'danger')  # Mensaje de error

    return redirect(url_for('reservamiento.ver_reserva'))  # Redirige a la vista de reservas
