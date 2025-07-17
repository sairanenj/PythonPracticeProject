from flask import Blueprint, render_template, redirect, request, session, url_for, flash
from services.module_service import create_user_custom_module, remove_custom_module, edit_module

module_bp = Blueprint("module", __name__)

# Kirjautumisen tarkistava koristetoiminto
def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated_function

@module_bp.route("/create_custom_module", methods=["POST"])
@login_required
def create_custom_module_route():
    user_id = session["user_id"]
    # Voit halutessasi ottaa nimen lomakkeelta, tässä oletusnimi
    module = create_user_custom_module(user_id)
    flash("Uusi kustomoitu moduuli luotu!")
    return redirect(url_for("entry.custom_module_view", module_id=module.id))

# Poista kustomoitu moduuli
@module_bp.route("/delete_custom_module/<int:module_id>", methods=["POST"])
@login_required
def delete_custom_module_route(module_id):
    remove_custom_module(module_id)
    flash("Moduuli poistettu!")
    return redirect(url_for("start"))

@module_bp.route("/rename_custom_module/<int:module_id>", methods=["POST"])
@login_required
def rename_custom_module_route(module_id):
    new_name = request.form.get("new_name")
    edit_module(module_id, name=new_name)
    flash("Moduulin nimi päivitetty!")
    return redirect(url_for("entry.custom_module_view", module_id=module_id))