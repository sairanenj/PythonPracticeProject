from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from services.entry_service import (
    add_entry,
    list_entries,
    get_entry,
    get_values,
    edit_entry,
    remove_entry,
)
from services.module_service import list_fields_for_module, find_module

entry_bp = Blueprint("entry", __name__)

# Kirjautumisen tarkistava koristetoiminto
def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("auth.kirjaudu"))
        return f(*args, **kwargs)
    return decorated_function

@entry_bp.route("/<int:module_id>", methods=["GET"])
#@login_required
def module_entries(module_id):
    module_id = 1  # Oletetaan, että ruokailumoduulin id on 1
    entries = list_entries(1, 1)
    print(f"Entries: {entries}") #DEBUG
    fields = list_fields_for_module(module_id)
    # Haetaan jokaiselle entrylle sen arvot (field_id -> value)
    entries_with_values = []
    for entry in entries:
        values = {v.field_id: v.value for v in get_values(entry.id)}
        print(f"Entry {entry.id} values: {values}") #DEBUG
        entries_with_values.append({"entry": entry, "values": values})
    return render_template(
        "eating2.html",
        entries=entries_with_values,
        fields=fields,
        module_id=module_id
    )

@entry_bp.route("/eating2", methods=["GET"])
#@login_required
def eating_view():
    module_id = 1  # ruokailumoduulin id
    user_id = 1    # voit muuttaa dynaamiseksi myöhemmin

    # Hae moduuli ja kentät
    module = find_module(module_id)
    if not module:
        return render_template("module_not_found.html"), 404
    fields = list_fields_for_module(module_id)

    # Hae entryt ja niiden valuet
    entries = list_entries(user_id, module_id)
    entries_with_values = []
    for entry in entries:
        values = {v.field_id: v.value for v in get_values(entry.id)}
        print(f"Entry {entry.id} values: {values}")  # Debug-tulostus
        entries_with_values.append({"entry": entry, "values_dict": values})

    print(f"Kaikki entries_with_values: {entries_with_values}")  # Debug-tulostus
    return render_template(
        "eating2.html",
        module=module,
        fields=fields,
        entries=entries_with_values,
        module_id=module_id
    )

@entry_bp.route("/entry/<int:entry_id>/values", methods=["GET"])
def entry_values(entry_id):
    values = get_values(entry_id)
    print(f"Entry {entry_id} values: {[v.value for v in values]}")
    return render_template("eating.html", values=values)