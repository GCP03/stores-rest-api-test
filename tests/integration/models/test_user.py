from models.user import UserModel
from tests.base_test import BaseTest


class UserTest(BaseTest):
    def test_crud(self):
        with self.app_context():
            user = UserModel('test', 'abcd')

            # user not saved to db yet
            self.assertIsNone(UserModel.find_by_user_name('test'))
            self.assertIsNone(UserModel.find_by_user_id(1))

            user.save_to_db()

            # user now saved to db
            self.assertIsNotNone(UserModel.find_by_user_name('test'))
            self.assertIsNotNone(UserModel.find_by_user_id(1))

