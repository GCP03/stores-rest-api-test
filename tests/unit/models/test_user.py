from models.user import UserModel
from tests.unit.unit_base_test import UnitBaseTest

class UserTest(UnitBaseTest):
    def test_create_user(self):
        user = UserModel('test_user', 'abcd')

        self.assertEqual(user.username, 'test_user', 'User name is incorrect')
        self.assertEqual(user.password, 'abcd', 'Password is incorrect')