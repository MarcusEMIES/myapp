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
        return redirect(url_for('tasks.dashboard', user_id=user.id))

    return render_template('editar_usuario.html', usuario=user)


@admin.route('/borrar_usuario/<int:user_id>', methods=['POST'])
@login_required
def borrar_usuario(user_id):
    if current_user.role != 'admin':
        flash("Acceso denegado.", "danger")
        return redirect(url_for('tasks.dashboard'))

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    
    flash("Usuario eliminado exitosamente", "success")
    return redirect(url_for('admin.listar_usuarios'))



# Ruta para la controlar la subida de archivos 
@admin.route('/uploads/<filename>')
def uploads(filename):
    return send_from_directory(Config.UPLOAD_FOLDER, filename)


#ADMINISTRACION DEL CONTENIDO APP

@admin.route('/admin_panel')
@login_required
def admin_panel():
    # Comprobamos si el usuario es un administrador
    if current_user.role != 'admin':
        flash("Acceso denegado.", "danger")
        return redirect(url_for('tasks.dashboard'))  # Redirigir si no es admin
    
    # Renderizar la plantilla del panel de administración
    return render_template('tareas_admin/admin_panel.html')


@admin.route('/subir_imagen', methods=['GET', 'POST'])
@login_required
def subir_imagen():
    """Ruta para subir imágenes en el panel de administración."""
    if request.method == 'POST':
        foto = request.files.get('foto')
        if foto and allowed_file(foto.filename):
            filename = secure_filename(foto.filename)
            foto.save(os.path.join(Config.UPLOAD_FOLDER, filename))
            flash("Imagen subida exitosamente", "success")
            return redirect(url_for('admin.admin_dashboard'))
        else:
            flash("Archivo no permitido. Asegúrate de que la imagen tenga una extensión válida.", "danger")
    return render_template('subir_imagen.html')




# 1. Gestión de Usuarios
@admin.route('/usuarios')
@login_required
def listar_usuarios():
    usuarios = User.query.all()
    return render_template('tareas_admin/usuarios.html', usuarios=usuarios)

def allowed_file(filename):
    """Verifica si el archivo tiene una extensión permitida."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

# 2. Administración de Contenidos
@admin.route('/contenido')
@login_required
def administracion_contenido():
    return render_template('tareas_admin/administracion_contenido.html')

# 3. Seguridad y Accesos
@admin.route('/seguridad')
@login_required
def seguridad_accesos():
    return render_template('tareas_admin/seguridad_accesos.html')

# 4. Gestión de Correos y Notificaciones
@admin.route('/correo')
@login_required
def gestion_correos():
    return render_template('tareas_admin/gestion_correos.html')

# 5. Configuración del Sitio
@admin.route('/configuracion')
@login_required
def configuracion_sitio():
    return render_template('tareas_admin/configuracion_sitio.html')

# 6. Monitoreo y Análisis
@admin.route('/monitoreo')
@login_required
def monitoreo_analisis():
    return render_template('tareas_admin/monitoreo_analisis.html')

# 7. Gestión de Pagos y Finanzas
@admin.route('/Pagos')
@login_required
def gestion_pagos():
    return render_template('tareas_admin/gestion_pagos.html')

# 8. Administración de Base de Datos
@admin.route('/Bases_de_datos')
@login_required
def administracion_base_datos():
    return render_template('tareas_admin/administracion_base_datos.html')

#9 Imprimir reportes
@admin.route('/Reportes')
@login_required
def reports():
    # Aquí va la lógica para generar y mostrar los reportes
    return render_template('tareas_admin/printreport.html')



# from flask import Blueprint, render_template, request, redirect, url_for, flash, send_from_directory
# from flask_login import login_required, current_user
# from werkzeug.utils import secure_filename
# from models.users import User
# from models import db
# import os
# from config import Config

# admin = Blueprint('admin', __name__)

# @admin.route('/admin')
# @login_required
# def admin_dashboard():
#     if current_user.role != 'admin':
#         flash("Acceso denegado.", "danger")
#         return redirect(url_for('tasks.dashboard'))
#     return render_template('admin.html')

# @admin.route('/usuarios')
# @login_required
# def listar_usuarios():
#     usuarios = User.query.all()
#     return render_template('usuarios.html', usuarios=usuarios)

# def allowed_file(filename):
#     """Verifica si el archivo tiene una extensión permitida."""
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

# @admin.route('/subir_imagen', methods=['GET', 'POST'])
# @login_required
# def subir_imagen():
#     """Ruta para subir imágenes en el panel de administración."""
#     if request.method == 'POST':
#         foto = request.files.get('foto')
#         if foto and allowed_file(foto.filename):
#             filename = secure_filename(foto.filename)
#             foto.save(os.path.join(Config.UPLOAD_FOLDER, filename))
#             flash("Imagen subida exitosamente", "success")
#             return redirect(url_for('admin.admin_dashboard'))
#         else:
#             flash("Archivo no permitido. Asegúrate de que la imagen tenga una extensión válida.", "danger")
#     return render_template('subir_imagen.html')

# @admin.route('/editar_usuario/<int:user_id>', methods=['GET', 'POST'])
# def editar_usuario(user_id):
#     user = User.query.get_or_404(user_id)

#     if request.method == 'POST':
#         username = request.form.get('username', user.username)
#         nombre = request.form.get('nombre', user.nombre)
#         apellidos = request.form.get('apellidos', user.apellidos)
#         telefono = request.form.get('telefono', user.telefono)
#         direccion = request.form.get('direccion', user.direccion)
#         ciudad = request.form.get('ciudad', user.ciudad)
#         pais = request.form.get('pais', user.pais)
#         email = request.form.get('email', user.email)

#         # Si se proporciona una nueva contraseña, actualizarla
#         password = request.form.get('password')
#         if password:
#             user.set_password(password)  # Usamos el método de set_password del modelo

#         # Si se carga una nueva foto de perfil, guardarla
#         foto = request.files.get('foto')
#         if foto and allowed_file(foto.filename):
#             filename = secure_filename(foto.filename)
#             foto.save(os.path.join(Config.UPLOAD_FOLDER, filename))
#             user.foto = filename

#         # Actualizar otros campos del usuario
#         user.username = username
#         user.nombre = nombre
#         user.apellidos = apellidos
#         user.telefono = telefono
#         user.direccion = direccion
#         user.ciudad = ciudad
#         user.pais = pais
#         user.email = email

#         # Guardar los cambios en la base de datos
#         db.session.commit()

#         flash("Usuario actualizado exitosamente", "success")
#         return redirect(url_for('admin.editar_usuario', user_id=user.id))

#     return render_template('editar_usuario.html', usuario=user)

# @admin.route('/uploads/<filename>')
# def uploads(filename):
#     return send_from_directory(Config.UPLOAD_FOLDER, filename)
