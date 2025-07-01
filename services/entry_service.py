from repositories.entry_repository import (
    create_entry,
    get_entries_for_module_and_user,
    get_entry_by_id,
    get_entry_values,
    update_entry_values,
    delete_entry,
)

# Lisää uusi merkintä moduuliin
def add_entry(module_id, user_id, field_value_dict):
    return create_entry(module_id, user_id, field_value_dict)

# Listaa kaikki käyttäjän merkinnät moduulissa
def list_entries(module_id, user_id):
    return get_entries_for_module_and_user(module_id, user_id)

# Hae yksittäinen merkintä id:llä
def get_entry(entry_id):
    return get_entry_by_id(entry_id)

# Hae kaikki arvot yhdelle merkinnälle
def get_values(entry_id):
    return get_entry_values(entry_id)

# Päivitä merkinnän arvot
def edit_entry(entry_id, field_value_dict):
    update_entry_values(entry_id, field_value_dict)

# Poista merkintä
def remove_entry(entry_id):
    delete_entry(entry_id)