# Importamos las librerías necesarias
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# Inicializamos la aplicación Flask
app = Flask(__name__)

# Configuración de la base de datos SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'clave_secreta'  # Clave para manejar sesiones

# Inicializamos la base de datos
db = SQLAlchemy(app)

# -------------------------
# 📌 MODELO DE USUARIO
# -------------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # ID único de usuario
    username = db.Column(db.String(50), unique=True, nullable=False)  # Nombre de usuario único
    email = db.Column(db.String(100), unique=True, nullable=False)  # Correo único
    password = db.Column(db.String(256), nullable=False)  # Contraseña cifrada

# -------------------------
# 📌 RUTA: PÁGINA PRINCIPAL
# -------------------------
@app.route('/')
def index():
    return render_template('index.html')

# -------------------------
# 📌 RUTA: REGISTRO DE USUARIOS
# -------------------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Cifrar la contraseña antes de guardarla
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        # Crear usuario y guardarlo en la base de datos
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))  # Redirigir al login tras registrarse
    
    return render_template('register.html')

# -------------------------
# 📌 RUTA: INICIO DE SESIÓN
# -------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Buscar usuario por su email
        user = User.query.filter_by(email=email).first()

        # Verificar si el usuario existe y si la contraseña es correcta
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id  # Guardar usuario en sesión
            return redirect(url_for('dashboard'))
        else:
            return "Credenciales incorrectas, intenta nuevamente."

    return render_template('login.html')

# -------------------------
# 📌 RUTA: DASHBOARD (SOLO USUARIOS AUTENTICADOS)
# -------------------------
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))  # Redirigir si no está autenticado

    return render_template('dashboard.html')

# -------------------------
# 📌 RUTA: CERRAR SESIÓN
# -------------------------
@app.route('/logout')
def logout():
    session.pop('user_id', None)  # Eliminar la sesión del usuario
    return redirect(url_for('index'))

# -------------------------
# 📌 CREAR BASE DE DATOS
# -------------------------
with app.app_context():
    db.create_all()  # Crea la base de datos si no existe

# -------------------------
# 📌 EJECUTAR LA APLICACIÓN
# -------------------------
if __name__ == '__main__':
    app.run(debug=True)
