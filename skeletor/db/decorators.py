"""Decorators to simplify database access

"""

from skeletor.db import context
from skeletor.util import decorators


def query(f):
    return decorators.acquire_context(default_factory=context.DatabaseFactory)(f)


def mutator(f):
    return decorators.acquire_context(default_factory=context.DatabaseFactory,
                                      commit=True)(f)


def staticmethod_query(f):
    return decorators.acquire_context(default_factory=context.DatabaseFactory,
                                      decorator=staticmethod)(f)


def staticmethod_mutator(f):
    return decorators.acquire_context(default_factory=context.DatabaseFactory,
                                      decorator=staticmethod,
                                      commit=True)(f)


def classmethod_query(f):
    return decorators.acquire_context(default_factory=context.DatabaseFactory,
                                      decorator=classmethod)(f)


def classmethod_mutator(f):
    return decorators.acquire_context(default_factory=context.DatabaseFactory,
                                      decorator=classmethod,
                                      commit=True)(f)
