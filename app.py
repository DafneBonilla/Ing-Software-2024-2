from datetime import datetime
from flask import Flask
from alchemyClasses import db
from model import model_usuarios
from model import model_peliculas
from model import model_rentar
from alchemyClasses.Rentar import Rentar
from alchemyClasses.Usuarios import Usuarios
from alchemyClasses.Peliculas import Peliculas

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://lab:Developer123!@localhost:3306/lab_ing_software'
app.config.from_mapping(
    SECRET_KEY='dev'
)
db.init_app(app)

def print_menu():
    print("What would you like to do?")
    print("1. View records from a table")
    print("2. Filter records from a table by ID")
    print("3. Update a record's name (rental date for rentals)")
    print("4. Delete a record or all records")
    print("5. Quit")

def print_table_options():
    print("Which table records do you want to view?")
    print("1. Users")
    print("2. Movies")
    print("3. Rentals")
    print("4. Go back")

def print_filter_options():
    print("Which table do you want to filter records from?")
    print("1. Users")
    print("2. Movies")
    print("3. Rentals")
    print("4. Go back")

def print_update_options():
    print("Which table do you want to update a record from?")
    print("1. Users")
    print("2. Movies")
    print("3. Rentals")
    print("4. Go back")

def print_delete_options():
    print("Which table do you want to delete a record from?")
    print("1. Users")
    print("2. Movies")
    print("3. Rentals")
    print("4. Go back")

def print_delete_record_options():
    print("1. Delete a record")
    print("2. Delete all records")
    print("3. Go back")

def print_goodbye():
    print("Goodbye!")

if __name__ == '__main__':
    with app.app_context():
        ok = False
        while not ok:
            print_menu()
            option = input("Option: ")
            if option == "1":
                done = False
                while not done:
                    print_table_options()
                    table_option = input("Option: ")
                    if table_option == "1":
                        model_usuarios.show_users()
                    elif table_option == "2":
                        model_peliculas.show_movies()
                    elif table_option == "3":
                        model_rentar.show_rentals()
                    elif table_option == "4":
                        done = True
                    else:
                        print("Invalid option")
            elif option == "2":
                done = False
                while not done:
                    print_filter_options()
                    filter_option = input("Option: ")
                    if filter_option == "1":
                        complete = False
                        while not complete:
                            try:
                                id_num = int(input("Enter the ID of the user you want to filter: "))
                                model_usuarios.filter_user_by_id(id_num)
                                complete = True
                            except ValueError:
                                print("Enter an integer")
                    elif filter_option == "2":
                        complete = False
                        while not complete:
                            try:
                                id_num = int(input("Enter the ID of the movie you want to filter: "))
                                model_peliculas.filter_movie_by_id(id_num)
                                complete = True
                            except ValueError:
                                print("Enter an integer")
                    elif filter_option == "3":
                        complete = False
                        while not complete:
                            try:
                                id_num = int(input("Enter the ID of the rental you want to filter: "))
                                model_rentar.filter_rental_by_id(id_num)
                                complete = True
                            except ValueError:
                                print("Enter an integer")
                    elif filter_option == "4":
                        done = True
                    else:
                        print("Invalid option")
            elif option == "3":
                done = False
                while not done:
                    print_update_options()
                    update_option = input("Option: ")
                    if update_option == "1":
                        complete = False
                        while not complete:
                            try:
                                id_num = int(input("Enter the ID of the user you want to update: "))
                                new_name = input("Enter the new name: ")
                                model_usuarios.update_name(id_num, new_name)
                                complete = True
                            except ValueError:
                                print("Enter an integer")
                    elif update_option == "2":
                        complete = False
                        while not complete:
                            try:
                                id_num = int(input("Enter the ID of the movie you want to update: "))
                                new_name = input("Enter the new name: ")
                                model_peliculas.update_name(id_num, new_name)
                                complete = True
                            except ValueError:
                                print("Enter an integer")
                    elif update_option == "3":
                        complete = False
                        while not complete:
                            try:
                                id_num = int(input("Enter the ID of the rental you want to update: "))
                                new_date = input("Enter the new date (yyyy-mm-dd): ")
                                try:
                                    datetime.strptime(new_date, "%Y-%m-%d")
                                except ValueError:
                                    print("Invalid date format. Should be yyyy-mm-dd")
                                    continue
                                model_rentar.update_date(id_num, new_date)
                                complete = True
                            except ValueError:
                                print("Enter an integer")
                    elif update_option == "4":
                        done = True
                    else:
                        print("Invalid option")
            elif option == "4":
                done = False
                while not done:
                    print_delete_options()
                    delete_option = input("Option: ")
                    if delete_option == "1":
                        complete = False
                        while not complete:
                            print_delete_record_options()
                            record_option = input("Option: ")
                            if record_option == "1":
                                finished = False
                                while not finished:
                                    try:
                                        id_num = int(input("Enter the ID of the record you want to delete: "))
                                        model_usuarios.delete_user(id_num)
                                        finished = True
                                    except ValueError:
                                        print("Enter an integer")
                            elif record_option == "2":
                                model_usuarios.delete_all()
                                complete = True
                            elif record_option == "3":
                                complete = True
                            else:
                                print("Invalid option")
                    elif delete_option == "2":
                        complete = False
                        while not complete:
                            print_delete_record_options()
                            record_option = input("Option: ")
                            if record_option == "1":
                                finished = False
                                while not finished:
                                    try:
                                        id_num = int(input("Enter the ID of the record you want to delete: "))
                                        model_peliculas.delete_movie(id_num)
                                        finished = True
                                    except ValueError:
                                        print("Enter an integer")
                            elif record_option == "2":
                                model_peliculas.delete_all()
                                complete = True
                            elif record_option == "3":
                                complete = True
                            else:
                                print("Invalid option")
                    elif delete_option == "3":
                        complete = False
                        while not complete:
                            print_delete_record_options()
                            record_option = input("Option: ")
                            if record_option == "1":
                                finished = False
                                while not finished:
                                    try:
                                        id_num = int(input("Enter the ID of the record you want to delete: "))
                                        model_rentar.delete_rental(id_num)
                                        finished = True
                                    except ValueError:
                                        print("Enter an integer")
                            elif record_option == "2":
                                model_rentar.delete_all()
                                complete = True
                            elif record_option == "3":
                                complete = True
                            else:
                                print("Invalid option")
                    elif delete_option == "4":
                        done = True
                    else:
                        print("Invalid option")
            elif option == "5":
                ready = True
                print_goodbye()
            else:
                print("Invalid option")
