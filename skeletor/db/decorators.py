"""Decorators to simplify database access

skeletor database decorators makes it easy to provide access to common schema
or other database resource.  These are referred to as contexts.

Contexts provide access to a sqlalchemy session and provide it to their
decorated functions in the `context` keyword argument.

Contexts are created by a factory provided by the skeletor library,
:class:`skeletor.util.context.DatabaseFactory`.  In order to customize
how the context is created, the default factory support a `creator`
keyword argument that is called with a single `commit=<boolean>` argument
to signify whether the returned context should acquire a transaction.

skeletor provides decorators for read-only queries and transactional mutators.
Mutators will construct contexts with the keyword argument `commit=True`.
An internal context manager catches exceptions created in the wrapped
functions and automatically rollback mutator transactions when an
exception occurs.  Upon completion of a mutator function, the transaction is
committed.

When multiple mutator functions need to be chained then the `context` keyword
argument must be used when calling out to other decorated context functions.
e.g. `some_func(context=context)` will ensure that the context is reused and
passed through as-is rather than having to construct a new context for that
call.  This is also a good thing to do in general, even with queries, since it
will reuse the existing session instead of creating a new one for that call.

The expected use case is that you can use these decorators while binding
them to a custom creator function.

First, we'll define a simple schema.

.. sourcecode:: python

    from sqlachemy import Column, Integer, String

    from skeletor.db import schema
    from skeletor.db import context
    from skeletor.db import decorators
    from skeletor.db import sql


    class Schema(schema.Schema):
        def __init__(self):
            schema.Schema.__init__(self)
            self.add_table('users',
                Column('id', Integer, autoincrement=True, primary_key=True),
                Column('name', String),
                Column('email', String, unique=True))


    def new_schema():
        return Schema().bind_url('sqlite:///:memory:')


Next, we'll provide a :func:`creator` function that will wrap
our custom schema in a :class:`skeletor.db.context.DatabaseContext`.
This class provides the automatic commit/rollback logic.

.. sourcecode:: python

    def creator(commit=False):
        return context.DatabaseContext(context=new_schema())


To use the our custom creator with a free-form function we
decorate it and supply the decorator with our custom :func:`creator`.

.. sourcecode:: python

    @decorators.query.bind(creator=creator)
    def get_users(context=None):
        return context.users.select().execute().fetchall()

The end result is that callers do not need to worry about managing
contexts.  It will be automatically supplied by the decorator.

.. sourcecode:: python

    # Somewhere else
    users = get_users() #  no arguments required!

When :func:`get_users` is called, no context was provided so the provided
creator will be used to construct a context.  :func:`creator` constructs a
Schema object that defines the tables, binds it a URL, and returns the schema.
That schema is effectively what is seen by :func:`get_users`.

This extends to mutator functions.  Mutators are automatically
run within a transaction which is committed when the function finishes,
or rolls back if an exception occurs.

.. sourcecode:: python

    @decorators.mutator.bind(creator=creator)
    def create_user(context=None):
        table = context.users
        args = dict(name='hello', email='world')
        return table.insert(args).execute()

    create_user()

If you supply the context explicitly then no commit/rollback
is performed.  You must manually manage the context.

.. sourcecode:: python

    context = creator(commit=True)
    try:
        create_user(context=context)
        context.commit()
    except:
        context.rollback()

"""

from skeletor.db import context

from skeletor.util.decorators import acquire_context
from skeletor.util.decorators import bindfunc


@bindfunc()
def query(f):
    """Provide a read-only database context to a wrapped function"""
    return acquire_context(context.DatabaseFactory)(f)


@bindfunc()
def mutator(f):
    """Provide a transactional database context to a wrapped function"""
    return acquire_context(context.DatabaseFactory, commit=True)(f)


@bindfunc(decorator=staticmethod)
def staticmethod_query(f):
    """Provide a read-only database context to a wrapped function

    :returns: a staticmethod.

    """
    return acquire_context(context.DatabaseFactory)(f)


@bindfunc(decorator=staticmethod)
def staticmethod_mutator(f):
    """Provide a transactional database context to a wrapped function

    :returns: a staticmethod.

    """
    return acquire_context(context.DatabaseFactory, commit=True)(f)


@bindfunc(decorator=classmethod)
def classmethod_query(f):
    """Provide a read-only database context to a wrapped function

    :returns: a classmethod.

    """
    return acquire_context(context.DatabaseFactory)(f)


@bindfunc(decorator=classmethod)
def classmethod_mutator(f):
    """Provide a transactional database context to a wrapped function

    :returns: a classmethod.

    """
    return acquire_context(context.DatabaseFactory, commit=True)(f)
