from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_required, current_user
from models.products import Product
from flask import  abort
from io import BytesIO
from zipfile import ZipFile


portafolio = Blueprint('portafolio', __name__)

# Página del portafolio (formulario + contenido si tiene acceso)
@portafolio.route('/portafolio/cliente', methods=['GET'])
@login_required
def portafolio_cliente():
    content_access = session.get('portafolio_access', False)
    archivos = Product.query.filter_by(user_id=current_user.id).all()

    return render_template('portafolios/portafolio_cliente.html',
                           archivos=archivos,
                           content_access=content_access,
                           error=session.pop('portafolio_error', None))

# Procesar el formulario de contraseña
@portafolio.route('/portafolio/validar', methods=['POST'])
@login_required
def ingresar_contraseña():
    contraseña = request.form.get('password')
    productos = Product.query.filter_by(user_id=current_user.id).all()

    # Verificar si la contraseña coincide con algún producto del usuario
    for p in productos:
        if p.contraseña_producto == contraseña:
            session['portafolio_access'] = True
            flash("¡Acceso concedido!", "success")
            return redirect(url_for('portafolio.portafolio_cliente'))

    # Si no coincide
    session['portafolio_access'] = False
    session['portafolio_error'] = "Contraseña incorrecta."
    return redirect(url_for('portafolio.portafolio_cliente'))


#Opcion para que el cliente pueda descargar todo en un zip

import zipfile
import io
from flask import send_file
import os

@portafolio.route('/descargar_todo')
@login_required
def descargar_todo():
    archivos = Product.query.filter_by(user_id=current_user.id).all()
    memory_file = io.BytesIO()

    with zipfile.ZipFile(memory_file, 'w') as zf:
        for producto in archivos:
            # Añadir imágenes
            if producto.image_urls:
                for path in producto.image_urls.split(';'):
                    filepath = os.path.join('static', path.strip())
                    if os.path.exists(filepath):
                        zf.write(filepath, arcname=os.path.basename(filepath))

            # Añadir videos
            if producto.video_urls:
                for path in producto.video_urls.split(';'):
                    filepath = os.path.join('static', path.strip())
                    if os.path.exists(filepath):
                        zf.write(filepath, arcname=os.path.basename(filepath))

    memory_file.seek(0)
    return send_file(memory_file, download_name='portafolio.zip', as_attachment=True)


#Ruta para descargar el book completo

@portafolio.route('/descargar_book/<int:book_id>')
@login_required
def descargar_todo_por_book(book_id):
    producto = Product.query.get_or_404(book_id)
    if producto.user_id != current_user.id and current_user.role != 'admin':
        abort(403)

    # Archivos a incluir
    files = []
    if producto.image_urls:
        files += [os.path.join('static', img.strip()) for img in producto.image_urls.split(';')]
    if producto.video_urls:
        files += [os.path.join('static', vid.strip()) for vid in producto.video_urls.split(';')]

    # Crear el ZIP
    zip_stream = BytesIO()
    with ZipFile(zip_stream, 'w') as zipf:
        for file in files:
            zipf.write(file, os.path.basename(file))
    zip_stream.seek(0)

    return send_file(zip_stream,
                     mimetype='application/zip',
                     as_attachment=True,
                     download_name=f'{producto.name}_portafolio.zip')