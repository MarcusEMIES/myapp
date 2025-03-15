from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from models import db  # Asegúrate de que 'db' esté importado correctamente desde 'models'
from models.users import User  # Importa el modelo User
from flask_login import login_user  # Importa login_user desde Flask-Login

# Creamos el blueprint para la autenticación
auth = Blueprint('auth', __name__)

# Ruta para el login
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password_hash, password):  # Correcto: Verificamos el password_hash
            login_user(user)  # Usamos Flask-Login para manejar la sesión
            return redirect(url_for('tasks.dashboard'))  # Redirige al dashboard o página principal
        else:
            flash('Credenciales inválidas', 'danger')  # Flash en caso de error
    return render_template('login.html')

# Ruta para el registro
@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Verificar que las contraseñas coinciden
        if password != confirm_password:
            flash("Las contraseñas no coinciden.", "danger")
            return redirect(url_for('auth.register'))

        # Verificar si el nombre de usuario ya existe
        if User.query.filter_by(username=username).first():
            flash("El nombre de usuario ya existe.", "danger")
            return redirect(url_for('auth.register'))

        # Verificar si el correo ya está registrado
        if User.query.filter_by(email=email).first():
            flash("El correo ya está registrado.", "danger")
            return redirect(url_for('auth.register'))

        # Hash de la contraseña y creación del nuevo usuario
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, email=email, password_hash=hashed_password)  # Se usa 'password_hash'
        db.session.add(new_user)
        db.session.commit()

        flash("Registro exitoso. Ahora puedes iniciar sesión.", "success")
        return redirect(url_for('auth.login'))  # Redirige al login

    return render_template('register.html')

# Otras rutas como "about", "políticas", etc.
@auth.route('/about')
def about():
    return render_template('about.html')

@auth.route('/politicas')
def politicas():
    return render_template('politicas.html')

@auth.route('/preguntas_frecuentes')
def preguntas_frecuentes():
    return render_template('preguntas_frecuentes.html')

@auth.route('/contacto')
def contacto():
    return render_template('contacto.html')
