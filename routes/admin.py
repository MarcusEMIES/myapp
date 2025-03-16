from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db  # Importar la instancia de la base de datos
from models.users import User  

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
    if current_user.role != 'admin':
        flash("Acceso denegado.", "danger")
        return redirect(url_for('tasks.dashboard'))

    usuario = User.query.get_or_404(user_id)
    if request.method == 'POST':
        usuario.username = request.form['username']
        usuario.email = request.form['email']
        db.session.commit()
        flash("Usuario actualizado correctamente.", "success")
        return redirect(url_for('admin.listar_usuarios'))

    return render_template('editar_usuario.html', usuario=usuario)
