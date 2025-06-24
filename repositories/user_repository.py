from models import User, db

def find_user_by_username(username): # Fetch a user by username
    return User.query.filter_by(username=username).first()

def create_user(username, password_hash): # Create a new user in the database
    user = User(username=username, password_hash=password_hash)
    db.session.add(user)
    db.session.commit()
    return user