from repositories.module_repository import (
    get_modules_for_user,
    get_module_by_id,
    create_module,
    update_module,
    delete_module,
    get_fields_for_module,
    add_field_to_module,
    delete_field,
)

# Palauta kaikki käyttäjän käytettävissä olevat moduulit
def list_modules_for_user(user_id):
    return get_modules_for_user(user_id)

# Palauta yksittäinen moduuli id:llä
def find_module(module_id):
    return get_module_by_id(module_id)

# Luo uusi moduuli käyttäjälle
def create_user_module(name, type, user_id):
    return create_module(name=name, type=type, user_id=user_id, is_public=False)

# Luo uusi julkinen moduuli (vain ylläpitäjälle tms.)
def create_public_module(name, type):
    return create_module(name=name, type=type, user_id=None, is_public=True)

# Päivitä moduulin tietoja
def edit_module(module_id, **kwargs):
    return update_module(module_id, **kwargs)

# Poista moduuli
def remove_module(module_id):
    delete_module(module_id)

# Palauta moduulin kentät oikeassa järjestyksessä
def list_fields_for_module(module_id):
    return get_fields_for_module(module_id)

# Lisää kenttä moduuliin
def add_field(module_id, name, field_type, order_index, formula=None):
    return add_field_to_module(module_id, name, field_type, order_index, formula)

# Poista kenttä moduulista
def remove_field(field_id):
    delete_field(field_id)