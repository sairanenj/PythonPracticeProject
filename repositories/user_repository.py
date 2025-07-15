from models import User, db

def find_user_by_username(username): # Hae käyttäjä käyttäjänimen perusteella
    return User.query.filter_by(username=username).first()

def create_user(username, password_hash): # Luo uusi käyttäjä
    user = User(username=username, password_hash=password_hash)
    db.session.add(user)
    db.session.commit()
    return user