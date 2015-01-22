from __future__ import absolute_import
import json
import os
from datetime import datetime
import logging


# Provided for compatibility with the python interface
load = json.load
dump = json.dump


def read(path):
    """Read JSON objects; return an empty dict on error"""
    # empty file == {} is used by the __include__ mechanism.
    if os.path.exists(path):
        try:
            with open(path) as fp:
                try:
                    return _read_includes(path, load(fp))
                except ValueError as e:
                    logging.debug('Invalid JSON: ' + path)
                    logging.debug(e)
        except IOError as e:
            logging.debug('IOError: ' + path)
            logging.debug(e)

    return {}


def _read_includes(path, data):
    """Allow config files to include others using an '__include__' tag"""
    try:
        include = data['__include__']
    except:
        return data
    if type(include) is list:
        subpaths = include
    else:
        subpaths = [include]

    for subpath in subpaths:
        if os.path.isabs(subpath):
            abspath = subpath
        else:
            # Relative paths are relative to the config file containing
            # the __include__ statement.
            abspath = os.path.join(os.path.dirname(path), subpath)
        # Allow variable references
        abspath_with_vars = os.path.expandvars(abspath)
        abspath_expanded = os.path.expanduser(abspath_with_vars)
        data.update(read(abspath_expanded))
    return data


def _handler(obj):
    """Handle serialization for sets and datetime objects"""
    if type(obj) is set:
        return list(obj)
    elif isinstance(obj, datetime) and hasattr(obj, 'isoformat'):
        return obj.isoformat()
    else:
        raise TypeError(repr(obj) + ' is not JSON serializable')


def dumps(obj, **kwargs):
    """Serialize an object into a JSON string"""
    return json.dumps(obj, default=_handler, **kwargs)


def loads(json_str):
    """Load an object from a JSON string"""
    return json.loads(json_str)


def write(obj, path):
    """Write object as JSON to path

    creates directories if needed

    """
    try:
        parent_dir = os.path.dirname(path)
        if not os.path.isdir(parent_dir):
            os.makedirs(parent_dir)

        with open(path, 'w') as fp:
            dump(obj, fp, indent=4, sort_keys=True, default=_handler)
            fp.write('\n')
            return True
    except IOError:
        return False
