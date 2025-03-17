from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from flask_login import login_user, login_required, logout_user
from models.users import User
from models import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('tasks.dashboard'))
        flash("Credenciales incorrectas.", "danger")

    return render_template('login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash("Las contraseñas no coinciden.", "danger")
            return redirect(url_for('auth.register'))

        if User.query.filter_by(username=username).first():
            flash("El nombre de usuario ya existe.", "danger")
            return redirect(url_for('auth.register'))

        if User.query.filter_by(email=email).first():
            flash("El correo ya está registrado.", "danger")
            return redirect(url_for('auth.register'))

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash("Registro exitoso. Ahora puedes iniciar sesión.", "success")
        return redirect(url_for('auth.login'))

    return render_template('register.html')

@auth.route('/logout')
def logout():
    logout_user()
    flash("Sesión cerrada exitosamente", "success")
    return redirect(url_for('index'))
