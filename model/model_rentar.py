from alchemyClasses.Rentar import Rentar
from alchemyClasses import db
from datetime import datetime

'''
Function to retrieve and display all rentals from the database
'''
def show_rentals():
    rentals = Rentar.query.all()
    for rental in rentals:
        print(rental)

'''
Function to filter rentals by their ID and display the result
'''
def filter_rental_by_id(id_rental):
    exists = Rentar.query.filter_by(idRentar = id_rental).exists().scalar()
    if exists:
        rental = Rentar.query.filter_by(idRentar = id_rental).first()
        print(rental)
    else:
        print("No rental exists with that id")

'''
Function to update the date of a rental based on its ID
'''
def update_date(id_rental, new_date):
    datetime = datetime.strptime(new_date, "%Y-%m-%d")
    updated_rows = Rentar.query.filter_by(idRentar = id_rental).update({"rent_date": datetime})
    db.session.commit()
    if updated_rows:
        print("Rental updated")
    else:
        print("No rental exists with that id")

'''
Function to delete a rental from the database by its ID.
'''
def delete_rental(id_rental):
    deleted_rows = Rentar.query.filter_by(idRentar = id_rental).delete()
    if deleted_rows:
        db.session.commit()
        print("Rental deleted")
    else:
        print("No rental exists with that id")

'''
Function to delete all rentals from the database.
'''
def delete_all():
    deleted_rows = Rentar.query.delete()
    db.session.commit()
    print(f"Rentals deleted: {deleted_rows}")
