# from flask import Blueprint
# from models.db1_models import UsuarioDB1
# from models.mensajes import_
# from models import db

# # Crear un Blueprint para organizar la ruta
# importacion_bp = Blueprint('importacion', __name__)

# @importacion_bp.route('/importar_datos', methods=['POST'])
# def importar_datos():
#     # Obtener todos los usuarios de la base de datos 1
#     usuarios_db1 = UsuarioDB1.query.all()

#     # Insertar los usuarios en la base de datos 2
#     for usuario in usuarios_db1:
#         nuevo_usuario = UsuarioDB2(nombre=usuario.nombre, email=usuario.email)
#         db.session.add(nuevo_usuario)

#     db.session.commit()  # Confirmar los cambios en db2

#     return "Datos importados correctamente"
