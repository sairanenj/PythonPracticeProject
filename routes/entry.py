from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from services.entry_service import (
    add_entry,
    list_entries,
    get_entry,
    get_values,
    edit_entry,
    remove_entry,
    list_gym_exercises_by_category,
    add_gym_exercise_to_program,
    list_gym_program_entries
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

# RUOKAILUREITIT

@entry_bp.route("/eating2", methods=["GET", "POST"])
#@login_required
def eating_view():
    module_id = 1  # ruokailumoduulin id
    user_id = session.get("user_id") # dynaaminen käyttäjän id

    if not user_id: # Tarkista onko käyttäjä kirjautunut
        flash("Kirjaudu ensin sisään nähdäksesi merkinnät.")
        return redirect(url_for("auth.login"))
    
    if request.method == "POST":
        # Oletetaan, että lomakkeessa on kentät: field_id[] ja value[]
        field_value_dict = {} # Sanakirja joka yhdistää kentän id:n ja sen valuen
        for field_id, value in zip(request.form.getlist("field_id"), request.form.getlist("value")): # Kentät ovat listoja, joten yhdistetään ne sanakirjaan
            field_value_dict[int(field_id)] = value # Lisätään kentän id ja sen arvo sanakirjaan
        add_entry(module_id, user_id, field_value_dict) # Lisää merkintä tietokantaan
        flash("Ruoka-aine lisätty!")
        return redirect(url_for("entry.eating_view")) # Uudelleenohjaa syömisnäkymään, jotta näytetään lisätty merkintä
    
    # Hae moduuli ja kentät
    module = find_module(module_id)
    if not module:
        return render_template("module_not_found.html"), 404
    fields = list_fields_for_module(module_id)

    # Hae entryt ja niiden valuet
    entries = list_entries(module_id, user_id)
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

@entry_bp.route("/eating1", methods=["GET", "POST"])
def eating1_view():
    user_id = session.get("user_id")
    if not user_id:
        flash("Kirjaudu ensin sisään.")
        return redirect(url_for("auth.login"))

    # Hae kaikki käyttäjän ruoka-aineet alasvetovalikkoon (module_id=1)
    food_entries = list_entries(1, user_id)
    foods = []
    for entry in food_entries:
        values = {v.field_id: v.value for v in get_values(entry.id)}
        food_name = values.get(1, "Tuntematon") # oletetaan kenttä 1 = nimi
        foods.append({"id": entry.id, "name": food_name, "macros": values}) # lisätään ruoka-aineen id, nimi ja makrot (arvot) listaan

    # Lisää päivän ruokailu vain sessioniin
    if request.method == "POST":
        food_entry_id = int(request.form["food_entry_id"])
        amount = float(request.form["amount"])
        # Hae nykyinen päivän ruokailu sessionista tai luo uusi lista
        day_meals = session.get("day_meals", [])
        day_meals.append({"food_entry_id": food_entry_id, "amount": amount})
        session["day_meals"] = day_meals
        flash("Ruoka-aine lisätty päivän ruokailuun!")
        return redirect(url_for("entry.eating1_view"))

    # Hae päivän ruokailut sessionista
    day_meals = session.get("day_meals", [])
    meal_rows = []
    for meal in day_meals:
        food = next((f for f in foods if f["id"] == meal["food_entry_id"]), None)
        if not food:
            continue
        amount = meal["amount"]
        macros = food["macros"]
        meal_rows.append({
            "name": food["name"],
            "amount": amount,
            "fat": float(macros.get(2, 0)) * amount / 100,
            "protein": float(macros.get(3, 0)) * amount / 100,
            "carb": float(macros.get(4, 0)) * amount / 100,
            "energy": float(macros.get(5, 0)) * amount / 100,
        })

    total_amount = sum(meal["amount"] for meal in meal_rows)
    total_fat = sum(meal["fat"] for meal in meal_rows)
    total_protein = sum(meal["protein"] for meal in meal_rows)
    total_carb = sum(meal["carb"] for meal in meal_rows)
    total_energy = sum(meal["energy"] for meal in meal_rows)

    return render_template(
        "eating1.html",
        foods=foods,
        meal_rows=meal_rows,
        total_amount=total_amount,
        total_fat=total_fat,
        total_protein=total_protein,
        total_carb=total_carb,
        total_energy=total_energy
    )

@entry_bp.route("/clear_day_meals")
def clear_day_meals():
    session.pop("day_meals", None) # Poistaa päivän ruokailut sessionista
    flash("Päivän ruokailu tyhjennetty.")
    return redirect(url_for("eating1"))

# KUNTOSALIREITIT

@entry_bp.route("/gym", methods=["GET"])
def gym_view():
    gym_module = find_module(2)
    if not gym_module:
        return "Gym module not found", 404

    categories = ["chest", "back", "legs", "shoulders", "arms"]
    # Oikean laidan liikkeet haetaan user_id=999
    exercises_by_category = list_gym_exercises_by_category(gym_module.id, categories, user_id=999)
    # Vasemman laidan ohjelma haetaan kirjautuneelle käyttäjälle
    user_id = session.get("user_id", 1)
    gym_program = list_gym_program_entries(gym_module.id, user_id)

    return render_template(
        "gym.html",
        exercises_by_category=exercises_by_category,
        gym_program=gym_program
    )

@entry_bp.route("/add_gym_exercise", methods=["POST"])
def add_gym_exercise():
    exercise_name = request.form.get("exercise_name")
    category = request.form.get("category")
    weight = request.form.get("weight", 0)
    sets = request.form.get("sets", 0)
    reps = request.form.get("reps", 0)
    info = request.form.get("info", "empty")
    user_id = session.get("user_id", 1)  # Oletetaan käyttäjä 1, jos ei kirjautumista

    gym_module = find_module(2)  # Gym-moduulin id on 2
    if not gym_module:
        flash("Gym module not found.")
        return redirect(url_for("entry.gym_view"))

    add_gym_exercise_to_program(
        module_id=gym_module.id,
        user_id=user_id,
        exercise_name=exercise_name,
        category=category,
        weight=weight,
        sets=sets,
        reps=reps,
        info=info
    )

    flash(f"Liike {exercise_name} ({category}) lisätty ohjelmaan!")
    return redirect(url_for("entry.gym_view"))
