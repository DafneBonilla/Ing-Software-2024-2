from flask import Blueprint, render_template, request, flash, url_for, redirect
from alchemyClasses.Peliculas import Peliculas
from alchemyClasses.Rentar import Rentar
from alchemyClasses import db

pelicula_blueprint = Blueprint('pelicula', __name__, url_prefix='/pelicula')

"""
Movies are deleted and modified by id in order to avoid posible mistakes.
"""

# Route to add a movie -> localhost:5001/pelicula/agregar
@pelicula_blueprint.route('/agregar', methods=['GET', 'POST'])
def add_movie():
    if request.method == 'GET':
        return render_template('agregar_pelicula.html')
    else:
        nombre = request.form.get('nombre')
        genero = request.form.get('genero')
        duracion = request.form.get('duracion')
        inventario = request.form.get('inventario')
        if not nombre:
            flash('Falta el campo nombre.', 'error')
            return redirect(url_for('pelicula.agregar_pelicula'))
        # Convert duration and inventory to int if provided
        duracion = int(duracion) if duracion else None
        inventario = int(inventario) if inventario else 1
        new_movie = Peliculas(nombre = nombre, genero = genero, duracion = duracion, inventario = inventario)
        try:
            db.session.add(new_movie)
            db.session.commit()
            flash('Pelicula añadida correctamente.', 'success')
            return redirect(url_for('pelicula.ver_peliculas'))
        except Exception as e:
            db.session.rollback()
            flash('Error al agregar película. Detalles: {}'.format(str(e)), 'error')
            return redirect(url_for('pelicula.agregar_pelicula'))

# Route to modify movie -> localhost:5001/pelicula/modificar
@pelicula_blueprint.route('/modificar', methods=['GET', 'POST'])
def modify_movie():
    if request.method == 'POST':
        id_movie = request.form.get('id_pelicula')
        try:
            # Convert id to int when provided
            id_movie = int(id_movie)
            return redirect(url_for('pelicula.modificar_pelicula_id', id = id_movie))
        except ValueError:
            flash('Ops! ID inválido, ingrese un ID válido nuevamente', 'error')
    return render_template('solicitar_id_pelicula.html')

# Route to modify movie by id -> localhost:5001/pelicula/odificar/<int:id>
@pelicula_blueprint.route('/modificar/<int:id>', methods=['GET', 'POST'])
def modify_movie_id(id):
    pelicula = Peliculas.query.get(id)
    if not pelicula:
        return render_template('pelicula_no_encontrada.html')
    if request.method == 'GET':
        return render_template('modificar_pelicula.html', pelicula = pelicula)
    elif request.method == 'POST':
        pelicula.nombre = request.form.get('nombre')
        pelicula.genero = request.form.get('genero')
        pelicula.duracion = request.form.get('duracion')
        pelicula.inventario = request.form.get('inventario')
        if not pelicula.nombre:
            flash('Ops! Falta el nombre de la película', 'error')
            return render_template('modificar_pelicula.html', pelicula = pelicula)
        # Convert duration and inventory to int if provided
        pelicula.duracion = int(pelicula.duracion) if pelicula.duracion else None
        pelicula.inventario = int(pelicula.inventario) if pelicula.inventario else 1
        try:
            db.session.commit()
            flash('La película se modificó correctamente.', 'success')
            return redirect(url_for('pelicula.ver_peliculas'))
        except Exception as e:
            db.session.rollback()
            flash('Error al modificar película. Detalles: {}'.format(str(e)), 'error')
            return redirect(url_for('pelicula.modificar_pelicula_id', id = id))

# Route to delete movie -> localhost:5001/pelicula/eliminar
@pelicula_blueprint.route('/eliminar', methods=['GET', 'POST'])
def delete_movie():
    if request.method == 'POST':
        id_movie = request.form.get('id_pelicula')
        try:
            id_movie = int(id_movie)
            return redirect(url_for('pelicula.eliminar_pelicula_id', id = id_movie))
        except ValueError:
            flash('Ops! ID inválido, ingrese un ID válido nuevamente', 'error')
    return render_template('solicitar_id_pelicula.html')

# Route to delete movie by id -> localhost:5001/pelicula/eliminar/<int:id>
@pelicula_blueprint.route('/eliminar/<int:id>', methods=['GET', 'POST'])
def delete_movie_id(id):
    pelicula = Peliculas.query.get(id)
    if not pelicula:
        return render_template('pelicula_no_encontrada.html')
    else:
        rentas = Rentar.query.filter_by(idPelicula=pelicula.idPelicula).all()
        if rentas:
            flash('No es posible eliminar la película debido a que tiene rentas asociadas', 'error')
        else:
            try:
                db.session.delete(pelicula)
                db.session.commit()
                flash('La película fue eliminada correctamente', 'success')
            except Exception as e:
                db.session.rollback()
                flash('Error al eliminar película. Detalles: {}'.format(str(e)), 'error')
        return redirect(url_for('pelicula.ver_peliculas'))
