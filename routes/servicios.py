# Importación de módulos necesarios de Flask para gestionar rutas y plantillas.
from flask import Blueprint, render_template

# Crear un Blueprint llamado 'servicioso' que contiene las rutas relacionadas con los servicios.
# Especificamos que los templates estarán en una carpeta diferente ('../templates/servicios'), 
# fuera del directorio de plantillas principal de la aplicación.
servicioso = Blueprint('servicioso', __name__, template_folder='../templates/servicios')

# Rutas para la sección de 'formación' de los servicios.
# Cada una de estas rutas renderiza una plantilla HTML específica relacionada con los cursos y formaciones.

# Ruta para la página de edición de los cursos en la formación.
@servicioso.route('/formacion/edicion')
def formacion_edicion():
    # Renderiza la plantilla 'curso_edicion.html' dentro de la carpeta 'servicios/formacion'.
    return render_template('servicios/formacion/curso_edicion.html')

# Ruta para la página de formación en fotografía.
@servicioso.route('/formacion/fotografia')
def formacion_fotografia():
    # Renderiza la plantilla 'fotografia.html' dentro de la carpeta 'servicios/formacion'.
    return render_template('servicios/formacion/fotografia.html')

# Ruta para la página de formación en videografía.
@servicioso.route('/formacion/videografia')
def formacion_videografia():
    # Renderiza la plantilla 'curso_videografia.html' dentro de la carpeta 'servicios/formacion'.
    return render_template('servicios/formacion/curso_videografia.html')

# Rutas para la sección de 'sesiones de fotos' de los servicios.
# Estas rutas renderizan páginas específicas para los diferentes tipos de sesiones de fotos que ofrece el servicio.

# Ruta para la página de sesiones fotográficas en el estudio.
@servicioso.route('/sesiones_fotos/estudio')
def sesiones_estudio():
    # Renderiza la plantilla 'estudio.html' dentro de la carpeta 'servicios/sesiones_fotos'.
    return render_template('servicios/sesiones_fotos/estudio.html')

# Ruta para la página de sesiones fotográficas al aire libre (exterior).
@servicioso.route('/sesiones_fotos/exterior')
def sesiones_exterior():
    # Renderiza la plantilla 'exterior.html' dentro de la carpeta 'servicios/sesiones_fotos'.
    return render_template('servicios/sesiones_fotos/exterior.html')

# Ruta para la página de sesiones fotográficas para bodas.
@servicioso.route('/sesiones_fotos/bodas')
def sesiones_bodas():
    # Renderiza la plantilla 'bodas.html' dentro de la carpeta 'servicios/sesiones_fotos'.
    return render_template('servicios/sesiones_fotos/bodas.html')

# Rutas para la sección de 'video marketing' y 'publicidad' de los servicios.
# Esta ruta renderiza la página que habla sobre los servicios de video marketing relacionados con publicidad.

# Ruta para la página de video marketing y publicidad.
@servicioso.route('/video_marketing/publicidad')
def video_publicidad():
    # Renderiza la plantilla 'publicidad.html' dentro de la carpeta 'servicios/video_marketing'.
    return render_template('servicios/video_marketing/publicidad.html')
