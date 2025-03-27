# 🌟 Aplicación de Servicios de Fotografía

Esta aplicación es un sistema modular en **Flask** para gestionar servicios de fotografía, cursos de edición y videografía, reservas y pagos con integración de **Stripe** y **PayPal**.

## 🚀 Características
- 🎨 **Gestión de Servicios:** Sesiones de fotos, cursos de formación y video marketing.
- 🛍️ **Sistema de Pago:** Integración con **Stripe** y **PayPal**.
- 🔒 **Autenticación de Usuarios:** Flask-Login y Flask-WTF para formularios seguros.
- 📂 **Base de Datos SQLAlchemy:** Manejo de usuarios, productos y reservas con Flask-Migrate.
- 💻 **Sistema Modular:** Uso de Blueprints para separar la lógica en módulos.

---

## 👅 Instalación

### 🔹 1. Clonar el repositorio
```sh
git clone https://github.com/tuusuario/myapp.git
cd myapp
```

### 🔹 2. Crear y activar entorno virtual
```sh
# En Windows (PowerShell)
python -m venv myenv
myenv\Scripts\activate

# En macOS/Linux
python3 -m venv myenv
source myenv/bin/activate
```

### 🔹 3. Instalar dependencias
```sh
pip install -r requirements.txt
```

---

## 📂 Estructura del Proyecto
```
myapp/
│── instance/               # Bases de datos SQLite y archivos privados
│── migrations/             # Migraciones de la base de datos (Flask-Migrate)
│── models/                 # Modelos de la base de datos con SQLAlchemy
│   ├── usuario.py          # Modelo de usuarios
│   ├── producto.py         # Modelo de productos
│   ├── reserva.py          # Modelo de reservas
│   ├── pago.py             # Modelo de pagos
│   ├── __init__.py         # Inicialización de modelos
│── myenv/                  # Entorno virtual (excluido en .gitignore)
│── routes/                 # Módulos Flask con Blueprints
│   ├── auth.py             # Rutas de autenticación
│   ├── servicios.py        # Rutas de servicios fotográficos
│   ├── pago.py             # Rutas de pago (Stripe/PayPal)
│   ├── admin.py            # Panel de administración
│   ├── pedidos.py          # Gestión de pedidos y reservas
│   ├── __init__.py         # Inicialización de rutas
│── static/                 # Archivos estáticos (CSS, imágenes, videos)
│   ├── css/                # Estilos CSS
│   ├── images/             # Imágenes del sitio
│   │   ├── Bodas/
│   │   ├── Coches/
│   │   ├── Comida/
│   │   ├── Hombre/
│   │   ├── Mujer/
│   │   ├── Servicios/
│   │   ├── Urbana/
│   ├── video/              # Archivos de video
│── templates/              # Plantillas HTML
│   ├── base.html           # Base para todas las páginas
│   ├── index.html          # Página principal
│   ├── auth/               # Plantillas de autenticación
│   │   ├── login.html      # Iniciar sesión
│   │   ├── register.html   # Registro de usuario
│   │   ├── perfil.html     # Perfil del usuario
│   ├── servicios/          # Plantillas de servicios fotográficos
│   │   ├── formacion/      # Cursos y formación
│   │   │   ├── fotografia.html
│   │   │   ├── edicion.html
│   │   │   ├── videografia.html
│   │   ├── sesiones_fotos/ # Sesiones de fotografía
│   │   │   ├── estudio.html
│   │   │   ├── exterior.html
│   │   │   ├── bodas.html
│   │   ├── video_marketing/ # Servicios de video marketing
│   │   │   ├── publicidad.html
│   ├── pago/               # Páginas de pago y confirmación
│   │   ├── pago.html       # Formulario de pago
│   │   ├── pago_exitoso.html # Confirmación de pago
│   ├── admin/              # Panel de administración
│   │   ├── dashboard.html  # Panel principal
│   │   ├── usuarios.html   # Gestión de usuarios
│   │   ├── reportes.html   # Informes
│── uploads/                # Archivos subidos por usuarios
│── config.py               # Configuración de la aplicación (Base de Datos, Stripe, PayPal)
│── app.py                  # Archivo principal de la aplicación
│── requirements.txt        # Dependencias necesarias
│── README.md               # Documentación del proyecto



## ⚙️ Configuración

### 🔹 4. Configurar variables de entorno
Renombra `.env.example` a `.env` y edítalo con tus credenciales de **Stripe, PayPal y la base de datos**:
```sh
SECRET_KEY="tu_secreto"
STRIPE_PUBLIC_KEY="tu_public_key"
STRIPE_SECRET_KEY="tu_secret_key"
PAYPAL_CLIENT_ID="tu_client_id"
PAYPAL_CLIENT_SECRET="tu_client_secret"
DATABASE_URL="sqlite:///instance/usuarios.db"
```

---

## 🔄 Migraciones de la Base de Datos

Si es la primera vez que ejecutas la aplicación, inicializa la base de datos con:
```sh
flask db init
flask db migrate -m "Inicializar BD"
flask db upgrade
```

---

## 🌐 Ejecutar la Aplicación
Para iniciar el servidor Flask:
```sh
flask run
```
Abre tu navegador en: **http://127.0.0.1:5000**

---

## 💪 Autenticación y Usuarios

- Para registrarse, ve a `/registro`
- Para iniciar sesión, ve a `/login`

---

## 🛒 Pagos con Stripe y PayPal
La aplicación permite pagar servicios con **Stripe** y **PayPal**.

Para simular un pago con Stripe, usa la tarjeta de prueba:
```
4242 4242 4242 4242  (Fecha: Cualquiera | CVV: 123)
```

---

## 🔧 Tecnologías Usadas
- **Flask** - Framework web
- **Flask-Login** - Manejo de sesiones
- **Flask-WTF** - Formularios seguros
- **Flask-SQLAlchemy** - ORM para base de datos
- **Flask-Migrate** - Migraciones de base de datos
- **Stripe y PayPal SDK** - Procesamiento de pagos

---

## 💡 Notas Finales
- Asegúrate de que `myenv` esté activado antes de ejecutar Flask.
- No compartas tu `SECRET_KEY` ni credenciales de pago.

🛠️ **Autor:** Marcus Hinestroza
🌟 **Proyecto:** Servicios de Fotografía con Flask  
👥 **Contacto:** alumno311emies@gmail.com
```

# Hinestroza Torres Marcus-C
usuario administrador 
admin@mht.com   password: admin3428