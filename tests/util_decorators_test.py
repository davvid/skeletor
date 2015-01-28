import unittest

from skeletor.util import decorators


# Decorators for testing bind() and bindfunc()

@decorators.bind(foo='bar')
def bind_foo(foo=None, *args, **kwargs):
    return (foo, args, kwargs)


@decorators.bindfunc()
def mydecorator(f):
    def wrapper(*args, **kwargs):
        return ('decorated', f(*args, **kwargs))
    return wrapper


@decorators.bindfunc(decorator=staticmethod)
def mydecorator_staticmethod(f):
    def wrapper(*args, **kwargs):
        return ('decorated', f(*args, **kwargs))
    return wrapper


@decorators.bindfunc(decorator=classmethod)
def mydecorator_classmethod(f):
    def wrapper(*args, **kwargs):
        return ('decorated', f(*args, **kwargs))
    return wrapper


# Use the decorators to create various methods in a class

class Example(object):

    @mydecorator.bind(foo='bar')
    def bindfunc_foo(self, foo=None, **kwargs):
        return (foo, kwargs)

    @staticmethod
    @mydecorator.bind(foo='bar')
    def bindfunc_foo_explicit_staticmethod(foo=None, **kwargs):
        return (foo, kwargs)

    @mydecorator_staticmethod.bind(foo='bar')
    def bindfunc_foo_staticmethod(foo=None, **kwargs):
        return (foo, kwargs)

    @classmethod
    @mydecorator.bind(foo='bar')
    def bindfunc_foo_explicit_classmethod(cls, foo=None, **kwargs):
        return (cls.__name__, foo, kwargs)

    @mydecorator_classmethod.bind(foo='bar')
    def bindfunc_foo_classmethod(cls, foo=None, **kwargs):
        return (cls.__name__, foo, kwargs)


class CustomContext(decorators.Context):
    """Custom context for testing acquire_context()"""

    def __init__(self, foo='context-foo', bar='context-bar', *args, **kwargs):
        self.foo = foo
        self.bar = bar
        self.args = args
        self.kwargs = kwargs
        self._ok = None

    def ok(self):
        return self._ok

    def success(self):
        self._ok = True

    def error(self):
        self._ok = False


class CustomFactory(decorators.DefaultFactory):
    """Custom factory for testing acquire_context()"""

    @staticmethod
    def filter_kwargs(kwargs):
        base = decorators.DefaultFactory.filter_kwargs(kwargs)
        try:
            base['foo'] = kwargs.pop('foo')
        except KeyError:
            pass
        return base

    @staticmethod
    def create(foo='create', *args, **kwargs):
        return CustomContext(foo=foo, *args, **kwargs)


@decorators.acquire_context(CustomFactory)
def acquires_custom_context(*args, **kwargs):
    return (args, kwargs)


@decorators.acquire_context(CustomFactory, foo='decorator')
def acquires_custom_context_with_foo(*args, **kwargs):
    return (args, kwargs)


@decorators.acquire_context(CustomFactory, bar='decorator')
def acquires_custom_context_with_bar(*args, **kwargs):
    return (args, kwargs)


