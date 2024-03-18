from sqlalchemy import Column, Integer, String
from alchemyClasses import db

'''
Class that represents the movie table in the database
'''
class Peliculas(db.Model):
    # Table
    __tablename__ = 'peliculas'
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4'}
    # Columns
    idPelicula = Column(Integer, primary_key = True, autoincrement = True)
    nombre = Column(String(200), nullable = False)
    genero = Column(String(45), default = None)
    duracion = Column(Integer, default = None)
    inventario = Column(Integer, default = 1, nullable = False)

    '''
    Function to create a movie object
    '''
    def __init__(self, nombre, genero = None, duracion = None, inventario = None):
        self.nombre = nombre
        self.genero = genero
        self.duracion = duracion
        self.inventario = inventario

    '''
    Function to represent the movie object as a string
    '''
    def __str__(self):
        return f"<Pelicula(Pelicula Id ='{self.idPelicula}', Nombre = '{self.nombre}', Genero = '{self.genero}', " \
                f"Duracion = {self.duracion}, Inventario = {self.inventario})>"