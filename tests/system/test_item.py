from models.store import StoreModel
from models.user import UserModel
from models.item import ItemModel
from tests.base_test import BaseTest
import json


class ItemTest(BaseTest):
    def setUp(self):
        super(ItemTest, self).setUp()
        with self.app() as client:
            with self.app_context():
                UserModel('test_user', 1234).save_to_db()
                auth_request = client.post('/auth',
                                           data=json.dumps({'username': 'test_user', 'password': '1234'}),
                                           headers={'Content-Type': 'application/json'})
                # our JWT token, need to include in authorization header
                auth_token = json.loads(auth_request.data)['access_token']
                # must be in this format
                #header = {'Authorization': 'JWT ' + auth_token}
                # or use format string
                self.access_token = f'JWT {auth_token}'


    def test_get_item_no_auth(self):
        with self.app() as client:
            with self.app_context():
                # don't include the JWT header so we have no auth (not logged in)
                resp = client.get('/item/test')
                self.assertEqual(resp.status_code, 401)


    def test_get_item_not_found(self):
        with self.app() as client:
            with self.app_context():
                resp = client.get('/item/test', headers={'Authorization': self.access_token})
                # we don't have a test item
                self.assertEqual(resp.status_code, 404)


    def test_get_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test_store').save_to_db()
                ItemModel('test_item', 19.99, 1).save_to_db()
                resp = client.get('/item/test_item', headers={'Authorization': self.access_token})
                self.assertEqual(resp.status_code, 200)


    def test_delete_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test_store').save_to_db()
                ItemModel('test_item', 19.99, 1).save_to_db()
                # auth not need for delete, only get
                resp = client.delete('/item/test_item')
                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual(json.loads(resp.data), {'message': 'Item deleted'})


    def test_create_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test_store').save_to_db()
                resp = client.post('/item/test_item', data={'price': 17.99, 'store_id': 1})
                self.assertEqual(resp.status_code, 201)
                self.assertDictEqual(json.loads(resp.data),
                                     {'name': 'test_item', 'price': 17.99})



    def test_create_duplicate_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test_store').save_to_db()
                ItemModel('test_item', 17.99, 1).save_to_db()
                # add dupe
                resp = client.post('/item/test_item', data={'price': 17.99, 'store_id': 1})
                self.assertEqual(resp.status_code, 400)
                self.assertDictEqual(json.loads(resp.data), {'message': "An item with name 'test_item' already exists."})


    def test_put_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test_store').save_to_db()
                resp = client.put('/item/test_item', data={'price': 17.99, 'store_id': 1})
                self.assertEqual(resp.status_code, 200)
                self.assertEqual(ItemModel.find_by_name('test_item').price, 17.99)
                self.assertDictEqual(json.loads(resp.data), {'name': 'test_item',
                                                             'price': 17.99})


    def test_put_update_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test_store').save_to_db()
                # add item with price of 17.99
                ItemModel('test_item', 17.99, 1).save_to_db()
                self.assertEqual(ItemModel.find_by_name('test_item').price, 17.99)
                # update price for item
                resp = client.put('/item/test_item', data={'price': 20.00, 'store_id': 1})
                self.assertEqual(resp.status_code, 200)
                self.assertEqual(ItemModel.find_by_name('test_item').price, 20.00)
                self.assertDictEqual(json.loads(resp.data), {'name': 'test_item',
                                                             'price': 20.00})



    def test_item_list(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test_store').save_to_db()
                # add item with price of 17.99
                ItemModel('test_item', 17.99, 1).save_to_db()

                resp = client.get('/items')
                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual(json.loads(resp.data),
                                     {'items': [{'name': 'test_item', 'price': 17.99}]} )
