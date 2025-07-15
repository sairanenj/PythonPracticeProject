from repositories.user_repository import find_user_by_username, create_user
from werkzeug.security import generate_password_hash, check_password_hash

def register_user(username, password): # Rekisteröi uusi käyttäjä
    if find_user_by_username(username):
        return "Käyttäjätunnus on jo käytössä."
    password_hash = generate_password_hash(password) # Hashaa salasana rekisteröinnin yhteydessä
    create_user(username, password_hash)
    return "Rekisteröinti onnistui!"

def authenticate_user(username, password): # Authentikoi käyttäjä kirjautumisen yhteydessä
    user = find_user_by_username(username)
    if user and check_password_hash(user.password_hash, password): # Tarkista, että käyttäjä löytyy ja salasana täsmää
        return user
    return None