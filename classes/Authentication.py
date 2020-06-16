import jwt
from models.User import JwtPayloadModel
from settings.GlobalSettings import settings
from werkzeug.exceptions import Forbidden


class Authentication:
    @staticmethod
    def create_jwt(data: JwtPayloadModel):
        return jwt.encode(payload=data.dict(), key=settings.JWT_KEY)

    @staticmethod
    def validate_jwt(jwt_token: str) -> str:
        decoded = jwt.decode(jwt_token, key=settings.JWT_KEY)
        token = JwtPayloadModel(**decoded)
        diff = token.ex - token.ca
        if diff.days > 7:
            raise Forbidden(description="expire")
        return token.username
