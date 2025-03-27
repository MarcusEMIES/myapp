# Importación de módulos necesarios de Flask para gestionar rutas, plantillas, peticiones y mensajes flash.
from flask import Blueprint, render_template, request, redirect, url_for, flash
# Importación de una función para generar el hash de las contraseñas de forma segura.
from werkzeug.security import generate_password_hash
# Importación de funciones para gestionar el inicio y cierre de sesión del usuario.
from flask_login import login_user, login_required, logout_user
# Importación del modelo 'User' que define la estructura y métodos de los usuarios.
from models.users import User
# Importación de la base de datos para interactuar con la misma.
from models import db

# Creación del Blueprint llamado 'auth', que contiene rutas relacionadas con autenticación.
auth = Blueprint('auth', __name__)

# Ruta para el inicio de sesión de los usuarios.
@auth.route('/login', methods=['GET', 'POST'])
def login():
    # Si la petición es de tipo 'POST' (formulario enviado).
    if request.method == 'POST':
        # Se obtiene el correo y la contraseña del formulario.
        email = request.form['email']
        password = request.form['password']
        # Se consulta si hay un usuario con el correo proporcionado.
        user = User.query.filter_by(email=email).first()
        
        # Si se encuentra el usuario y la contraseña es correcta.
        if user and user.check_password(password):
            # Se inicia sesión con el usuario encontrado.
            login_user(user)
            # Se redirige al dashboard de tareas.
            return redirect(url_for('tasks.dashboard'))
        
        # Si las credenciales son incorrectas, se muestra un mensaje de error.
        flash("Usuario y contraseña no existen, verifique sus datos o registrese", "danger")

    # Si la petición es 'GET' o si hay un error, se renderiza la plantilla de login.
    return render_template('login.html')

# Ruta para el registro de nuevos usuarios.
@auth.route('/register', methods=['GET', 'POST'])
def register():
    # Si la petición es de tipo 'POST' (formulario enviado).
    if request.method == 'POST':
        # Se obtienen los valores del formulario.
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Si las contraseñas no coinciden, se muestra un mensaje de error.
        if password != confirm_password:
            flash("Las contraseñas no coinciden.", "danger")
            return redirect(url_for('auth.register'))

        # Se verifica si ya existe un usuario con el mismo nombre de usuario.
        if User.query.filter_by(username=username).first():
            flash("El nombre de usuario ya existe.", "danger")
            return redirect(url_for('auth.register'))

        # Se verifica si ya existe un usuario con el mismo correo electrónico.
        if User.query.filter_by(email=email).first():
            flash("El correo ya está registrado.", "danger")
            return redirect(url_for('auth.register'))

        # Si todo es correcto, se genera un hash seguro para la contraseña.
        hashed_password = generate_password_hash(password)
        # Se crea un nuevo usuario con los datos proporcionados y la contraseña encriptada.
        new_user = User(username=username, email=email, password_hash=hashed_password)
        # Se añade el nuevo usuario a la base de datos.
        db.session.add(new_user)
        db.session.commit()

        # Se muestra un mensaje de éxito y se redirige al login.
        flash("Registro exitoso. Ahora puedes iniciar sesión.", "success")
        return redirect(url_for('auth.login'))

    # Si la petición es 'GET' o si hay un error, se renderiza la plantilla de registro.
    return render_template('register.html')

# Ruta para cerrar sesión del usuario.
@auth.route('/logout')
def logout():
    # Se cierra la sesión del usuario actual.
    logout_user()
    # Se muestra un mensaje de éxito indicando que la sesión fue cerrada.
    flash("Sesión cerrada exitosamente", "success")
    # Se redirige al usuario a la página de inicio.
    return redirect(url_for('index'))
