# from flask import Blueprint, render_template, request, redirect, url_for, flash
# from werkzeug.security import generate_password_hash
# from flask_login import login_required
# from models.users import User
# from models import db

# # Creación del blueprint para la administración
# crearadmin = Blueprint('tasks', __name__)

# # Ruta para cambiar la contraseña del administrador
# @crearadmin.route('/change_password', methods=['POST'])
# @login_required  # Se asegura de que el usuario esté logueado antes de cambiar la contraseña
# def change_password():
#     # Suponiendo que el admin ha iniciado sesión
#     admin_user = User.query.filter_by(username='admin').first()

#     if admin_user:
#         new_password = request.form['new_password']  # Tomamos la nueva contraseña del formulario
#         admin_user.set_password(new_password)  # Establecemos la nueva contraseña
#         db.session.commit()  # Guardamos los cambios en la base de datos
#         flash("Contraseña cambiada con éxito!", "success")
#         return redirect(url_for('tasks.change_password'))  # Redirigir al usuario a una página de confirmación o de administración

#     flash("Usuario admin no encontrado.", "error")
#     return redirect(url_for('tasks.change_password'))  # Redirigir si no se encuentra el admin
