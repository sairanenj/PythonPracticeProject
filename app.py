from flask import Flask, render_template
from models import db, Module, Module_field, Entry, Entry_value
from routes.auth import auth_bp # Import the authentication blueprint
from routes.module import module_bp # Import the module blueprint
from routes.entry import entry_bp # Import the entry blueprint
from datetime import datetime, timezone

app = Flask(__name__)
app.secret_key = "secretkey" # This should be a strong secret key in production
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:@localhost/jshealthprodb"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False # Disable track modifications to save resources
db.init_app(app) # Initialize the database with the Flask app

app.register_blueprint(auth_bp) # Register the authentication blueprint
app.register_blueprint(module_bp) # Register the module blueprint
app.register_blueprint(entry_bp) # Register the entry blueprint

@app.route("/") # Root route to redirect to the start page
def start():
    return render_template("start.html")

@app.route("/eating1") # VÄLIAIKAINEN TESTAAMISEEN
def eating1():
    return render_template("eating1.html")

def default_modules():
    existing = Module.query.filter_by(name="ruokailu").first()
    if not existing:
        module = Module(
            user_id=None,
            name="ruokailu",
            type="yleinen",
            is_public=True
        )
        db.session.add(module)
        db.session.commit()

def default_module_fields():
    module_id = 1  # ruokailu-moduulin id
    fields = [
        {"name": "Ruoka-aine", "field_type": "text", "formula": None, "order_index": 1},
        {"name": "Rasva", "field_type": "number", "formula": None, "order_index": 2},
        {"name": "Proteiini", "field_type": "number", "formula": None, "order_index": 3},
        {"name": "Hiilihydraatti", "field_type": "number", "formula": None, "order_index": 4},
        {"name": "Energia", "field_type": "number", "formula": None, "order_index": 5},
    ]
    for field in fields:
        exists = Module_field.query.filter_by(
            module_id=module_id,
            name=field["name"]
        ).first()
        if not exists:
            db.session.add(Module_field(
                module_id=module_id,
                name=field["name"],
                field_type=field["field_type"],
                formula=field["formula"],
                order_index=field["order_index"]
            ))
    db.session.commit()

def default_entries():
    # Tarkista onko vastaava Entry jo olemassa (esim. module_id=1, user_id=1)
    entry = Entry.query.filter_by(module_id=1, user_id=1).first()
    if not entry:
        entry = Entry(
            module_id=1,
            user_id=1
        )
        db.session.add(entry)
        db.session.commit()  # entry.id muodostuu

    # Tarkista onko Entry_value -rivit jo olemassa tälle entrylle
    existing_fields = {ev.field_id for ev in Entry_value.query.filter_by(entry_id=entry.id).all()}
    values = [
        (1, "Peruna (keitetty)"),
        (2, 0.1),
        (3, 1.9),
        (4, 15.5),
        (5, 75),
    ]
    for field_id, value in values:
        if field_id not in existing_fields:
            db.session.add(Entry_value(
                entry_id=entry.id,
                field_id=field_id,
                value=value
            ))
    db.session.commit()


if __name__ == "__main__":
    with app.app_context(): # Create the database tables
        db.create_all() # Ensure the database tables are created
        default_modules()
        default_module_fields()
        default_entries()
    app.run(debug=True)