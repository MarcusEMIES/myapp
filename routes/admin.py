from flask import Blueprint, render_template, request, redirect, url_for, flash, send_from_directory
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from models.users import User
from models import db
import os
from config import Config
from models.products import Product

# Crear el Blueprint para la parte administrativa
admin = Blueprint('admin', __name__)

# Ruta principal del panel de administración
@admin.route('/admin')
@login_required  # Requiere que el usuario esté autenticado
def admin_dashboard():
    # Verificar si el usuario tiene el rol 'admin', de lo contrario se deniega el acceso
    if current_user.role != 'admin':
        flash("Acceso denegado.", "danger")  # Mensaje de acceso denegado
        return redirect(url_for('tasks.dashboard'))  # Redirigir al dashboard de tareas
    return render_template('admin.html')  # Renderizar la plantilla de administración

# Ruta para editar un usuario
@admin.route('/editar_usuario/<int:user_id>', methods=['GET', 'POST'])
def editar_usuario(user_id):
    user = User.query.get_or_404(user_id)  # Obtener el usuario por su ID o 404 si no existe

    if request.method == 'POST':  # Si la solicitud es POST, se actualizan los datos del formulario
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
            user.set_password(password)  # Usamos el método set_password del modelo User

        # Si se carga una nueva foto de perfil, guardarla
        foto = request.files.get('foto')
        if foto and allowed_file(foto.filename):  # Verificar si el archivo tiene una extensión permitida
            filename = secure_filename(foto.filename)  # Asegurar que el nombre del archivo sea seguro
            foto.save(os.path.join(Config.UPLOAD_FOLDER, filename))  # Guardar la foto en el servidor
            user.foto = filename  # Guardar el nombre del archivo en la base de datos

        # Actualizar los otros campos del usuario
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

        flash("Usuario actualizado exitosamente", "success")  # Mensaje de éxito
        return redirect(url_for('tasks.dashboard', user_id=user.id))  # Redirigir al dashboard de tareas

    return render_template('editar_usuario.html', usuario=user)  # Renderizar la plantilla de edición

# Ruta para eliminar un usuario
@admin.route('/borrar_usuario/<int:user_id>', methods=['POST'])
@login_required  # Requiere que el usuario esté autenticado
def borrar_usuario(user_id):
    # Verificar si el usuario tiene el rol 'admin', si no, se deniega el acceso
    if current_user.role != 'admin':
        flash("Acceso denegado.", "danger")
        return redirect(url_for('tasks.dashboard'))  # Redirigir al dashboard de tareas

    user = User.query.get_or_404(user_id)  # Obtener el usuario por ID o 404 si no existe
    db.session.delete(user)  # Eliminar el usuario de la base de datos
    db.session.commit()  # Confirmar los cambios

    flash("Usuario eliminado exitosamente", "success")  # Mensaje de éxito
    return redirect(url_for('admin.listar_usuarios'))  # Redirigir a la lista de usuarios

# Ruta para servir los archivos subidos (por ejemplo, imágenes)
@admin.route('/uploads/<filename>')
def uploads(filename):
    return send_from_directory(Config.UPLOAD_FOLDER, filename)  # Servir el archivo desde el directorio de subidas

# Ruta para mostrar el panel de administración
@admin.route('/admin_panel')
@login_required  # Requiere autenticación
def admin_panel():
    if current_user.role != 'admin':  # Verificar si el usuario tiene el rol de administrador
        flash("Acceso denegado.", "danger")
        return redirect(url_for('tasks.dashboard'))  # Redirigir si el usuario no tiene acceso
    return render_template('tareas_admin/admin_panel.html')  # Renderizar la plantilla del panel de administración

