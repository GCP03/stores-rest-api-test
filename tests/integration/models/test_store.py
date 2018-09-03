from models.item import ItemModel
from models.store import StoreModel
from tests.base_test import BaseTest


class StoreTest(BaseTest):
    def test_create_store(self):
        store = StoreModel('test_store')

        self.assertListEqual(store.items.all(), [],
                             'The store"s length is not0 even though no items were added')

    def test_crud(self):
        with self.app_context():
            store = StoreModel('test_store')

            # not added to db yet
            self.assertIsNone(store.find_by_name('test_store'),
                              "Store has not been added but already exists")

            # add to db
            store.save_to_db()
            self.assertIsNotNone(store.find_by_name('test_store'),
                                 "Store was added but is not found")

            # delete to db
            store.delete_from_db()
            self.assertIsNone(store.find_by_name('test_store'),
                              "Store was deleted but is still found")

    def test_store_relationship(self):
        with self.app_context():
            store = StoreModel('test_store')
            item = ItemModel('test_item', 19.99, 1)

            store.save_to_db()
            item.save_to_db()

            self.assertEqual(store.items.count(), 1)
            self.assertEqual(store.items.first().name, 'test_item',
                             f"Store name is {store.items.first().name}, expected 'test_item'")
            self.assertEqual(store.items.first().price, 19.99)
            self.assertEqual(store.items.first().id, 1)

    def test_store_json(self):
        store = StoreModel('test_store')
        expected = {
            'name': 'test_store',
            'items': []
        }
        self.assertEqual(store.json(), expected)
    def test_store_json_with_item(self):
        with self.app_context():
            store = StoreModel('test_store')
            item = ItemModel('test_item', 19.99, 1)

            store.save_to_db()
            item.save_to_db()

            expected = {
                'name': 'test_store',
                'items': [{'name': 'test_item', 'price': 19.99}]
            }
            self.assertEqual(store.json(), expected)
