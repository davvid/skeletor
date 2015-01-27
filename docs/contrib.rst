========================
Contributing to skeletor
========================

We welcome contributions from everyone.
Please fork this project on `github <http://github.com/davvid/skeletor>`_.

Get the Code
============

.. _contrib-clone:

::

    git clone git://github.com/davvid/skeletor.git

Run the Test Suite
==================

All tests must pass before code can be pulled into the master branch.
If you are contributing an addition or a change in behavior, we ask that you
document the change in the form of test cases.

In order to run the test cases you will need to install some dependencies into
your test environment.  We recomment using tox_ To simplify the process of
setting up a test environment.

To run the suite, simply invoke `make test` or use tox_ to run the unittests
across multiple Python versions::

    $ make test
    nosetests --with-doctest  skeletor tests
    .............................
    ----------------------------------------------------------------------
    Ran 29 tests in 0.544s

.. _tox: https://testrun.org/tox/latest/

Generate Documentation
======================

You do not need to generate the documentation_ when contributing, though, if
you are interested, you can generate the docs yourself.  The following requires
Sphinx_::

    cd docs
    make html

If you wish to browse the documentation, use Python's :mod:`SimpleHTTPServer`
to host them at http://localhost:8000::

    cd build/html
    python -m SimpleHTTPServer

.. _documentation: https://skeletor.readthedocs.org
.. _Sphinx: http://sphinx.pocoo.org
