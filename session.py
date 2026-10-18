# session.py
_current_user = None

def set_current_user(user):
    global _current_user
    _current_user = user

def get_current_user():
    return _current_user

def get_current_role():
    return _current_user['rol'] if _current_user else None

def is_admin():
    return get_current_role() == 'admin'

def is_editor():
    return get_current_role() == 'editor'

def can_edit():
    return get_current_role() in ['admin', 'editor']

def logout():
    global _current_user
    _current_user = None