# Ruta para subir imágenes desde el panel de administración
@admin.route('/subir_imagen', methods=['GET', 'POST'])
@login_required  # Requiere autenticación
def subir_imagen():
    """Ruta para subir imágenes en el panel de administración."""
    if request.method == 'POST':  # Si se recibe un formulario POST
        foto = request.files.get('foto')  # Obtener el archivo de imagen del formulario
        if foto and allowed_file(foto.filename):  # Verificar si el archivo tiene una extensión permitida
            filename = secure_filename(foto.filename)  # Asegurar que el nombre del archivo sea seguro
            foto.save(os.path.join(Config.UPLOAD_FOLDER, filename))  # Guardar el archivo en el servidor
            flash("Imagen subida exitosamente", "success")  # Mensaje de éxito
            return redirect(url_for('admin.admin_dashboard'))  # Redirigir al dashboard de administración
        else:
            flash("Archivo no permitido. Asegúrate de que la imagen tenga una extensión válida.", "danger")  # Mensaje de error
    return render_template('subir_imagen.html')  # Renderizar la plantilla para subir la imagen

# Ruta para listar todos los usuarios
@admin.route('/usuarios')
@login_required
def listar_usuarios():
    usuarios = User.query.all()  # Obtener todos los usuarios de la base de datos
    return render_template('tareas_admin/usuarios.html', usuarios=usuarios)  # Renderizar la plantilla con la lista de usuarios

# Función para verificar si un archivo tiene una extensión permitida
def allowed_file(filename):
    """Verifica si el archivo tiene una extensión permitida."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

# Rutas de administración de contenido
@admin.route('/contenido')
@login_required
def administracion_contenido():
    return render_template('tareas_admin/administracion_contenido.html')

# Rutas de administración de seguridad
@admin.route('/seguridad')
@login_required
def seguridad_accesos():
    return render_template('tareas_admin/seguridad_accesos.html')

# Rutas de gestión de correos
@admin.route('/correo')
@login_required
def gestion_correos():
    return render_template('tareas_admin/gestion_correos.html')

# Rutas de configuración del sitio
@admin.route('/configuracion')
@login_required
def configuracion_sitio():
    return render_template('tareas_admin/configuracion_sitio.html')

# Rutas de monitoreo y análisis
@admin.route('/monitoreo')
@login_required
def monitoreo_analisis():
    return render_template('tareas_admin/monitoreo_analisis.html')

# Rutas de gestión de pagos y finanzas
@admin.route('/Pagos')
@login_required
def gestion_pagos():
    return render_template('tareas_admin/gestion_pagos.html')

# Rutas de administración de base de datos
@admin.route('/Bases_de_datos')
@login_required
def administracion_base_datos():
    return render_template('tareas_admin/administracion_base_datos.html')

# Rutas de reportes
@admin.route('/Reportes')
@login_required
def reports():
    return render_template('tareas_admin/printreport.html')  # Mostrar la plantilla de reportes


# Aqui definiremos las rutas admin para añadir los productos finales para el cliente 

# Ruta para agregar productos
@admin.route('/admin/productos', methods=['GET', 'POST'])
@login_required
def agregar_producto():
    if current_user.role != 'admin':
        flash('No tienes permiso para acceder a esta página', 'danger')
        return redirect(url_for('main.index'))  # Redirigir si no es admin

    if request.method == 'POST':
        # Obtener los datos del formulario
        name = request.form.get('name')
        description = request.form.get('description')
        price = float(request.form.get('price'))
        image = request.files.get('image')
        video = request.files.get('video')

        # Subir los archivos si se proporcionan
        if image:
            image_filename = secure_filename(image.filename)
            image.save(f'instance/static/uploads/{image_filename}')
            image_url = f'uploads/{image_filename}'
        else:
            image_url = None

        if video:
            video_filename = secure_filename(video.filename)
            video.save(f'instance/static/uploads/{video_filename}')
            video_url = f'uploads/{video_filename}'
        else:
            video_url = None

        # Crear un nuevo producto en la base de datos
        new_product = Product(
            name=name,
            description=description,
            price=price,
            image_url=image_url,
            video_url=video_url,
            user_id=current_user.id  # Asumiendo que el producto está asociado al usuario actual
        )

        # Agregar el producto a la base de datos
        db.session.add(new_product)
        db.session.commit()

        flash('Producto agregado correctamente', 'success')
        return redirect(url_for('admin.agregar_producto'))  # Redirigir después de agregar el producto

    return render_template('admin/agregar_producto.html')

