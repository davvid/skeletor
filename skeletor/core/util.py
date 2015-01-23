import os
import base64
import random
import uuid


def deep_update(a, b):
    """Allow piece-wise overriding of dictionaries"""
    for k, v in b.items():
        if type(v) is dict and type(a) is dict and type(a.get(k)) is dict:
            deep_update(a[k], v)
        else:
            a[k] = v


def import_string(modstr):
    """Resolve a package.module.variable string"""
    module_name, module_var = modstr.rsplit('.', 1)

    module = __import__(module_name)
    for elt in module_name.split('.')[1:]:
        module = getattr(module, elt)

    return getattr(module, module_var)


def rand32():
    return int(random.getrandbits(32))


def randb64():
    return base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes)
