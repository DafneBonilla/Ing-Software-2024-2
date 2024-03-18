from flask import Blueprint, render_template, request, flash, url_for, redirect
from alchemyClasses.Usuarios import Usuarios
from alchemyClasses.Rentar import Rentar
from alchemyClasses import db

usuario_blueprint = Blueprint('usuario', __name__, url_prefix='/usuario')

"""
Users are deleted and modified by id in order to avoid posible mistakes.
"""

# Route to see users -> localhost:5001/usuario/
@usuario_blueprint.route('/')
def watch_users():
    usuarios = Usuarios.query.all()
    return render_template('usuarios.html', usuarios=usuarios)

# Route to add a user -> localhost:5001/usuario/agregar
@usuario_blueprint.route('/agregar', methods=['GET', 'POST'])
def add_user():
    if request.method == 'GET':
        return render_template('agregar_usuario.html')
    else:
        try:
            nombre = request.form.get('nombre')
            apPat = request.form.get('apPat')
            apMat = request.form.get('apMat')
            password = request.form.get('password')
            email = request.form.get('email')
            superUser = bool(request.form.get('superUser'))
            if not all((nombre, apPat, password, email)):
                flash('Faltan campos por llenar', 'error')
                return redirect(url_for('usuario.agregar_usuario'))
            if Usuarios.query.filter_by(email = email).first():
                flash('Ya hay una cuenta asociada a esta dirección de correo electrónico', 'error')
                return render_template('agregar_usuario.html')
            new_user = Usuarios(nombre = nombre, apPat = apPat, apMat = apMat, password = password, email = email, superUser = superUser)
            db.session.add(new_user)
            db.session.commit()
            flash('Usuario agregado', 'success')
            return redirect(url_for('usuario.ver_usuarios'))
        except Exception as e:
            flash(f'Error al agregar usuario: {str(e)}', 'error')
            return redirect(url_for('usuario.agregar_usuario'))

# Route to modify user -> localhost:5001/usuario/modificar
@usuario_blueprint.route('/modificar', methods=['GET', 'POST'])
def modify_user():
    if request.method == 'POST':
        id_usuario = request.form.get('id_usuario')
        try:
            id_usuario = int(id_usuario)
            return redirect(url_for('usuario.modificar_usuario_id', id = id_usuario))
        except ValueError:
            flash('Ops! ID inválido, ingrese un ID válido nuevamente', 'error')
    return render_template('solicitar_id_usuario.html')

# Route to modify user by id -> localhost:5001/usuario/modificar/<int:id>
@usuario_blueprint.route('/modificar/<int:id>', methods=['GET', 'POST'])
def modify_user_id(id):
    usuario = Usuarios.query.get(id)
    if not usuario:
        return render_template('usuario_no_encontrado.html')
    if request.method == 'GET':
        return render_template('modificar_usuario.html', usuario=usuario)
    elif request.method == 'POST':
        new_email = request.form['email']
        old_email = Usuarios.query.filter(
            (Usuarios.email == new_email) & (Usuarios.idUsuario != usuario.idUsuario)).first()
        if old_email:
            flash('El correo electrónico ya está en uso.', 'error')
            return render_template('modificar_usuario.html', usuario = usuario)
        usuario.nombre = request.form['nombre']
        usuario.apPat = request.form['apPat']
        usuario.apMat = request.form['apMat']
        usuario.password = request.form['password']
        usuario.email = new_email
        usuario.superUser = bool(request.form.get('superUser'))
        if not all((usuario.nombre, usuario.apPat, usuario.password, usuario.email)):
            flash('Faltan campos por llenar', 'error')
            return render_template('modificar_usuario.html', usuario = usuario)
        try:
            db.session.commit()
            flash('Usuario modificado', 'success')
            return redirect(url_for('usuario.ver_usuarios'))
        except Exception as e:
            flash(f'Error al modificar usuario: {str(e)}', 'error')
            return render_template('modificar_usuario.html', usuario = usuario)

# Route to delete user -> localhost:5001/usuario/eliminar
@usuario_blueprint.route('/eliminar', methods=['GET', 'POST'])
def delete_user():
    if request.method == 'POST':
        id_usuario = request.form.get('id_usuario')
        try:
            id_usuario = int(id_usuario)
            return redirect(url_for('usuario.eliminar_usuario_id', id = id_usuario))
        except ValueError:
            flash('Ops! ID inválido, ingrese un ID válido nuevamente', 'error')
    return render_template('solicitar_id_usuario.html')

# Route to delete user by id -> localhost:5001/usuario/eliminar/<int:id>
@usuario_blueprint.route('/eliminar/<int:id>', methods=['GET', 'POST'])
def delete_user_id(id):
    usuario = Usuarios.query.get(id)
    if not usuario:
        return render_template('usuario_no_encontrado.html')
    rentas = Rentar.query.filter_by(idUsuario = usuario.idUsuario).all()
    if rentas:
        flash('No es posible eliminar al usuario debido a que tiene rentas asociadas', 'error')
    else:
        try:
            db.session.delete(usuario)
            db.session.commit()
            flash('El usuario se eliminó correctamente', 'success')
        except Exception as e:
            flash(f'Error al eliminar usuario: {str(e)}', 'error')
    return redirect(url_for('usuario.ver_usuarios'))
