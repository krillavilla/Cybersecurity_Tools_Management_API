from flask import request, abort
from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt


def requires_auth(permission):
    """
    A decorator to enforce role-based access control (RBAC) on Flask routes.

    Args:
        permission (str): The required permission to access the route.

    Returns:
        function: The decorated function with RBAC enforced.
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if "permissions" not in claims or permission not in claims["permissions"]:
                abort(403, description="Permission not found.")
            return f(*args, **kwargs)
        return wrapper
    return decorator
