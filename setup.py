#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2015 David Aguilar (davvid -at- gmail.com)
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.

import os
try:
    import setuptools as setup_mod
except ImportError:
    import distutils.core as setup_mod

here = os.path.dirname(__file__)
version = os.path.join(here, 'skeletor', 'core', 'version.py')
scope = {}
exec(open(version).read(), scope)

SETUP_ARGS = dict(
    name='skeletor',
    version=scope['VERSION'],
    description='application skeleton',
    long_description='skeletor is a reusable application skeleton',
    author='David Aguilar',
    author_email='davvid@gmail.com',
    url='https://github.com/davvid/skeletor',
    license='BSD',
    platforms=['POSIX'],
    keywords=['skeletor', 'skeleton', 'application', 'utilities'],
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
    ],
    options={'clean': {'all': 1}},
    packages=['skeletor', 'skeletor.core', 'skeletor.db', 'skeletor.util'],
)

if __name__ == '__main__':
    setup_mod.setup(**SETUP_ARGS)
