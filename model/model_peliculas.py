from alchemyClasses.Peliculas import Peliculas
from alchemyClasses import db
from alchemyClasses.Rentar import Rentar

'''
Function to retrieve and display all movies from the database
'''
def show_movies():
    movies = Peliculas.query.all()
    for movie in movies:
        print(movie)

'''
Function to filter movies by their ID and display the result
'''
def filter_movie(id_movie):
    movie = Peliculas.query.filter_by(idPelicula = id_movie).one_or_none()
    if movie:
        print(movie)
    else:
        print("No movie exists with that id")

'''
Function to update the name of a movie based on its ID
'''
def update_name(id_movie, new_name):
    movie = Peliculas.query.filter_by(idPelicula = id_movie).first_or_404()
    movie.name = new_name
    db.session.commit()
    print("Movie updated")

'''
Function to delete a movie from the database by its ID.
'''
def delete_movie(id_movie):
    movie = Peliculas.query.filter_by(idPelicula = id_movie).first()
    if movie:
        rents = Rentar.query.filter_by(idPelicula = movie.idPelicula).all()
        if rents:
            print("Movie with associated rentals, it can't be delete it")
            return
        else:
            db.session.delete(movie)
            db.session.commit()
            print("Movie deleted successfully!")
    else:
        print("No movie exists with that id or it has been deleted already")

'''
Function to delete all movies from the database.
'''
def delete_all():
    has_rentals = db.session.query(Rentar.query.exists()).scalar()
    if not has_rentals:
        Peliculas.query.delete()
        db.session.commit()
        print("All movies deleted")
    else:
        print("Some movies have associated rentals, deletion aborted")
