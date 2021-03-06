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

    def test_ifilter_by(self):
        context = self.context
        self.table.new(name='first', email='A', context=context)
        self.table.new(name='second', email='B', context=context)

        user = self.table.ifilter_by(email='a', context=context)
        self.assertEqual(user['email'], 'A')

        user = self.table.ifilter_by(name='Second', email='A', context=context)
        self.assertEqual(user, None)

    def test_select_all(self):
        context = self.context
        self.table.new(name='a', email='a', context=context)
        self.table.new(name='a', email='a2', context=context)
        self.table.new(name='b', email='b', context=context)

        users = self.table.select_all(name='a', context=context)
        self.assertEqual(len(users), 2)
        self.assertEqual(users[0]['email'], 'a')
        self.assertEqual(users[1]['email'], 'a2')

    def test_delete(self):
        context = self.context
        self.table.new(email='a', context=context)
        self.table.new(email='b', context=context)
        all_users = self.table.fetchall(context=context)
        self.assertEqual(len(all_users), 2)

        self.table.delete(email='a', context=context)
        all_users = self.table.fetchall(context=context)
        self.assertEqual(len(all_users), 1)
        self.assertEqual(all_users[0]['email'], 'b')


if __name__ == '__main__':
    unittest.main()
