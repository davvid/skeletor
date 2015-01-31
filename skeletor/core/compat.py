# -*- coding: utf-8 -*-

__all__ = ('bytes', 'set', 'unicode', 'long', 'unichr')

import sys

PY_MAJOR = sys.version_info[0]
PY_MINOR = sys.version_info[1]
PY2 = PY_MAJOR == 2
PY3 = PY_MAJOR == 3

try:
    bytes = bytes
except NameError:
    bytes = str

try:
    set = set
except NameError:
    from sets import Set as set
    set = set

try:
    unicode = unicode
except NameError:
    unicode = str

try:
    long = long
except NameError:
    long = int

try:
    unichr = unichr
except NameError:
    unichr = chr
