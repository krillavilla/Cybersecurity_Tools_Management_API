import json
from flask import request, abort
from functools import wraps
from jose import jwt
import os
from urllib.request import urlopen


# Auth0 Configuration - Critical security settings
# These environment variables must be set for the application to function securely
AUTH0_DOMAIN = os.environ.get('AUTH0_DOMAIN')
if not AUTH0_DOMAIN:
    raise ValueError("No AUTH0_DOMAIN set. This is a required environment variable for authentication.")

ALGORITHMS = ['RS256']

# API audience is required for token validation
# Check both API_AUDIENCE and API_IDENTIFIER for backward compatibility
API_AUDIENCE = os.environ.get('API_AUDIENCE') or os.environ.get('API_IDENTIFIER')
if not API_AUDIENCE:
    raise ValueError("No API_AUDIENCE or API_IDENTIFIER set. One of these is required for authentication.")


class AuthError(Exception):
    """
    An exception class for authentication errors.
    """
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def get_token_auth_header():
    """
    Get the Authorization header from the request.

    Returns:
        str: The token part of the Authorization header.

    Raises:
        AuthError: If the Authorization header is missing or malformed.
    """
    auth = request.headers.get('Authorization', None)
    if not auth:
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected.'
        }, 401)

    parts = auth.split()
    if parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must start with "Bearer".'
        }, 401)

    elif len(parts) == 1:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Token not found.'
        }, 401)

    elif len(parts) > 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must be bearer token.'
        }, 401)

    token = parts[1]
    return token


def verify_decode_jwt(token):
    """
    Decode and verify the JWT using the Auth0 secret.

    Args:
        token (str): The JWT token.

    Returns:
        dict: The decoded payload.

    Raises:
        AuthError: If the token is invalid, expired, or malformed.
    """
    try:
        # First try to parse the token header
        try:
            unverified_header = jwt.get_unverified_header(token)
        except jwt.JWTError:
            raise AuthError({
                'code': 'invalid_token',
                'description': 'Token is malformed or invalid.'
            }, 400)
        except Exception as e:
            raise AuthError({
                'code': 'invalid_header',
                'description': f'Unable to parse authentication token: {str(e)}'
            }, 400)

        # Then fetch the JWKS
        jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
        jwks = json.loads(jsonurl.read())
        rsa_key = {}
    except Exception as e:
        raise AuthError({
            'code': 'invalid_header',
            'description': f'Unable to fetch authentication keys: {str(e)}'
        }, 400)

    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }

    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer=f'https://{AUTH0_DOMAIN}/'
            )
            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError as e:
            raise AuthError({
                'code': 'invalid_claims',
                'description': f'Incorrect claims. Please, check the audience and issuer. Error: {str(e)}'
            }, 401)

        except Exception as e:
            raise AuthError({
                'code': 'invalid_header',
                'description': f'Unable to parse authentication token. Error: {str(e)}'
            }, 400)

    # If we get here, it means no matching key was found in the JWKS
    raise AuthError({
        'code': 'invalid_header',
        'description': f'Unable to find the appropriate key. Verify that the token was issued by the correct Auth0 tenant and that the key has not been rotated. Token kid: {unverified_header.get("kid", "Not found")}'
    }, 400)


def check_permissions(permission, payload):
    """
    Check if the required permission is in the JWT payload.

    Args:
        permission (str): The required permission.
        payload (dict): The decoded JWT payload.

    Returns:
        bool: True if the permission is in the payload.

    Raises:
        AuthError: If the permissions are not included in the payload or the required permission is not in the payload.
    """
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'Permissions not included in JWT. The token must include a permissions claim.'
        }, 400)

    if permission not in payload['permissions']:
        available_permissions = ', '.join(payload['permissions'])
        raise AuthError({
            'code': 'unauthorized',
            'description': f'Permission "{permission}" not found. Available permissions: {available_permissions}'
        }, 403)

    return True


def requires_auth(permission=''):
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
            try:
                token = get_token_auth_header()
                payload = verify_decode_jwt(token)
                check_permissions(permission, payload)
                return f(*args, **kwargs)
            except AuthError as e:
                # Add more context to the error message
                error_description = e.error['description']
                if e.status_code == 400:
                    error_description += " Please check that your token is valid and properly formatted."
                elif e.status_code == 401:
                    error_description += " Please check that your token is not expired and has the correct issuer and audience."
                elif e.status_code == 403:
                    error_description += " Please check that your token has the required permissions."

                abort(e.status_code, description=error_description)
        return wrapper
    return decorator
