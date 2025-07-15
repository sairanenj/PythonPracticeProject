from models import db, Entry, Entry_value, Module_field

# Luo uusi merkintä (entry) ja siihen liittyvät arvot (entry_values)
def create_entry(module_id, user_id, field_value_dict):
    entry = Entry(module_id=module_id, user_id=user_id)
    db.session.add(entry)
    db.session.commit()  # Tarvitaan, jotta entry.id syntyy

    entry_values = []
    for field_id, value in field_value_dict.items():
        entry_value = Entry_value(entry_id=entry.id, field_id=field_id, value=str(value))
        db.session.add(entry_value)
        entry_values.append(entry_value)
    db.session.commit()
    return entry, entry_values

# Hae kaikki merkinnät moduulille ja käyttäjälle
def get_entries_for_module_and_user(module_id, user_id):
    return Entry.query.filter_by(module_id=module_id, user_id=user_id).order_by(Entry.created_at.desc()).all()

# Hae yksittäinen merkintä id:llä
def get_entry_by_id(entry_id):
    return Entry.query.get(entry_id)

# Hae kaikki arvot yhdelle merkinnälle
def get_entry_values(entry_id):
    return Entry_value.query.filter_by(entry_id=entry_id).all()

# Päivitä merkinnän arvoja
def update_entry_values(entry_id, field_value_dict):
    for field_id, value in field_value_dict.items():
        entry_value = Entry_value.query.filter_by(entry_id=entry_id, field_id=field_id).first()
        if entry_value:
            entry_value.value = str(value)
        else:
            # Jos arvoa ei ole, luodaan uusi
            new_value = Entry_value(entry_id=entry_id, field_id=field_id, value=str(value))
            db.session.add(new_value)
    db.session.commit()

# Poista merkintä ja siihen liittyvät arvot
def delete_entry(entry_id):
    Entry_value.query.filter_by(entry_id=entry_id).delete()
    Entry.query.filter_by(id=entry_id).delete()
    db.session.commit()

def get_name_field_for_category(module_id, category): # Haetaan kategorian nimi kentälle
    fields = Module_field.query.filter_by(module_id=module_id, category=category).all()
    return next((f for f in fields if f.name == "name"), None)

def get_exercise_names_for_field(field_id, user_id):
    from models import Entry_value, Entry
    # Hae vain ne Entry_value:t, joiden entry kuuluu user_id:lle
    values = (
        Entry_value.query
        .join(Entry)
        .filter(Entry_value.field_id == field_id, Entry.user_id == user_id)
        .all()
    )
    return [v.value for v in values]

def create_gym_entry(module_id, user_id, exercise_name, category, weight, sets, reps, info):
    # Luo uusi Entry
    entry = Entry(module_id=module_id, user_id=user_id)
    db.session.add(entry)
    db.session.commit()

    # Hae kentät tälle kategoriaryhmälle
    fields = Module_field.query.filter_by(module_id=module_id, category=category).all()
    fields_dict = {f.name: f for f in fields}

    # Luo Entry_value:t
    for fname, value in [
        ("name", exercise_name),
        ("weight", weight),
        ("sets", sets),
        ("reps", reps),
        ("info", info)
    ]:
        field = fields_dict.get(fname)
        if field:
            db.session.add(Entry_value(
                entry_id=entry.id,
                field_id=field.id,
                value=value
            ))
    db.session.commit()
    return entry

def get_gym_program_entries(module_id, user_id):
    entries = Entry.query.filter_by(module_id=module_id, user_id=user_id).all()
    result = []
    for entry in entries:
        values = Entry_value.query.filter_by(entry_id=entry.id).all()
        value_dict = {}
        for v in values:
            field = Module_field.query.get(v.field_id)
            value_dict[field.name] = v.value
            value_dict["category"] = field.category  # Tarvitaan otsikkoon
        result.append(value_dict)
    return result