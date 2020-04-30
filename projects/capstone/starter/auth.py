#https://jonsheffer.auth0.com/authorize?audience=capstone&response_type=token&client_id=PZ009ZG2EW8n5dipOGrduq1lEAo3PFJb&redirect_uri=http://localhost:5000
from flask import Flask, request, abort
import json
from functools import wraps
from jose import jwt
from urllib.request import urlopen
import json

app = Flask(__name__)

AUTH0_DOMAIN = 'jonsheffer.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'capstone'


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def get_token_auth_header():
    """Obtains the Access Token from the Authorization Header
    """
    print("wtf am i not getting here")
    auth = request.headers.get('Authorization', None)
    if not auth:
        abort(401)

    parts = auth.split()
    print("here again")
    if parts[0].lower() != 'bearer':
        abort(401)

    elif len(parts) == 1:
        abort(401)

    elif len(parts) > 2:
        abort(401)

    token = parts[1]
    #print(token)
    return token


def verify_decode_jwt(token):
    print("in veriflaksdjflkjasy")
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    #jsonurl = urlopen(f'https://jonsheffer.auth0.com/.well-known/jwks.json')
    print(jsonurl)
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    
    print("in verify2")
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
                issuer='https://' + AUTH0_DOMAIN + '/'
            )
            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
            }, 400)

def check_permissions(permission, payload):
    if 'permissions' not in payload:
        print("made it here")
        abort(400)
    if permission not in payload['permissions']:
        print(permission)
        print("made it here2")
        abort(403)
    print("made it here3")
    return True

def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            print("in wrapper")
            try:
                print("in try??222?")
                payload = verify_decode_jwt(token)
                print("after verify")
            except:
                abort(401)
            check_permissions(permission, payload)
            print("after permissions")
            if(kwargs.get('id')):
                return f(kwargs.get('id'))
            else:
                return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator
