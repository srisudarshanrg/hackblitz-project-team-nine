from flask_login import current_user
from flask import abort
from functools import wraps
from . import bcrypt, db, session
from flask_login import login_user

def hash_password(password):
    hashed = bcrypt.generate_password_hash(password).decode(encoding="utf-8")
    return hashed

def check_hash_password(hash_password: bytes, password: str) -> bool:
    return bcrypt.check_password_hash(hash_password, bytes(password, "utf-8"))

def roles_required(*roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated or current_user.get_role() not in roles:
                abort(401)
            return func(*args, **kwargs)
        return wrapper
    return decorator