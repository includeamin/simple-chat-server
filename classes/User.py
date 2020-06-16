from models.User import *
from database.DB import session, User as UserDB
from hashlib import md5
from classes.Authentication import Authentication
from classes.CustomErrors import ItemAlreadyExist, Forbidden


class UserActions:

    @staticmethod
    def is_user_exist(name, should_exist: bool = False):
        data = session.query(UserDB).filter(UserDB.name == name).all()
        if should_exist:
            if not data:
                raise Forbidden(description="wrong password or username")
        else:
            if data:
                raise ItemAlreadyExist(description='user already exist')

    @staticmethod
    def password_to_hash(password: str):
        hashed_password = md5(password.encode('utf-8')).hexdigest()
        return hashed_password

    @staticmethod
    def signup(body: SignUpUserBodyModel) -> SignUpResponseModel:
        hashed_password = UserActions.password_to_hash(body.password)
        user = UserDB(name=body.username, password=hashed_password)
        UserActions.is_user_exist(user.name)
        session.add(user)
        token = Authentication.create_jwt(JwtPayloadModel(username=body.username))
        session.commit()
        return SignUpResponseModel(Authorization=token)

    @staticmethod
    def login(body: LoginUserBodyModel) -> LoginResponseModel:
        UserActions.is_user_exist(body.username, should_exist=True)
        hashed_password = UserActions.password_to_hash(body.password)
        user_in_db: UserDB = session.query(UserDB).filter(UserDB.name == body.username)[0]
        if user_in_db.password == hashed_password:
            return LoginResponseModel(
                Authorization=Authentication.create_jwt(JwtPayloadModel(username=body.username)))
        raise Forbidden(description="wrong password or username")
