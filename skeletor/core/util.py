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
