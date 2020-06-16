from werkzeug.exceptions import *


class ItemAlreadyExist(HTTPException):
    code = 400
    description = "item already exist"
