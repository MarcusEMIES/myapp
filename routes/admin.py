from flask import Blueprint, render_template, request, redirect, url_for, flash, send_from_directory
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from models.users import User
from models import db
import os
from config import Config

admin = Blueprint('admin', __name__)

@admin.route('/admin')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        flash("Acceso denegado.", "danger")
        return redirect(url_for('tasks.dashboard'))
    return render_template('admin.html')

@admin.route('/usuarios')
@login_required
def listar_usuarios():
    usuarios = User.query.all()
    return render_template('usuarios.html', usuarios=usuarios)

def allowed_file(filename):
    """Verifica si el archivo tiene una extensión permitida."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS


@admin.route('/editar_usuario/<int:user_id>', methods=['GET', 'POST'])
def editar_usuario(user_id):
    user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        username = request.form.get('username', user.username)
        nombre = request.form.get('nombre', user.nombre)
        apellidos = request.form.get('apellidos', user.apellidos)
        telefono = request.form.get('telefono', user.telefono)
        direccion = request.form.get('direccion', user.direccion)
        ciudad = request.form.get('ciudad', user.ciudad)
        pais = request.form.get('pais', user.pais)
        email = request.form.get('email', user.email)

        # Si se proporciona una nueva contraseña, actualizarla
        password = request.form.get('password')
        if password:
            user.set_password(password)  # Usamos el método de set_password del modelo

        # Si se carga una nueva foto de perfil, guardarla
        foto = request.files.get('foto')
        if foto and allowed_file(foto.filename):
            filename = secure_filename(foto.filename)
            foto.save(os.path.join(Config.UPLOAD_FOLDER, filename))
            user.foto = filename

        # Actualizar otros campos del usuario
        user.username = username
        user.nombre = nombre
        user.apellidos = apellidos
        user.telefono = telefono
        user.direccion = direccion
        user.ciudad = ciudad
        user.pais = pais
        user.email = email

        # Guardar los cambios en la base de datos
        db.session.commit()

        flash("Usuario actualizado exitosamente", "success")
        return redirect(url_for('admin.editar_usuario', user_id=user.id))

    return render_template('editar_usuario.html', usuario=user)
@admin.route('/uploads/<filename>')
def uploads(filename):
    return send_from_directory(Config.UPLOAD_FOLDER, filename)
