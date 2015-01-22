import unittest

from tests import testlib

from skeletor.db import table


class DBTableTestCase(unittest.TestCase):

    def setUp(self):
        self.name = 'test'
        self.email = 'test@example.com'
        self.context = testlib.create_database(self)
        self.table = table.Table('users')

    def test_new_user(self):
        context = self.context
        user = self.table.new(name=self.name, context=context)
        self.assertEqual(user['name'], self.name)

    def test_find_by_id(self):
        context = self.context
        user = self.table.new(name=self.name, email=self.email, context=context)
        self.assertEqual(user['name'], self.name)
        user_id = user['id']

        user = self.table.find_by_id(user_id, context=context)
        self.assertEqual(user['name'], self.name)

    def test_update_user(self):
        context = self.context
        user = self.table.new(name=self.name, email=self.email, context=context)
        self.assertEqual(user['name'], self.name)
        user_id = user['id']

        self.table.update(user_id, name='updated', context=context)
        user = self.table.find_by_id(user_id, context=context)
        self.assertEqual(user['name'], 'updated')

    def test_duplicate_user(self):
        context = self.context
        user = self.table.new(email=self.email, context=context)
        self.assertEqual(user['email'], self.email)

        user = self.table.new(email=self.email, context=context)
        self.assertEqual(user, None)

    def test_fetchall(self):
        context = self.context
        self.table.new(email='a', context=context)
        self.table.new(email='b', context=context)
        all_users = self.table.fetchall(context=context)
        self.assertEqual(len(all_users), 2)
        self.assertEqual(all_users[0]['email'], 'a')
        self.assertEqual(all_users[1]['email'], 'b')

    def test_filter_by(self):
        context = self.context
        self.table.new(name='first', email='a', context=context)
        self.table.new(name='second', email='b', context=context)

        user = self.table.filter_by(email='a', context=context)
        self.assertEqual(user['email'], 'a')

        user = self.table.filter_by(name='second', email='a', context=context)
        self.assertEqual(user, None)


if __name__ == '__main__':
    unittest.main()
