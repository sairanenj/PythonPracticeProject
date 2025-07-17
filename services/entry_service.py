from repositories.entry_repository import (
    create_entry,
    get_entries_for_module_and_user,
    get_entry_by_id,
    get_entry_values,
    update_entry_values,
    delete_entry,
    get_name_field_for_category,
    get_exercise_names_for_field,
    create_gym_entry,
    get_gym_program_entries,
    add_note_entry,
    add_calculation_entry,
    add_timer_entry
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

def list_gym_exercises_by_category(gym_module_id, categories, user_id):
    exercises_by_category = {}
    for category in categories:
        name_field = get_name_field_for_category(gym_module_id, category)
        if not name_field:
            exercises_by_category[category] = []
            continue
        # Hae vain user_id:lle kuuluvat liikkeet
        exercises_by_category[category] = get_exercise_names_for_field(name_field.id, user_id)
    return exercises_by_category

def add_gym_exercise_to_program(module_id, user_id, exercise_name, category, weight, sets, reps, info):
    return create_gym_entry(module_id, user_id, exercise_name, category, weight, sets, reps, info)

def list_gym_program_entries(module_id, user_id):
    return get_gym_program_entries(module_id, user_id)

# Kustomoitu moduuli

def add_note(module_id, user_id, note_field_id, note_text):
    return add_note_entry(module_id, user_id, note_field_id, note_text)

def add_calculation(module_id, user_id, calc_field_id, result_field_id, desc_field_id, calculation, result, description):
    return add_calculation_entry(module_id, user_id, calc_field_id, result_field_id, desc_field_id, calculation, result, description)

def add_timer(module_id, user_id, timer_field_id, desc_field_id, timer_value, description):
    return add_timer_entry(module_id, user_id, timer_field_id, desc_field_id, timer_value, description)