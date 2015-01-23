import os

from skeletor.core import json
from skeletor.core import util
from skeletor.util import string


class Config(object):
    """Read configuration values from a file"""

    def __init__(self, path, environ=None):
        self._data = {}
        self._path = path
        self.environ = environ
        self.initialize_environ()

    def initialize_environ(self):
        pass

    def __getitem__(self, item):
        """Allow config[key]"""
        self.read()
        return self._data[item]

    def __getattr__(self, attr):
        self.read()
        return self._data[attr]

    def read(self):
        raise NotImplemented('read() must be implemented by %s'
                             % self.__class__.__name__)

    def reset(self):
        self._data = {}

    def value(self, key, env=None):
        """Return a configured value"""
        self.read()
        value = self._data[key]
        if env is not None:
            # This key has a corresponding environment variable
            # so override the value if the variable is defined.
            value = os.getenv(env, value)
        return _expand(value, self.environ)


class JSONConfig(Config):
    """Read configuration values from a JSON file"""

    def __init__(self, path, environ=None):
        super(JSONConfig, self).__init__(path, environ=environ)

    def read(self):
        if self._data:
            return self._data
        config_data = json.read(self._path)
        util.deep_update(self._data, config_data)
        return self._data


def _expand(value, environ):
    if isinstance(value, basestring):
        # Expand string values
        return string.expand_path(value, environ)
    if hasattr(value, 'items'):
        return value.__class__([(k, _expand(v, environ))
                                for k, v in value.items()])
    return value
