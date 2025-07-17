from models import db, Module, Module_field, Entry, Entry_value, User
from werkzeug.security import generate_password_hash

def default_user():
    user = User.query.filter_by(id=1).first()
    if not user:
        user = User(
            id=1,
            username="admin",
            password_hash=generate_password_hash("admin123")
        )
        db.session.add(user)
        db.session.commit()

def default_values_user():
    user = User.query.filter_by(id=999).first()
    if not user:
        user = User(
            id=999,
            username="999",
            password_hash=generate_password_hash("999")
        )
        db.session.add(user)
        db.session.commit()

# RUOKAILUMODUULI

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
    entry = Entry.query.filter_by(module_id=1, user_id=1).first()
    if not entry:
        entry = Entry(
            module_id=1,
            user_id=1
        )
        db.session.add(entry)
        db.session.commit()

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

# KUNTOSALIMODUULI 

def default_gym_module_and_fields():
    # Luo kuntosali-moduuli, jos sitä ei ole
    gym_module = Module.query.filter_by(name="gym").first()
    if not gym_module:
        gym_module = Module(
            user_id=None,
            name="gym",
            type="exercise",
            is_public=True
        )
        db.session.add(gym_module)
        db.session.commit()

    # Kategoriat englanniksi
    categories = ["chest", "back", "legs", "shoulders", "arms"]

    # Kentät englanniksi
    fields = [
        {"name": "name", "field_type": "text"},
        {"name": "weight", "field_type": "number"},
        {"name": "sets", "field_type": "number"},
        {"name": "reps", "field_type": "number"},
        {"name": "info", "field_type": "text"}
    ]

    order = 1
    for category in categories:
        for field in fields:
            exists = Module_field.query.filter_by(
                module_id=gym_module.id,
                name=field["name"],
                category=category
            ).first()
            if not exists:
                db.session.add(Module_field(
                    module_id=gym_module.id,
                    name=field["name"],
                    field_type=field["field_type"],
                    formula=None,
                    order_index=order,
                    category=category
                ))
            order += 1
    db.session.commit()

def default_gym_entries():
    # Hae gym-moduuli
    gym_module = Module.query.filter_by(name="gym").first()
    if not gym_module:
        return

    # Liikkeet kategorioittain
    default_exercises = {
        "chest": ["Penkkipunnerrus", "Vinopenkkipunnerrus", "Pec Deck"],
        "back": ["Maastaveto", "Kulmasoutu", "Leuanveto"],
        "legs": ["Kyykky", "Jalkaprässi", "Reidenkoukistus"],
        "shoulders": ["Pystypunnerrus", "Vipunostot sivulle", "Vipunostot eteen"],
        "arms": ["Hauiskääntö", "Scott", "Dippi"]
    }

    # Hae default-value-käyttäjä (id=999)
    user = User.query.filter_by(id=999).first()
    if not user:
        return

    for category, exercises in default_exercises.items():
        # Hae kentät tälle kategoriaryhmälle
        fields = Module_field.query.filter_by(module_id=gym_module.id, category=category).all()
        # Järjestä kentät nimen mukaan, jotta löydetään oikeat id:t
        fields_dict = {f.name: f for f in fields}

        for exercise_name in exercises:
            # Tarkista ettei sama entry ole jo olemassa
            entry = Entry.query.filter_by(module_id=gym_module.id, user_id=user.id).join(Entry_value).join(Module_field).filter(
                Entry_value.value == exercise_name,
                Module_field.name == "name",
                Module_field.category == category
            ).first()
            if entry:
                continue

            # Luo uusi entry
            entry = Entry(module_id=gym_module.id, user_id=user.id)
            db.session.add(entry)
            db.session.commit()

            # Lisää kenttäarvot
            for fname in ["name", "weight", "sets", "reps", "info"]:
                field = fields_dict.get(fname)
                if not field:
                    continue
                if fname == "name":
                    value = exercise_name
                elif fname == "info":
                    value = "empty"
                else:
                    value = 0
                db.session.add(Entry_value(
                    entry_id=entry.id,
                    field_id=field.id,
                    value=value
                ))
            db.session.commit()

# KARDIOMODUULI

def default_cardio_module():
    existing = Module.query.filter_by(name="kardio").first()
    if not existing:
        module = Module(
            user_id=None,
            name="kardio",
            type="yleinen",
            is_public=True
        )
        db.session.add(module)
        db.session.commit()

def default_cardio_module_fields():
    module_id = 3  # kardio-moduulin id
    fields = [
        {"name": "Laji", "field_type": "text", "formula": None, "order_index": 1},
        {"name": "Matka", "field_type": "number", "formula": None, "order_index": 2},
        {"name": "Aika", "field_type": "number", "formula": None, "order_index": 3},
        {"name": "Tiedot", "field_type": "text", "formula": None, "order_index": 4},
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