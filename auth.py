import jwt
from functools import wraps
from flask import request, abort
import os

def requires_auth(permission):
    def wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            auth_header = request.headers.get('Authorization', None)
            if not auth_header:
                abort(401)

            try:
                token = auth_header.split()[1]
                secret_key = os.getenv('JWT_SECRET_KEY', 'your-jwt-secret')  # Fetch secret from environment variables
                payload = jwt.decode(token, secret_key, algorithms=["HS256"])
                if permission not in payload['permissions']:
                    abort(403)
            except Exception:
                abort(401)

            return f(*args, **kwargs)

        return decorated_function

    return wrapper
