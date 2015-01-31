from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Text
from sqlalchemy.exc import IntegrityError

from skeletor.db import decorators
from skeletor.db import schema
from skeletor.db import context
from skeletor.db import sql


def create_database(test):
    test_schema = new_schema()
    engine = test_schema.engine
    test.assertEqual(engine.name, 'sqlite')
    test.assertEqual(engine.url.database, ':memory:')
    test.assertEqual(test_schema.dialect(), 'sqlite')

    return new_context(ctx=test_schema.create())


def new_schema():
    return Schema().bind_url('sqlite:///:memory:')


def new_context(ctx=None, commit=False):
    if ctx is None:
        ctx = new_schema()
    return context.DatabaseContext(context=ctx, commit=commit)


class Schema(schema.Schema):

    def __init__(self):
        schema.Schema.__init__(self)

        self.add_table('users',
                Column('id', Integer, primary_key=True, autoincrement=True),
                Column('name', Text),
                Column('email', Text, unique=True))


class User(object):

    @decorators.classmethod_query
    def new(cls, context=None, **kwargs):
        """Create a new from the attributes specified in kwargs

        Key names must match the column names from the schema.
        e.g.::

            user = User.new(nickname='godzilla', email='godzilla@example.com')
            if user is None:
                # user already exists
            else:
                # user created

        """
        users = context.users
        try:
            user_id = users.insert(kwargs).execute().lastrowid
        except IntegrityError:
            return None
        return cls.find_by_id(user_id, context=context)

    @decorators.staticmethod_query
    def fetchall(context=None):
        return sql.fetchall(context.users)

    @decorators.staticmethod_query
    def filter_by(context=None, **filters):
        return sql.select_one(context.users, **filters)

    @decorators.staticmethod_query
    def find_by_id(user_id, context=None):
        return sql.select_one(context.users, id=user_id)

    @decorators.staticmethod_mutator
    def update(user_id, context=None, **kwargs):
        return sql.update(context.users, user_id, **kwargs)
