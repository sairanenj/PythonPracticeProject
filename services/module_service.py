from repositories.module_repository import (
    get_modules_for_user,
    get_module_by_id,
    create_module,
    update_module,
    delete_module,
    get_fields_for_module,
    add_field_to_module,
    delete_field,
    create_custom_module_for_user,
    delete_module_and_related
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

# Poistetaan kustomoitu käyttäjän moduuli
def remove_custom_module(module_id):
    delete_module_and_related(module_id)

# Palauta moduulin kentät oikeassa järjestyksessä
def list_fields_for_module(module_id):
    return get_fields_for_module(module_id)

# Lisää kenttä moduuliin
def add_field(module_id, name, field_type, order_index, formula=None):
    return add_field_to_module(module_id, name, field_type, order_index, formula)

# Poista kenttä moduulista
def remove_field(field_id):
    delete_field(field_id)

# Luo uusi mukautettava moduuli käyttäjälle
def create_user_custom_module(user_id, name="Uusi avustin"): 
    module = create_custom_module_for_user(user_id, name)
    # Lisää tarvittavat kentät automaattisesti
    add_field_to_module(module.id, "Muistiinpano", "text", 1)
    add_field_to_module(module.id, "Lasku", "text", 2)
    add_field_to_module(module.id, "Tulos", "number", 3)
    add_field_to_module(module.id, "Selite", "text", 4)
    add_field_to_module(module.id, "Aika", "number", 5)
    return module
