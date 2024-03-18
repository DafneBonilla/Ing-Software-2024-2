from flask import Blueprint, render_template, request, flash, url_for, redirect
from datetime import datetime, timedelta, date
from alchemyClasses.Peliculas import Peliculas
from alchemyClasses.Usuarios import Usuarios
from alchemyClasses.Rentar import Rentar
from alchemyClasses import db

renta_blueprint = Blueprint('renta', __name__, url_prefix='/renta')

"""
Rents are modified by id in order to avoid posible mistakes.
"""

# Route to add a movie -> localhost:5001/renta/agregar
@renta_blueprint.route('/')
def watch_rents():
    try:
        rents = Rentar.query.all()
        rents_data = []
        for renta in rents:
            fecha_vencimiento = renta.fecha_renta + timedelta(days=renta.dias_de_renta)
            renta_pasada = fecha_vencimiento < datetime.combine(date.today(), datetime.min.time())
            rents_data.append({'renta': renta, 'renta_pasada': renta_pasada})
        return render_template('rentas/rents.html', rentas=rents_data)
    except Exception as e:
        print("Ocurrió un error:", str(e))
        return "Ocurrió un error. Por favor, inténtalo de nuevo más tarde."

# Route to add a rent -> localhost:5001/renta/agregar
@renta_blueprint.route('/agregar', methods=['GET', 'POST'])
def add_rent():
    if request.method == 'GET':
        return render_template('rentas/rent_add.html')
    else:
        try:
            idUsuario = request.form.get('idUsuario')
            idPelicula = request.form.get('idPelicula')
            fecha_renta = request.form.get('fecha_renta')
            dias_renta = request.form.get('dias_de_renta')
            estatus = True if request.form.get('estatus') else False
            if not idUsuario or not idPelicula:
                flash('Faltan campos por llenar', 'error')
                return redirect(url_for('renta.agregar_renta'))
            usuario = Usuarios.query.filter_by(idUsuario = idUsuario).first()
            if not usuario:
                flash('El usuario no está registrado', 'error')
                return redirect(url_for('renta.agregar_renta'))
            pelicula = Peliculas.query.filter_by(idPelicula=idPelicula).first()
            if not pelicula:
                flash('La película no está registrada', 'error')
                return redirect(url_for('renta.agregar_renta'))
            fecha_renta = fecha_renta or date.today()
            dias_renta = int(dias_renta) if dias_renta else 5
            new_rent = Rentar(idUsuario = idUsuario, idPelicula = idPelicula, fecha_renta = fecha_renta, dias_de_renta = dias_renta, estatus = estatus)
            db.session.add(new_rent)
            db.session.commit()
            flash('La renta se agregó correctamente', 'success')
            return redirect(url_for('renta.ver_rentas'))
        except Exception as e:
            flash(f'Ocurrió un error al agregar la renta: {str(e)}', 'error')
            return redirect(url_for('renta.agregar_renta'))

# Route to modify rent -> localhost:5001/renta/modificar
@renta_blueprint.route('/modificar', methods=['GET', 'POST'])
def modify_rent():
    if request.method == 'POST':
        try:
            id_renta = int(request.form.get('id_renta'))
            return redirect(url_for('renta.modificar_renta_id', id = id_renta))
        except ValueError:
            flash('Ops! ID inválido, ingrese un ID válido nuevamente', 'error')
            return redirect(url_for('renta.modificar_renta'))
    return render_template('rentas/rent_id.html')

# Route to modify rent by id -> localhost:5001/renta/modificar/<int:id>
@renta_blueprint.route('/modificar/<int:id>', methods=['GET', 'POST'])
def modify_rent_id(id):
    try:
        renta = Rentar.query.get(id)
        if not renta:
            return render_template('rentas/rent_not_found.html')
        if request.method == 'GET':
            return render_template('rentas/rent_modify.html', renta=renta)
        elif request.method == 'POST':
            renta.estatus = True if request.form.get('estatus') else False
            db.session.commit()
            flash('La renta se modificó correctamente', 'success')
            return redirect(url_for('renta.ver_rentas'))
    except Exception as e:
        flash(f'Ocurrió un error al modificar la renta: {str(e)}', 'error')
        return redirect(url_for('renta.ver_rentas'))
