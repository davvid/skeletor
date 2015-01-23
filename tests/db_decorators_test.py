import unittest

from tests import testlib

from skeletor.db import decorators
from skeletor.db import sql
from skeletor.util import decorators as core_decorators


def creator(commit=False):
    test_schema = testlib.new_schema()
    test_schema.create()

    ctx = testlib.new_context(ctx=test_schema, commit=commit)
    testlib.User.new(name='test', email='test@example.com', context=ctx)
    return ctx


@decorators.query
def select_one(context=None, **kwargs):
    return sql.select_one(context.users, **kwargs)


bound_select_one = core_decorators.bind(creator=creator)(select_one)


class DBDecoratorsTestCase(unittest.TestCase):

    def setUp(self):
        self.name = 'test'
        self.email = 'test@example.com'
        self.context = testlib.create_database(self)

    def test_new_user(self):
        context = self.context
        user = testlib.User.new(name=self.name, context=context)
        self.assertEqual(user['name'], self.name)

    def test_update_user(self):
        context = self.context
        user = testlib.User.new(name=self.name, email=self.email, context=context)
        self.assertEqual(user['name'], self.name)
        user_id = user['id']

        testlib.User.update(user_id, name='updated', context=context)
        user = testlib.User.find_by_id(user_id, context=context)
        self.assertEqual(user['name'], 'updated')

    def test_duplicate_user(self):
        context = self.context
        user = testlib.User.new(email=self.email, context=context)
        self.assertEqual(user['email'], self.email)

        user = testlib.User.new(email=self.email, context=context)
        self.assertEqual(user, None)

    def test_fetchall(self):
        context = self.context
        testlib.User.new(email='a', context=context)
        testlib.User.new(email='b', context=context)
        all_users = testlib.User.fetchall(context=context)
        self.assertEqual(len(all_users), 2)
        self.assertEqual(all_users[0]['email'], 'a')
        self.assertEqual(all_users[1]['email'], 'b')


    def test_creator(self):
        user = select_one(email='test@example.com', creator=creator)
        self.assertEqual(user['name'], 'test')

        user = select_one(name='test', creator=creator)
        self.assertEqual(user['email'], 'test@example.com')

    def test_bound_creator(self):
        user = bound_select_one(email='test@example.com')
        self.assertEqual(user['name'], 'test')

        user = bound_select_one(name='test')
        self.assertEqual(user['email'], 'test@example.com')


if __name__ == '__main__':
    unittest.main()
