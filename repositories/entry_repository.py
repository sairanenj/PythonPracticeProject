from models import db, Entry, Entry_value

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