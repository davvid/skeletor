from sqlalchemy import Table
from sqlalchemy import MetaData
from sqlalchemy import create_engine


DEFAULT_STRATEGY = 'threadlocal'


def engine(url, strategy=DEFAULT_STRATEGY):
    return create_engine(url, strategy=strategy)


class Schema(object):

    def __init__(self):
        self.engine = None
        self.metadata = MetaData()
        self.tables = {}

    def add_table(self, name, *columns, **kwargs):
        self.tables[name] = Table(name, self.metadata, *columns, **kwargs)

    def __getitem__(self, name):
        """For convenience so that subclasses can say schema[table]"""
        return self.tables[name]

    def __getattr__(self, name):
        """For convenience so that subclasses can say schema.table"""
        return self.tables[name]

    def bind_url(self, url, strategy=DEFAULT_STRATEGY):
        return self.bind(engine(url, strategy=strategy))

    def bind(self, engine):
        """Bind a sqlalchemy engine to the table metadata"""
        self.engine = engine
        self.metadata.bind = engine
        return self

    def unbind(self):
        """Unbind the metadata"""
        self.metadata.bind = None
        if self.engine is not None:
            self.engine.dispose()
        self.engine = None
        return self

    def create(self):
        """Create missing tables"""
        self.metadata.create_all()
        self.commit()
        return self

    def dialect(self):
        """The name of the bound engine dialect"""
        if self.engine is None:
            dialect = 'unknown'
        else:
            dialect = self.engine.name
        return dialect

    def commit(self):
        """Commit a transaction"""
        self.engine.commit()

    def rollback(self):
        """Rollback a transaction"""
        self.engine.rollback()
