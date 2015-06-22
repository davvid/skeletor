"""Decorators to simplify resource allocation

Many methods will require access to an initialized resource.
The :func:`acquire_context` decorator provides a live resource
context to its decorated function as the first argument.

Callers can override the decorator-provided resource
by passing in `context=...` as a keyword argument at
the call site, which is needed when the resource has
been pre-allocated and needs to be reused between calls.

"""

import functools


class DefaultFactory(object):
    """Creates contexts"""

    @staticmethod
    def filter_kwargs(kwargs):
        """Filter context arguments out from the function's kwargs"""
        filtered = {}
        for key in ('context', 'default_factory'):
            try:
                filtered[key] = kwargs.pop(key)
            except KeyError:
                pass
        return filtered

    @staticmethod
    def create(**kwargs):
        raise NotImplementedError('create() is not implemented')


class DefaultContextManager(object):

    def __init__(self, context=None, default_factory=None, *args, **kwargs):
        self.context = context
        self.default_factory = default_factory
        self.managed = False
        # Context arguments
        self.args = args
        self.kwargs = kwargs

    def __enter__(self):
        if self.default_factory is None:
            self.default_factory = DefaultFactory
        if self.context is None:
            managed = True
            context = self.default_factory.create(*self.args, **self.kwargs)
            context.acquire()
            self.context = context
        else:
            managed = False
            context = self.context
        self.managed = managed
        return context.__enter__()

    def __exit__(self, exc_type, exc_value, traceback):
        self.context.__exit__(exc_type, exc_value, traceback)
        if self.managed:
            self.context.release()
            self.context = None
        # Re-raise exceptions
        return False


def passthrough_decorator(f):
    """Return a function as-is, unchanged

    This is the default decorator used when creating contexts.

    """
    return f


class acquire_context(object):

    """A decorator to provide methods with a live resource context

    This decorator takes arguments, and thus the only time the
    to-be-decorated method is available is post-construction during
    the decoration process.  This happens in __call__, and it is
    called once.

    Methods inside a class can pass "decorator=staticmethod"
    if they want a static method.

    The blind `args` and `kwargs` are passed to the
    `default_factory` when contexts are constructed.

    """

    def __init__(self,
                 default_factory,
                 default_contextmgr=None,
                 decorator=None,
                 *args, **kwargs):
        # The default factory constructs context instances and
        # provides :func:`filter_kwargs()` to separate factory arguments
        # from function arguments.
        self.default_factory = default_factory
        # Allows overriding the context manager
        self.default_contextmgr = default_contextmgr or DefaultContextManager
        # Wraps our function with a user-supplied decorator
        self.decorator = decorator or passthrough_decorator
        # Factory arguments
        self.args = args
        self.kwargs = kwargs

    def __call__(self, f):
        """Wrap a function and return a decorated function

        The original function is passed to the decorator instance after
        construction and a wrapped function is returned.

        """
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            """Wraps f() to provide a context as a keyword argument"""
            factory_kwargs = self.default_factory.filter_kwargs(kwargs)
            factory_kwargs['default_factory'] = self.default_factory

            ctx_kwargs = self.kwargs.copy()
            ctx_kwargs.update(factory_kwargs)

            with self.default_contextmgr(*self.args, **ctx_kwargs) as context:
                kwargs['context'] = context
                return f(*args, **kwargs)

        return self.decorator(wrapper)


class bindfunc(object):
    """Allows fn.bind(foo=bar) when decorated on a decorator

    This is a decorator decorator, which takes a decorator as input
    and returns another decorator when applied, and grants decorators
    the ability to do `mydecorator.bind(foo=bar)` and have it work without
    having to repeat `foo=bar` everywhere.

    """

    def __init__(self, decorator=None):
        """:params decorator: outer decorator to apply"""
        self.decorator = decorator or passthrough_decorator
        self.args = ()
        self.kwargs = {}
        self.fn = None

    def bind(self, *args, **kwargs):
        """bind() stashes arguments"""
        self.args = args
        self.kwargs = kwargs
        return self

    def __call__(self, f):
        """Invoke the inner decorator and return a bound function

        __call__ is called twice.  The first time we are given the real
        function to decorate and return self so that we are called again
        when applying the decorator to the target function.

        The second time around we return the final, bound function.

        """
        if self.fn is None:
            # Store the decorator to decorate so that we can apply
            self.fn = f
            functools.update_wrapper(self, f)
            return self
        decorated = self.fn(f)
        return self.decorator(bind(*self.args, **self.kwargs)(decorated))


class Context(object):
    """Base class for custom contexts"""

    def acquire(self):
        """Called once iff the context is constructed by the context manager"""
        pass

    def __enter__(self):
        """Called when entering a context"""
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Called when exiting a context"""
        if exc_type is None:
            self.success()
        else:
            self.error()
        return False

    def success(self):
        """Called when exiting a context successfully"""
        pass

    def error(self):
        """Called when a exiting a context via an exception"""
        pass

    def release(self):
        """Called at the end of a context iff constructed by a manager"""
        pass


class bind(object):

    """A decorator to bind function parameters"""

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def __call__(self, f):
        """Wrap a function and return a decorated function"""

        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            args = self.args + args
            new_kwargs = self.kwargs.copy()
            new_kwargs.update(kwargs)
            return f(*args, **new_kwargs)

        return wrapper
