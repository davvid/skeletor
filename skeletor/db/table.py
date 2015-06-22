from sqlalchemy import and_
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

    def __init__(self, table, logger=None, verbose=False):
        self.table = table
        self.verbose = verbose
        if verbose:
            logger = ScopedLogger(self, logger=logger)
        self.logger = logger

    def get(self, context=None):
        return context.tables[self.table]

    @mutator
    def new(self, context=None, **kwargs):
        try:
            row_id = self.insert(kwargs, context=context)
        except IntegrityError as e:
            if self.verbose:
                self.logger.error('new: integrity error in %s -> %s (%s)'
                                  % (self.table, repr(kwargs), repr(e)))
            return None
        except BaseException as e:
            if self.verbose:
                self.logger.error('new: unknown error in %s -> %s (%s)'
                                  % (self.table, repr(kwargs), repr(e)))
            return None
        table = self.get(context=context)
        return sql.select_one(table, id=row_id)

    @mutator
    def update(self, row_id, context=None, **kwargs):
        table = self.get(context=context)
        return sql.update(table, row_id, **kwargs)

    @query
    def fetchall(self, context=None):
        table = self.get(context=context)
        return sql.fetchall(table)

    @query
    def filter_by(self, operator=and_, context=None, **filters):
        table = self.get(context=context)
        return sql.select_one(table, operator=operator, **filters)

    @query
    def select_all(self, context=None, **filters):
        table = self.get(context=context)
        return sql.select_all(table, **filters)

    @query
    def find_by_id(self, row_id, context=None):
        return self.filter_by(id=row_id, context=context)

    @mutator
    def insert(self, values, context=None):
        table = self.get(context=context)
        return table.insert(values).execute().lastrowid

    @mutator
    def delete(self, operator=and_, context=None, **filters):
        table = self.get(context=context)
        return sql.delete(table, operator=operator, **filters)
