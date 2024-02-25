from alchemyClasses.Usuarios import Usuarios
from alchemyClasses import db
from alchemyClasses.Rentar import Rentar

'''
Function to retrieve and display all users from the database
'''
def show_users():
    users = Usuarios.query.all()
    for user in users:
        print(user)

'''
Function to filter users by their ID and display the result
'''
def filter_user_by_id(id_user):
    user = Usuarios.query.get(id_user)
    if user:
        print(user)
    else:
        print("No user with that id")

'''
Function to update the name of a user based on its ID
'''
def update_name(id_user, new_name):
    user = Usuarios.query.get(id_user)
    if user:
        user.name = new_name
        db.session.commit()
        print("User updated")
    else:
        print("No user exists with that id")

'''
Function to delete a user from the database by its ID.
'''
def delete_user(id_user):
    user = Usuarios.query.filter_by(idUsuario = id_user).first()
    if user:
        rents = Rentar.query.filter_by(idUsuario = user.idUsuario).all()
        if rents:
            print("User with associated rents, it can't be delete it")
            return
        else:
            db.session.delete(user)
            db.session.commit()
            print("User deleted")
    else:
        print("No user exists with that id")

'''
Function to delete a user from the database by its ID.
'''
def delete_all():
    users_with_rents = db.session.query(Usuarios).join(Rentar).count()
    deleted_users = Usuarios.query.delete()
    skipped_users = deleted_users - users_with_rents
    db.session.commit()
    if skipped_users > 0:
        print(f"Users deleted: {skipped_users}. Skipped due to having associated rents")
    else:
        print("Users deleted")
