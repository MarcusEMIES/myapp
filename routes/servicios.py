from flask import Blueprint, render_template

# Crear el Blueprint
servicioso = Blueprint('servicioso', __name__, template_folder='../templates/servicios')

# Rutas para la sección de formación
@servicioso.route('/formacion/edicion')
def formacion_edicion():
    return render_template('servicios/formacion/curso_edicion.html')

@servicioso.route('/formacion/fotografia')
def formacion_fotografia():
    return render_template('servicios/formacion/fotografia.html')

@servicioso.route('/formacion/videografia')
def formacion_videografia():
    return render_template('servicios/formacion/curso_videografia.html')

# Rutas para la sección de sesiones de fotos
@servicioso.route('/sesiones_fotos/estudio')
def sesiones_estudio():
    return render_template('servicios/sesiones_fotos/estudio.html')

@servicioso.route('/sesiones_fotos/exterior')
def sesiones_exterior():
    return render_template('servicios/sesiones_fotos/exterior.html')

@servicioso.route('/sesiones_fotos/bodas')
def sesiones_bodas():
    return render_template('servicios/sesiones_fotos/bodas.html')

# Rutas para la sección de video marketing y publicidad
@servicioso.route('/video_marketing/publicidad')
def video_publicidad():
    return render_template('servicios/video_marketing/publicidad.html')
