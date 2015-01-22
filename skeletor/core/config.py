import os

from skeletor.core import json
from skeletor.core import util


class Config(object):
    """Read configuration values from a file"""

    def __init__(self, path):
        self._data = {}
        self._path = path

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
        return _expand(value)


class JSONConfig(Config):
    """Read configuration values from a JSON file"""

    def __init__(self, path):
        Config.__init__(self, path)

    def read(self):
        if self._data:
            return self._data
        config_data = json.read(self._path)
        util.deep_update(self._data, config_data)
        return self._data


def _expand(value):
    if isinstance(value, basestring):
        # Expand string values
        return util.expand_path(value)
    if hasattr(value, 'items'):
        return value.__class__([(k, _expand(v))
                                for k, v in value.items()])
    return value
