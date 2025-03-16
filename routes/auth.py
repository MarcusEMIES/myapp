#Configuracion de autenticacion routes/auth.py
from models.users import User
from models import db # Ahora puedes importar db y User sin problemas
from flask_login import login_user, login_required, logout_user
from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash




# Crear un Blueprint para la autenticación
auth = Blueprint('auth', __name__)

# -------------------------
# Ruta de login
# -------------------------
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Busca el usuario en la base de datos por el email
        user = User.query.filter_by(email=email).first()


        # Si el usuario existe y la contraseña es correcta
        if user and user.check_password(password):
            login_user(user)  # Inicia la sesión
            flash("Inicio de sesión exitoso", "success")
            login_required
            return redirect(url_for('dashboard'))  # Redirige al dashboard
        else:
            flash("Credenciales incorrectas.", "danger")
    return render_template('login.html')

# -------------------------
# Ruta de registro
# -------------------------


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Validaciones
        if password != confirm_password:
            flash("Las contraseñas no coinciden.", "danger")
            return redirect(url_for('auth.register'))

        if User.query.filter_by(username=username).first():
            flash("El nombre de usuario ya existe.", "danger")
            print("El nombre de usuario ya existe.")
            return redirect(url_for('auth.register'))

        if User.query.filter_by(email=email).first():
            flash("El correo electrónico ya está registrado.", "danger")
            return redirect(url_for('auth.register'))

        # Crear el nuevo usuario
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, email=email, password_hash=hashed_password)

        db.session.add(new_user)
        db.session.commit()

        # Iniciar sesión automáticamente después del registro
        login_user(new_user)

        flash("Registro exitoso. Ahora estás logueado.", "success")
        return redirect(url_for('dashboard'))  # Redirige a la página principal o al panel del usuario después del registro

    return render_template('register.html')

# -------------------------
# Ruta de logout
# -------------------------
@auth.route('/logout')

def logout():
    logout_user()
    flash("Sesión cerrada exitosamente", "success")
    return redirect(url_for('index'))  # Redirige a la página principal
