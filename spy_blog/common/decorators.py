from functools import wraps
from flask import request
from common import pretty_result, http_code

from flask_jwt_extended import verify_jwt_in_request, get_jwt_claims

from models.blog import role_permission, Permission

def permission_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        roles = claims.get('roles', [])
        path = request.path.split('/')[-1]
        method = request.method
        for role in roles:
            for permission in role.get('permissions', []):
                if permission.get('path') == path and permission.get('method', '').upper() == method:
                    return f(*args, **kwargs)
        return pretty_result(http_code.AUTHORIZATION_ERROR)
    return wrapper


