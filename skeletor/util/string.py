"""Functions for formatting various data strings"""

import re
import os

_expandvars_re = None

def expandvars(path, environ=None):
    """
    Like os.path.expandvars, but operates on a provided dictionary

    `os.environ` is used when `environ` is None.

    >>> expandvars('$foo', environ={'foo': 'bar'})
    'bar'

    >>> expandvars('$foo:$bar:${foo}${bar}', environ={'foo': 'a', 'bar': 'b'})
    'a:b:ab'

    """
    global _expandvars_re
    if '$' not in path:
        return path
    if _expandvars_re is None:
        _expandvars_re = re.compile(r'\$(\w+|\{[^}]*\})')
    if environ is None:
        environ = os.environ.copy()
    i = 0
    while True:
        m = _expandvars_re.search(path, i)
        if not m:
            break
        i, j = m.span(0)
        name = m.group(1)
        if name.startswith('{') and name.endswith('}'):
            name = name[1:-1]
        if name in environ:
            tail = path[j:]
            path = path[:i] + environ[name]
            i = len(path)
            path += tail
        else:
            i = j
    return path
