from functools import wraps
from flask import request, jsonify
from werkzeug.exceptions import BadRequest
from pydantic import ValidationError
import json
from typing import List


def json_body_validator(body_model):
    def real_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not request.json:
                raise BadRequest(description="body require!")
            try:
                data = body_model(**request.json)
                kwargs['data'] = data
            except ValidationError as ex:
                return jsonify(json.loads(ex.json()))
            return func(*args, **kwargs)

        return wrapper

    return real_decorator


def login_headers_validator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


# def query_key_validator(q_list: List[str]):
#     def real_decorator(func):
#         @wraps(func)
#         def wrapper(*args, **kwargs):
#             not_exist = []
#             for item in q_list:
#                 if request.ur
#             if not request.json:
#                 raise BadRequest(description="body require!")
#             try:
#                 data = body_model(**request.json)
#                 kwargs['data'] = data
#             except ValidationError as ex:
#                 return jsonify(json.loads(ex.json()))
#             return func(*args, **kwargs)
#
#         return wrapper
#
#     return real_decorator
