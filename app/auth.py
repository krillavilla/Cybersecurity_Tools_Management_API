from functools import wraps
from flask_jwt_extended import decode_token, get_jwt, jwt_required
from flask import request, jsonify
import requests
import json
import os

AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
API_IDENTIFIER = os.getenv('API_IDENTIFIER')


def requires_auth(permission=''):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = request.headers.get('Authorization', None)
            if not token:
                return jsonify({"msg": "Authorization token is missing"}), 401

            try:
                # Token verification via Auth0
                url = f'https://{AUTH0_DOMAIN}/.well-known/jwks.json'
                response = requests.get(url)
                jwks = response.json()
                unverified_header = decode_token(token, verify=False)
                rsa_key = {}
                if 'kid' in unverified_header:
                    for key in jwks['keys']:
                        if key['kid'] == unverified_header['kid']:
                            rsa_key = {
                                'kty': key['kty'],
                                'kid': key['kid'],
                                'use': key['use'],
                                'n': key['n'],
                                'e': key['e']
                            }
                if not rsa_key:
                    raise Exception('Unable to find appropriate key')

                payload = decode_token(token, rsa_key, algorithms=['RS256'], audience=API_IDENTIFIER,
                                       issuer=f'https://{AUTH0_DOMAIN}/')
                if permission and permission not in payload.get('permissions', []):
                    return jsonify({"msg": "You do not have permission to perform this action"}), 403

            except Exception as e:
                return jsonify({"msg": str(e)}), 401

            return f(*args, **kwargs)

        return wrapper

    return decorator