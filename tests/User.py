import unittest
from classes.User import UserActions
from models.User import *
from classes.CustomErrors import *
from classes.Authentication import Authentication
from classes.ChatActions import ChatActions
from logging import info
import os

sample_user = {
    "username": 'temp_user',
    "password": 'temp_password'
}


def make_orderer():
    order = {}

    def ordered(f):
        order[f.__name__] = len(order)
        return f

    def compare(a, b):
        return [1, -1][order[a] < order[b]]

    return ordered, compare


ordered, compare = make_orderer()
unittest.defaultTestLoader.sortTestMethodsUsing = compare


class UserTest(unittest.TestCase):
    token: str = ''

    @ordered
    def test_login_without_signup(self):
        self.assertRaises(Forbidden, UserActions.login, LoginUserBodyModel(**sample_user))

    @ordered
    def test_signup(self):
        result = UserActions.signup(SignUpUserBodyModel(**sample_user))
        self.assertIsInstance(result, SignUpResponseModel)
        self.assertIsInstance(result.Authorization, str)

    @ordered
    def test_signup_with_same_data(self):
        self.assertRaises(ItemAlreadyExist, UserActions.signup, SignUpUserBodyModel(**sample_user))

    @ordered
    def test_login_after_signup(self):
        result = UserActions.login(
            LoginUserBodyModel(username=sample_user["username"], password=sample_user["password"]))
        self.assertIsInstance(result, LoginResponseModel)
        self.assertIsInstance(result.Authorization, str)

    @ordered
    def test_login_with_wrong_password(self):
        sample_user_temp = sample_user
        sample_user_temp['password'] = 'wrong'
        self.assertRaises(Forbidden, UserActions.login, LoginUserBodyModel(**sample_user_temp))

    @ordered
    def test_get_user_chats(self):
        data = ChatActions.get_user_un_saw_messages(sample_user["username"])
        self.assertIsInstance(data, dict)

    @ordered
    def test_get_user_chat_history(self):
        data = ChatActions.get_messages_with_other_user(sample_user["username"], 'aminjamal')
        self.assertIsInstance(data, dict)

    @ordered
    def test_remove_db(self):
        os.remove('chat.db')
