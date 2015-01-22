from skeletor.util import decorators


class DatabaseContext(decorators.Context):

    def __init__(self, creator=None, context=None, commit=False):
        super(DatabaseContext, self).__init__()
        if context is None:
            context = creator(commit=commit)
        self._context = context
        self._commit = commit

    def acquire(self):
        pass

    def release(self):
        self._context.unbind()

    def success(self):
        if self._commit:
            self.commit()

    def error(self):
        if self.commit:
            self.rollback()

    def commit(self):
        self._context.commit()

    def rollback(self):
        self._context.rollback()

    def __getattr__(self, name):
        """Delegate attributes to the context"""
        return getattr(self._context, name)

    # TODO remove __getitem__ by doing foo.tables[table] rather than foo[table]
    # in table.py
    def __getitem__(self, item):
        """Delegate item lookup to the context"""
        return self._context[item]


class DatabaseFactory(decorators.DefaultFactory):

    @staticmethod
    def filter_kwargs(kwargs):
        opts = decorators.DefaultFactory.filter_kwargs(kwargs)
        for key in ('commit', 'creator'):
            opts[key] = kwargs.pop(key, None)
        return opts

    @staticmethod
    def create(creator=None, context=None, commit=False):
        return DatabaseContext(creator=creator, context=context, commit=commit)
