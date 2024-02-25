import pymysql
import random
from cryptoUtils.CryptoUtils import cipher
from hashlib import sha256

'''
Function to connect to the database
'''
def connect_to_database():
    connection = pymysql.connect(host='localhost',
                                 user='lab',
                                 password='Developer123!',
                                 database='lab_ing_software',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection

'''
Function to insert records in the database
'''
def insert_records():
    connection = connect_to_database()
    try:
        with connection.cursor() as cursor:
            # Inserting a record into the users table
            sql_usarios = "INSERT INTO usarios (nombre, apPat, apMat, password, email, superUser) VALUES (%s, %s, %s, %s, %s, %s)"
            # Inserting a record into the movies table
            sql_peliculas = "INSERT INTO peliculas (nombre, genero, duracion, inventario) VALUES (%s, %s, %s, %s)"
            # Inserting a record into the rent table
            sql_rentar = "INSERT INTO rentar (idUsuario, idPelicula, fecha_renta, dias_de_renta, estatus) VALUES (%s, %s, NOW(), %s, %s)"
            
            # Selecting userId and movieId
            cursor.execute("SELECT idUsuario FROM usarios LIMIT 1")
            idUsuario = cursor.fetchone()['idUsuario']
            cursor.execute("SELECT idPelicula FROM peliculas LIMIT 1")
            idPelicula = cursor.fetchone()['idPelicula']
            
            # Loop for multiple inserts
            for _ in range(3):  # Inserting 3 records
                random_num = random.randint(0, 1000)
                user = f'User{random_num}'
                random_num = random.randint(0, 1000)
                apPat = f'ApPat{random_num}'
                random_num = random.randint(0, 1000)
                apMat = f'ApMat{random_num}'
                random_num = random.randint(0, 1000)
                # password = sha256(cipher(password)).hexdigest() version with cryptoUtils
                password = f'password{random_num}'
                email = f'{user}@ciencias.unam.mx'
                
                # Insert user record
                cursor.execute(sql_usarios, (user, apPat, apMat, password, email, 0))
                print(f"User added: Name: {user}, Last Name: {apPat}, Second Last Name: {apMat}, Email: {email}")
                
                # Insert movie record
                random_num = random.randint(0, 1000)
                idPelicula = f'Movie{random_num}'
                cursor.execute(sql_peliculas, (idPelicula, 'Scarry', 210, 4))
                print(f"Movie added: Name: {idPelicula}")
                
                # Insert rent record
                cursor.execute(sql_rentar, (idUsuario, idPelicula, 3, 1))
                print(f"Rent added: User ID: {idUsuario}, Movie ID: {idPelicula}, Rent Date: CURRENT_TIMESTAMP, Rent Days: 3, Status: 1")
            
            # Commit transaction
            connection.commit()  
    finally:
        connection.close()

'''
Function to filter users by last name ending
'''
def filter_last_name(ending):
    connection = connect_to_database()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM users WHERE apPat LIKE %s OR apMat LIKE %s"
            coincidence = f'%{ending}'
            cursor.execute(sql, (coincidence, coincidence))
            result = cursor.fetchall()
            if not result: 
                print("No users found with last name ending in '{}'".format(ending))
            else:
                filtered_result = [(user['idUsuario'], user['nombre'], user['apPat'], user['apMat'], user['email']) for user in result]
                for user in filtered_result:
                    print("ID: {}, Name: {} {} {}, Email: {}".format(*user))
    finally:
        connection.close()

'''
Function to change the gender of a movie
'''
def change_movie_gender(movie, gender):
    connection = connect_to_database()
    try:
        with connection.cursor() as cursor:
            sql_change = "UPDATE movies SET gender = %s WHERE name = %s"
            rows_affected = cursor.execute(sql_change, (gender, movie))
            if rows_affected > 0:
                connection.commit()
                print("Gender changed successfully!")
            else:
                print("Movie not found!")
    finally:
        connection.close()

'''
Function to delete old rentals
'''
def delete_old_rentals():
    connection = connect_to_database()
    try:
        with connection.cursor() as cursor:
            sql_delete_rentals = """
                            DELETE FROM rentar
                            WHERE fecha_renta < DATE_SUB(NOW(), INTERVAL 4 DAY)
                        """
            deleted = cursor.execute(sql_delete_rentals)
            connection.commit()  
            print(f"Rentals deleted: {deleted}")
    finally:
        connection.close()

'''
Function to execute the functions lol
'''
def execute_functions():
    print("PyMySql Functions | First Exercise")
    # Insert records
    insert_records()

    # Prompt user for last name ending
    ending = input("Enter the ending of the last name to search: ")

    # Filter users by last name
    filter_last_name(ending)

    # Prompt user for movie name and new genre
    movie_example = input("Enter the name of the movie to change: ")
    gender_example = input("Enter the new genre of the movie: ")
    # Change movie genre
    change_movie_gender(movie_example, gender_example)

    # Delete old rentals
    delete_old_rentals()

    print("Functions executed successfully!")

# Execute functions
execute_functions()