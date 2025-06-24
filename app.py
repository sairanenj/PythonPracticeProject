from flask import Flask, render_template
from models import db
from routes.auth import auth_bp # Import the authentication blueprint

app = Flask(__name__)
app.secret_key = "secretkey" # This should be a strong secret key in production
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:@localhost/jshealthprodb"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False # Disable track modifications to save resources
db.init_app(app) # Initialize the database with the Flask app

app.register_blueprint(auth_bp) # Register the authentication blueprint

@app.route("/") # Root route to redirect to the start page
def start():
    return render_template("start.html")

if __name__ == "__main__":
    with app.app_context(): # Create the database tables
        db.create_all() # Ensure the database tables are created
    app.run(debug=True)