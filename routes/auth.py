from flask import Blueprint, render_template, request, redirect, url_for, session, flash, get_flashed_messages
from services.user_service import register_user, authenticate_user

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["GET", "POST"]) # GET näyttää rekisteröitymislomakkeen, POST käsittelee rekisteröinnin
def register():
    message = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        message = register_user(username, password)
    return render_template("register.html", message=message)

@auth_bp.route("/login", methods=["GET", "POST"]) # GET näyttää kirjautumislomakkeen, POST käsittelee kirjautumisen
def login():
    message = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = authenticate_user(username, password)
        if user:
            get_flashed_messages()
            session["user_id"] = user.id
            session["username"] = user.username
            return render_template("home.html") # TÄMÄ ON VÄLIAIKAINEN, OHJAA KOTISIVULLE TAI MUUALLE
        else:
            message = "Käyttäjätunnus tai salasana on väärin."
    return render_template("login.html", message=message)

@auth_bp.route("/logout", methods=["POST"]) # POST käsittelee uloskirjautumisen
def logout():
    session.clear()
    flash("Olet kirjautunut ulos.")
    return redirect(url_for("start"))