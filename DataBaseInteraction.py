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
                                 database='lab_software_eng',
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
            user_id = cursor.fetchone()['idUsuario']
            cursor.execute("SELECT idPelicula FROM peliculas LIMIT 1")
            movie_id = cursor.fetchone()['idPelicula']
            
            # Loop for multiple inserts
            for _ in range(3):  # Inserting 3 records
                random_num = random.randint(0, 1000)
                user = f'User{random_num}'
                random_num = random.randint(0, 1000)
                firstLastName = f'FirstLastName{random_num}'
                random_num = random.randint(0, 1000)
                secondLastName = f'SecondLastName{random_num}'
                random_num = random.randint(0, 1000)
                # password = sha256(cipher(password)).hexdigest() version with cryptoUtils
                password = f'password{random_num}'
                email = f'{user}@ciencias.unam.mx'
                
                # Insert user record
                cursor.execute(sql_usarios, (user, firstLastName, secondLastName, password, email, 0))
                print(f"User added: Name: {user}, Last Name: {firstLastName}, Second Last Name: {secondLastName}, Email: {email}")
                
                # Insert movie record
                random_num = random.randint(0, 1000)
                movie_name = f'Movie{random_num}'
                cursor.execute(sql_peliculas, (movie_name, 'Scarry', 210, 4))
                print(f"Movie added: Name: {movie_name}")
                
                # Insert rent record
                cursor.execute(sql_rentar, (user_id, movie_id, 3, 1))
                print(f"Rent added: User ID: {user_id}, Movie ID: {movie_id}, Rent Date: CURRENT_TIMESTAMP, Rent Days: 3, Status: 1")
            
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
            pattern = f'%{ending}'
            cursor.execute(sql, (pattern, pattern))
            result = cursor.fetchall()
            # Print result
            if not result:
                print("No users found")
            else:
                # Extracting only necessary fields from the result set
                filtered_result = [(user['idUsuario'], user['nombre'], user['apPat'], user['apMat'], user['email']) for user in result]
                for user in filtered_result:
                    print("ID: {}, Name: {} {} {}, Email: {}".format(*user))
    finally:
        connection.close()



# Function to change genre of a certain movie
def change_movie_genre(movie, genre):
    connection = connect_to_database()
    try:
        with connection.cursor() as cursor:
            # Query
            sql_find_movie = "SELECT * FROM movies WHERE name = %s"
            cursor.execute(sql_find_movie, (movie,))
            movie_to_change = cursor.fetchone()
            # Changing genre
            if movie_to_change:
                sql_change_genre = "UPDATE movies SET genre = %s WHERE name = %s"
                cursor.execute(sql_change_genre, (genre, movie))
                connection.commit()
                print("Genre changed successfully!")
            else:
                print("Movie not found!")
    finally:
        connection.close()


# Function that deletes rentals from 3 days ago
def delete_old_rentals():
    connection = connect_to_database()
    try:
        with connection.cursor() as cursor:
            # Limit date and query
            sql_delete_rentals = """
                            DELETE FROM rent 
                            WHERE rent_date < DATE_SUB(NOW(), INTERVAL 4 DAY)
                        """
            cursor.execute(sql_delete_rentals)
            connection.commit()  # Confirm transaction
            deleted = cursor.rowcount
            print(f"Rentals deleted: {deleted}")
    finally:
        connection.close()


# Perform functions
print("PyMySql Functions")
insert_records()
last_name_end = input("Enter the ending of the last name to search: ")
filter_users_last_name(last_name_end)
movie_c = input("Enter the name of the movie to change: ")
genre_c = input("Enter the new genre of the movie: ")
change_movie_genre(movie_c, genre_c)
delete_old_rentals()
print("End of PyMySql functions")
