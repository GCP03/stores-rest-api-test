import json

from models.item import ItemModel
from models.store import StoreModel
from tests.base_test import BaseTest


class StoreTest(BaseTest):
    def test_create_store(self):
        with self.app() as client:
            with self.app_context():
                resp = client.post('/store/test_store')

                # store added successfully
                self.assertEqual(resp.status_code, 201)
                self.assertIsNotNone(StoreModel.find_by_name('test_store'))
                self.assertDictEqual(json.loads(resp.data), {'name': 'test_store', 'items': []})


    def test_create_duplicate_store(self):
        with self.app() as client:
            with self.app_context():
                # add store
                client.post('/store/test_store')

                # add duplicate store
                resp = client.post('/store/test_store')
                self.assertEqual(resp.status_code, 400)
                self.assertDictEqual(json.loads(resp.data),
                                     {'message': "A store with name 'test_store' already exists."})

    def test_delete_store(self):
        with self.app() as client:
            with self.app_context():
                # add store
                # client.post('/store/test_store')
                # could do this instead to add store
                StoreModel('test_store').save_to_db()

                # delete store
                resp = client.delete('/store/test_store')
                self.assertEqual(resp.status_code, 200)
                self.assertEqual(json.loads(resp.data), {'message': 'Store deleted'})
                self.assertIsNone(StoreModel.find_by_name('test_store'))


    def test_find_store(self):
        with self.app() as client:
            with self.app_context():
                # add store
                client.post('/store/test_store')

                resp = client.get('/store/test_store')
                self.assertEqual(resp.status_code, 200)
                self.assertIsNotNone(StoreModel.find_by_name('test_store'))
                self.assertDictEqual(json.loads(resp.data), {'name': 'test_store', 'items': []})



    def test_store_not_found(self):
        with self.app() as client:
            with self.app_context():
                # store not added
                resp = client.get('/store/test_store')

                self.assertEqual(resp.status_code, 404)
                self.assertEqual(json.loads(resp.data), {'message': 'Store not found'})
                self.assertIsNone(StoreModel.find_by_name('test_store'))


    def test_store_found_with_items(self):
        with self.app() as client:
            with self.app_context():
                # add store
                client.post('/store/test_store')
                # add an item
                ItemModel('test_item', 19.99, 1).save_to_db()

                resp = client.get('/store/test_store')
                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual(json.loads(resp.data), {'name': 'test_store',
                                                             'items': [{'name': 'test_item',
                                                              'price': 19.99}]})

                # self.assertIsNotNone(StoreModel.find_by_name('test_store'))

    def test_store_list(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test_store').save_to_db()

                resp = client.get('/stores')
                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual(json.loads(resp.data), {'stores': [{'name': 'test_store',
                                                                         'items': []}]})


    def test_store_list_with_items(self):
        with self.app() as client:
            with self.app_context():
                # add store
                StoreModel('test_store').save_to_db()
                # add an item
                ItemModel('test_item', 19.99, 1).save_to_db()

                resp = client.get('/stores')
                self.assertEqual(resp.status_code, 200)
                expected = {'stores': [{'name': 'test_store',
                                        'items': [{'name': 'test_item',
                                                   'price': 19.99}]}]}
                self.assertDictEqual(json.loads(resp.data), expected)
