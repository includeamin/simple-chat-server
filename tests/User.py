import unittest
from classes.User import UserActions
from models.User import *
from classes.CustomErrors import *
import os

sample_user = {
    "username": 'temp_user',
    "password": 'temp_password'
}


class UserTest(unittest.TestCase):
    def test_login_without_signup(self):
        self.assertRaises(Forbidden, UserActions.login, LoginUserBodyModel(**sample_user))

    def test_signup(self):
        result = UserActions.signup(SignUpUserBodyModel(**sample_user))
        self.assertIsInstance(result, SignUpResponseModel)
        self.assertIsInstance(result.Authorization, str)

    def test_signup_with_same_data(self):
        self.assertRaises(ItemAlreadyExist, UserActions.signup, SignUpUserBodyModel(**sample_user))

    def test_login_with_wrong_password(self):
        sample_user_temp = sample_user
        sample_user_temp['password'] = 'wrong'
        # result = UserActions.login(LoginUserBodyModel(**sample_user_temp))
        self.failUnlessRaises(Forbidden, UserActions.login, LoginUserBodyModel(**sample_user))

        pass

    def test_login_with_wrong_username(self):
        pass

    def test_login_after_signup(self):
        result = UserActions.login(LoginUserBodyModel(**sample_user))
        self.assertIsInstance(result, LoginResponseModel)
        self.assertIsInstance(result.Authorization, str)
    #
    # def test_remove_db(self):
    #     os.remove('chat.db')
