#archivo admin.py

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db  # Importar la instancia de la base de datos
from models.users import User  

# Crear un Blueprint para la admin

admin = Blueprint('admin', __name__)

# Ruta para admin
@admin.route('/admin')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        flash("Acceso denegado.", "danger")
        return redirect(url_for('tasks.dashboard'))
    return render_template('admin.html')


# Ruta para "usuarios"
@admin.route('/usuarios')
@login_required
def listar_usuarios():
    if current_user.role != 'admin':
        flash("Acceso denegado.", "danger")
        return redirect(url_for('tasks.dashboard'))

    usuarios = User.query.all()
    return render_template('usuarios.html', usuarios=usuarios)



# Ruta para "editar_usuario"
@admin.route('/editar_usuario/<int:user_id>', methods=['GET', 'POST'])
@login_required
def editar_usuario(user_id):
    # Obtener el usuario a editar desde la base de datos
    usuario = User.query.get_or_404(user_id)

    # Si el usuario no es el mismo que el que está logueado, controlar lo que puede editarse
    if usuario.id != current_user.id and current_user.role != 'admin':
        flash("Acceso denegado a este perfil.", "danger")
        return redirect(url_for('tasks.dashboard'))  # Redirigir al dashboard si no es el perfil del usuario

    if request.method == 'POST':
        # Solo permitir edición si es el propio usuario o un admin
        if usuario.id == current_user.id or current_user.role == 'admin':
            usuario.username = request.form['username']
            usuario.email = request.form['email']
            db.session.commit()
            flash("Usuario actualizado correctamente.", "success")
            return redirect(url_for('admin.listar_usuarios'))  # Redirigir a la lista de usuarios

        flash("No tienes permisos para editar este usuario.", "danger")
        return redirect(url_for('tasks.dashboard'))

    return render_template('editar_usuario.html', usuario=usuario)
