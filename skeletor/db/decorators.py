"""Decorators to simplify database access

"""

from skeletor.db import context

from skeletor.util.decorators import acquire_context
from skeletor.util.decorators import bindfunc


@bindfunc()
def query(f):
    return acquire_context(context.DatabaseFactory)(f)


@bindfunc()
def mutator(f):
    return acquire_context(context.DatabaseFactory, commit=True)(f)


@bindfunc(decorator=staticmethod)
def staticmethod_query(f):
    return acquire_context(context.DatabaseFactory)(f)


@bindfunc(decorator=staticmethod)
def staticmethod_mutator(f):
    return acquire_context(context.DatabaseFactory, commit=True)(f)


@bindfunc(decorator=classmethod)
def classmethod_query(f):
    return acquire_context(context.DatabaseFactory)(f)


@bindfunc(decorator=classmethod)
def classmethod_mutator(f):
    return acquire_context(context.DatabaseFactory, commit=True)(f)
