from repositories.user_repository import find_user_by_username, create_user
from werkzeug.security import generate_password_hash, check_password_hash

def register_user(username, password): # Register a new user
    if find_user_by_username(username):
        return "Käyttäjätunnus on jo käytössä."
    password_hash = generate_password_hash(password) # Hash the password for security
    create_user(username, password_hash)
    return "Rekisteröinti onnistui!"

def authenticate_user(username, password): # Authenticate a user with username and password
    user = find_user_by_username(username)
    if user and check_password_hash(user.password_hash, password): # Check if user & password matches
        return user
    return None