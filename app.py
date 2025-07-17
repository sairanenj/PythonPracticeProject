from flask import Flask, render_template, session
from models import db
from routes.auth import auth_bp
from routes.module import module_bp
from routes.entry import entry_bp
from services.module_service import list_modules_for_user
from seed import default_user, default_modules, default_module_fields, default_entries, default_gym_module_and_fields, default_gym_entries, default_values_user, default_cardio_module, default_cardio_module_fields

app = Flask(__name__)
app.secret_key = "secretkey" # Tärkeä salainen avain istuntojen hallintaan
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:@localhost/jshealthprodb"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False # SQLAlchemyn muutosten seuranta pois päältä
db.init_app(app) # Alusta SQLAlchemy tietokantayhteys

app.register_blueprint(auth_bp) # Rekisteröi autentikointiblueprint
app.register_blueprint(module_bp) # Rekisteröi moduuliblueprint
app.register_blueprint(entry_bp) # Rekisteröi entry-blueprint

@app.route("/") # Root-reitti, ohjaa aloitussivulle
def start():
    return render_template("start.html")

# @app.route("/cardio") # VÄLIAIKAINEN TESTAAMISEEN
# def cardio():
#     return render_template("cardio.html")

@app.context_processor
def inject_user_modules():
    user_id = session.get("user_id")
    if user_id:
        # Hae kaikki käyttäjän ja julkiset moduulit
        all_modules = list_modules_for_user(user_id)
        # Suodata vain käyttäjän omat (user_id ei ole NULL/none)
        user_modules = [m for m in all_modules if m.user_id == user_id]
    else:
        user_modules = []
    return dict(user_modules=user_modules)

if __name__ == "__main__":
    with app.app_context(): # Varmista, että sovelluskonteksti on käytössä
        db.create_all() # Luo luo kaikki tietokantamallit
        default_user()
        default_values_user()
        default_modules()
        default_module_fields()
        default_gym_module_and_fields()
        default_cardio_module()
        default_cardio_module_fields()
        default_entries()
        default_gym_entries()
    app.run(debug=True)