from sqlalchemy.exc import IntegrityError

from skeletor.core import log
from skeletor.db import sql
from skeletor.db.decorators import query
from skeletor.db.decorators import mutator


class ScopedLogger(object):
    """Prefix log messages with the calling code's class name"""

    def __init__(self, client, logger=None):
        if logger is None:
            logger = log.logger()
        cls = client.__class__
        self.logger = logger
        self.prefix = '%s.%s:' % (cls.__module__, cls.__name__)

    def __getattr__(self, name):
        fn = getattr(self.logger, name)
        wrapper = lambda msg, fn=fn: fn(self.prefix + msg)
        setattr(self, name, wrapper)
        return wrapper


class Table(object):
    """Run simple queries against specific tables"""

    def __init__(self, table, logger=None):
        self.table = table
        self.logger = ScopedLogger(self, logger=logger)

    @mutator
    def new(self, context=None, **kwargs):
        table = context.tables[self.table]
        try:
            row_id = table.insert(kwargs).execute().lastrowid
        except IntegrityError as e:
            self.logger.error('new: integrity error in %s with kwargs %s (%s)'
                              % (self.table, repr(kwargs), repr(e)))
            return None
        except BaseException as e:
            self.logger.error('new: unknown error in %s with kwargs %s (%s)'
                              % (self.table, repr(kwargs), repr(e)))
            return None
        return sql.select_one(table, id=row_id)

    @mutator
    def update(self, row_id, context=None, **kwargs):
        table = context.tables[self.table]
        return sql.update(table, row_id, **kwargs)

    @query
    def fetchall(self, context=None):
        table = context.tables[self.table]
        return sql.fetchall(table)

    @query
    def filter_by(self, context=None, **filters):
        table = context.tables[self.table]
        return sql.select_one(table, **filters)

    @query
    def find_by_id(self, row_id, context=None):
        return self.filter_by(id=row_id, context=context)

    @mutator
    def delete(self, context=None, **filters):
        table = context.tables[self.table]
        return sql.delete(table, **filters)