class DecoratorsTestCase(unittest.TestCase):

    # bind() tests

    def test_bind_simple_noargs(self):
        expect = 'bar'
        actual = bind_foo()
        self.assertEqual(expect, actual[0])

    def test_bind_simple_passing_foo(self):
        expect = 'baz'
        actual = bind_foo(foo='baz')
        self.assertEqual(expect, actual[0])

    # bindfunc() tests

    def test_bind_method_noargs(self):
        example = Example()
        expect = ('decorated', ('bar', {}))
        actual = example.bindfunc_foo()
        self.assertEqual(expect, actual)

    def test_bind_method_passing_foo(self):
        example = Example()
        expect = ('decorated', ('baz', {}))
        actual = example.bindfunc_foo(foo='baz')
        self.assertEqual(expect, actual)

    def test_bind_explicit_staticmethod_noargs(self):
        expect = ('decorated', ('bar', {}))
        # via class
        actual = Example.bindfunc_foo_explicit_staticmethod()
        self.assertEqual(expect, actual)
        # via instance
        example = Example()
        actual = example.bindfunc_foo_explicit_staticmethod()
        self.assertEqual(expect, actual)

    def test_bind_explicit_staticmethod_passing_foo(self):
        expect = ('decorated', ('baz', {}))
        # via class
        actual = Example.bindfunc_foo_explicit_staticmethod(foo='baz')
        self.assertEqual(expect, actual)
        # via instance
        example = Example()
        actual = example.bindfunc_foo_explicit_staticmethod(foo='baz')
        self.assertEqual(expect, actual)

    def test_bind_staticmethod_noargs(self):
        expect = ('decorated', ('bar', {}))
        # via class
        actual = Example.bindfunc_foo_staticmethod()
        self.assertEqual(expect, actual)
        # via instance
        example = Example()
        actual = example.bindfunc_foo_explicit_staticmethod()
        self.assertEqual(expect, actual)

    def test_bind_staticmethod_passing_foo(self):
        expect = ('decorated', ('baz', {}))
        # via class
        actual = Example.bindfunc_foo_staticmethod(foo='baz')
        self.assertEqual(expect, actual)
        # via instance
        example = Example()
        actual = example.bindfunc_foo_explicit_staticmethod(foo='baz')
        self.assertEqual(expect, actual)

    def test_bind_explicit_classmethod_noargs(self):
        expect = ('decorated', (Example.__name__, 'bar', {}))
        # via class
        actual = Example.bindfunc_foo_explicit_classmethod()
        self.assertEqual(expect, actual)
        # via instance
        example = Example()
        actual = example.bindfunc_foo_explicit_classmethod()
        self.assertEqual(expect, actual)

    def test_bind_explicit_classmethod_passing_foo(self):
        expect = ('decorated', (Example.__name__, 'baz', {}))
        # via class
        actual = Example.bindfunc_foo_explicit_classmethod(foo='baz')
        self.assertEqual(expect, actual)
        # via instance
        example = Example()
        actual = example.bindfunc_foo_explicit_classmethod(foo='baz')
        self.assertEqual(expect, actual)

    def test_bind_classmethod_noargs(self):
        expect = ('decorated', (Example.__name__, 'bar', {}))
        # via class
        actual = Example.bindfunc_foo_classmethod()
        self.assertEqual(expect, actual)
        # via instance
        example = Example()
        actual = example.bindfunc_foo_explicit_classmethod()
        self.assertEqual(expect, actual)

    def test_bind_classmethod_passing_foo(self):
        expect = ('decorated', (Example.__name__, 'baz', {}))
        # via class
        actual = Example.bindfunc_foo_classmethod(foo='baz')
        self.assertEqual(expect, actual)
        # via instance
        example = Example()
        actual = example.bindfunc_foo_explicit_classmethod(foo='baz')
        self.assertEqual(expect, actual)

    # acquire_context() tests

    def test_acquire_context_noargs(self):
        result = acquires_custom_context()

        args = result[0]
        self.assertEqual(args, ())

        kwargs = result[1]
        context = kwargs.pop('context')
        self.assertTrue(isinstance(context, CustomContext))
        self.assertTrue(context.ok())

        self.assertEqual(kwargs, {})

    def test_acquire_context_passes_others(self):
        result = acquires_custom_context('arg1', 'arg2',
                                         default_factory=CustomFactory,
                                         foo='bar', not_foo='baz')
        args = result[0]
        kwargs = result[1]

        expect = ('arg1', 'arg2')
        actual = args
        self.assertEqual(expect, actual)

        self.assertTrue('context' in kwargs)
        self.assertTrue('default_factory' not in kwargs)

        context = kwargs['context']
        self.assertTrue(isinstance(context, CustomContext))
        self.assertTrue('default_factory' not in context.kwargs)

        expect = ()
        actual = context.args
        self.assertEqual(expect, actual)

        expect = 'bar'
        actual = context.foo
        self.assertEqual(expect, actual)

    def test_acquire_context_passes_not_foo(self):
        result = acquires_custom_context(default_factory=CustomFactory,
                                         not_foo='baz')
        args = result[0]
        kwargs = result[1]

        expect = ()
        actual = args
        self.assertEqual(expect, actual)

        context = kwargs['context']
        self.assertTrue(isinstance(context, CustomContext))
        self.assertTrue('default_factory' not in context.kwargs)

        expect = ()
        actual = context.args
        self.assertEqual(expect, actual)

        # The context has foo='context' and we want to ensure that
        # we do not get that value here, but rather the default from "create"
        expect = 'create'
        actual = context.foo
        self.assertEqual(expect, actual)

    def test_acquire_context_passes_context_and_others(self):
        ctx = decorators.Context()
        result = acquires_custom_context('arg1', 'arg2', context=ctx, not_foo='bar')

        expect = ('arg1', 'arg2')
        actual = result[0]
        self.assertEqual(expect, actual)

        context = result[1]['context']
        self.assertTrue(ctx is context)

        expect = 'bar'
        actual = result[1]['not_foo']
        self.assertEqual(expect, actual)

    def test_acquire_context_with_foo_gets_decorator_foo(self):
        result = acquires_custom_context_with_foo()
        args = result[0]
        kwargs = result[1]

        expect = ()
        actual = args
        self.assertEqual(expect, actual)

        context = kwargs['context']
        self.assertTrue(isinstance(context, CustomContext))
        self.assertTrue('default_factory' not in context.kwargs)

        expect = ()
        actual = context.args
        self.assertEqual(expect, actual)

        # The context has foo='context' and we want to ensure that
        # we do not get that value here, but rather the default from
        # "decorator"
        expect = 'decorator'
        actual = context.foo
        self.assertEqual(expect, actual)

    def test_acquire_context_with_foo_gets_caller_foo(self):
        # Make sure that the caller can replace the value seen
        # by the final function
        result = acquires_custom_context_with_foo(foo='caller')
        kwargs = result[1]
        context = kwargs['context']

        expect = 'caller'
        actual = context.foo
        self.assertEqual(expect, actual)

    def test_acquire_context_with_bar_gets_correct_bar(self):
        # Same test, but this time using a kwarg that is not used by the creator
        result = acquires_custom_context_with_bar()
        kwargs = result[1]
        context = kwargs['context']

        expect = 'decorator'
        actual = context.bar
        self.assertEqual(expect, actual)

        # The creator supplies foo
        expect = 'create'
        actual = context.foo
        self.assertEqual(expect, actual)

        # Make sure that the caller can replace the value seen
        # by the final function
        result = acquires_custom_context_with_bar(bar='caller')
        kwargs = result[1]
        context = kwargs['context']

        # The caller supplies bar, find it in kwargs because it
        # is not consumed by the factory.
        expect = 'caller'
        actual = kwargs['bar']
        self.assertEqual(expect, actual)


if __name__ == '__main__':
    unittest.main()
