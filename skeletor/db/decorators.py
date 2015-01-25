"""Decorators to simplify database access

"""

from skeletor.db import context

from skeletor.util.decorators import acquire_context
from skeletor.util.decorators import bindfunction
from skeletor.util.decorators import bindstaticmethod
from skeletor.util.decorators import bindclassmethod


@bindfunction
def query(f):
    return acquire_context(default_factory=context.DatabaseFactory)(f)


@bindfunction
def mutator(f):
    return acquire_context(default_factory=context.DatabaseFactory,
                           commit=True)(f)


@bindstaticmethod
def staticmethod_query(f):
    return acquire_context(default_factory=context.DatabaseFactory)(f)


@bindstaticmethod
def staticmethod_mutator(f):
    return acquire_context(default_factory=context.DatabaseFactory,
                           commit=True)(f)


@bindclassmethod
def classmethod_query(f):
    return acquire_context(default_factory=context.DatabaseFactory)(f)


@bindclassmethod
def classmethod_mutator(f):
    return acquire_context(default_factory=context.DatabaseFactory,
                           commit=True)(f)
