from models import db, Module, Module_field, Entry, Entry_value

# Hae kaikki moduulit (valmiit ja käyttäjän omat)
def get_modules_for_user(user_id):
    return Module.query.filter(
        (Module.user_id == user_id) | (Module.user_id == None)
    ).all()

# Hae yksi moduuli id:llä
def get_module_by_id(module_id):
    return Module.query.get(module_id)

# Luo uusi moduuli
def create_module(name, type, user_id=None, is_public=False):
    module = Module(name=name, type=type, user_id=user_id, is_public=is_public)
    db.session.add(module)
    db.session.commit()
    return module

# Päivitä moduulin tietoja
def update_module(module_id, **kwargs):
    module = Module.query.get(module_id)
    for key, value in kwargs.items():
        setattr(module, key, value)
    db.session.commit()
    return module

# Poista moduuli
def delete_module(module_id):
    module = Module.query.get(module_id)
    if module:
        db.session.delete(module)
        db.session.commit()

# Poista moduuli ja siihen liittyvät entryt ja kentät
def delete_module_and_related(module_id):
    # Poista kaikki entryt ja entry_valuet
    entries = Entry.query.filter_by(module_id=module_id).all()
    for entry in entries:
        Entry_value.query.filter_by(entry_id=entry.id).delete()
        db.session.delete(entry)
    # Poista kaikki kentät
    Module_field.query.filter_by(module_id=module_id).delete()
    # Poista moduuli
    module = Module.query.get(module_id)
    if module:
        db.session.delete(module)
    db.session.commit()

# Hae moduulin kentät järjestyksessä
def get_fields_for_module(module_id):
    return Module_field.query.filter_by(module_id=module_id).order_by(Module_field.order_index).all()

# Lisää kenttä moduuliin
def add_field_to_module(module_id, name, field_type, order_index, formula=None):
    field = Module_field(
        module_id=module_id,
        name=name,
        field_type=field_type,
        order_index=order_index,
        formula=formula
    )
    db.session.add(field)
    db.session.commit()
    return field

# Poista kenttä moduulista
def delete_field(field_id):
    field = Module_field.query.get(field_id)
    if field:
        db.session.delete(field)
        db.session.commit()

def create_custom_module_for_user(user_id, name="Uusi avustin"): # Luo uusi käyttäjän kustomoitava moduuli
    module = Module(name=name, type="custom", user_id=user_id, is_public=False) # Luo uusi moduuli
    db.session.add(module)
    db.session.commit()
    return module