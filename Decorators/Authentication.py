from functools import wraps
from flask_socketio import disconnect, ConnectionRefusedError
from flask import request
from classes.Authentication import Authentication
from werkzeug.exceptions import Forbidden, Unauthorized
import json


def is_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # data = Authentication.validate_jwt(args)
        # validate access
        if len(args) > 0:
            if "token" not in args[0]:
                raise ConnectionRefusedError("authentication failed")
            try:
                print(args[0])
                user_name = Authentication.validate_jwt(json.loads(args[0])["token"])
                kwargs.update({"username": user_name})
            except Exception as ex:
                raise ConnectionRefusedError("authentication failed")

        else:
            raise ConnectionRefusedError("authentication failed")

        return f(*args, **kwargs)

    return decorated_function


def is_login_header(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            raise Unauthorized(description="Authentication failed")
        try:
            user_name = Authentication.validate_jwt(jwt_token=token)
            kwargs.update({"username": user_name})
        except:
            raise Unauthorized(description="Authentication failed")

        return f(*args, **kwargs)

    return decorated_function


def body_validator(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # validate access
        return f(*args, **kwargs)

    return decorated_function


def check_form_key(key_list: list):
    def real_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            #
            # if request.form is None:
            #     return Result(False, Error("FR"))
            #
            # not_exist_key = []
            # for key in key_list:
            #     if key in request.form:
            #         continue
            #     else:
            #         not_exist_key.append(key)
            #
            # if len(not_exist_key) > 0:
            #     return Result(False, "this keys not exist {0}".format(not_exist_key))
            return func(*args, **kwargs)

        return wrapper

    return real_decorator
