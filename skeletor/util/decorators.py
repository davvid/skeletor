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
        return dict([(key, kwargs.pop(key, None))
                     for key in ('context', 'default_factory')])

    @staticmethod
    def create(**kwargs):
        raise NotImplemented('create() is not implemented')



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
                 decorator=None,
                 default_factory=None,
                 default_contextmgr=None,
                 *args, **kwargs):
        # A decorator allows us to automatically wrap our output
        self.decorator = decorator or passthrough_decorator
        # The default factory constructs context instances and
        # provides :func:`filter_kwargs()` to separate factory arguments
        # from function arguments.
        self.default_factory = default_factory
        # Allows overriding the context manager
        self.default_contextmgr = default_contextmgr or DefaultContextManager
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
            context_kwargs = self.default_factory.filter_kwargs(kwargs)
            context_kwargs['default_factory'] = self.default_factory
            context_kwargs.update(self.kwargs)
            with self.default_contextmgr(*self.args, **context_kwargs) as context:
                kwargs['context'] = context
                return f(*args, **kwargs)

        return self.decorator(wrapper)


class bindfunction(object):
    """Allows fn.bind(foo=bar) when decorated on a function"""

    def __init__(self, fn, decorator=passthrough_decorator):
        """This decorator is passed an inner decorator"""
        self.fn = fn
        self.args = ()
        self.kwargs = {}
        self.decorator = decorator

    def bind(self, *args, **kwargs):
        """bind() stashes arguments"""
        self.args = args
        self.kwargs = kwargs
        return self

    def __call__(self, f):
        """Invoke the inner decorator and return a bound function

        __call__() is invoked when the function is ready to be decorated.
        If we've gotten here then bind() was called and we must return the
        final decorated function.

        """
        decorated = self.fn(f)
        return self.decorator(bind(*self.args, **self.kwargs)(decorated))


class bindstaticmethod(bindfunction):
    """Allows fn.bind(foo=bar) and returns a staticmethod"""

    def __init__(self, f):
        super(bindstaticmethod, self).__init__(f, decorator=staticmethod)


class bindclassmethod(bindfunction):
    """Allows fn.bind(foo=bar) and returns a classmethod"""

    def __init__(self, f):
        super(bindclassmethod, self).__init__(f, decorator=classmethod)


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
