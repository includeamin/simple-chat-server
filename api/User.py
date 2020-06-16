from flask import Blueprint
from classes.User import UserActions
from models.User import SignUpUserBodyModel, LoginUserBodyModel
from Decorators.Validators import json_body_validator
from Decorators.Authentication import is_login_header
from classes.ChatActions import ChatActions

user_routes = Blueprint("user_routes", __name__)


@user_routes.route("/signup", methods=["POST"])
@json_body_validator(SignUpUserBodyModel)
def signup(**kwargs):
    return UserActions.signup(kwargs.get("data")).dict()


@user_routes.route("/login", methods=["POST"])
@json_body_validator(LoginUserBodyModel)
def login(**kwargs):
    return UserActions.login(kwargs.get('data')).dict()


@user_routes.route("/messages/unread")
@is_login_header
def get_user_new_messages(**kwargs):
    return ChatActions.get_user_un_saw_messages(kwargs.get('username'))


@user_routes.route("/messages/directs/<sender_username>")
@is_login_header
def get_direct_message_history(sender_username: str, **kwargs):
    return ChatActions.get_messages_with_other_user(kwargs.get('username'), sender_username)
