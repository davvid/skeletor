.. _api:

=========================
skeletor API documenation
=========================

.. testsetup:: *

    import skeletor
    import skeletor.core
    import skeletor.core.compat
    import skeletor.core.log
    import skeletor.core.json
    import skeletor.core.util
    import skeletor.core.version
    import skeletor.db
    import skeletor.db.context
    import skeletor.db.decorators
    import skeletor.db.schema
    import skeletor.db.table
    import skeletor.util
    import skeletor.util.config
    import skeletor.util.decorators
    import skeletor.util.string

.. contents::


:mod:`skeletor.core` -- Skeleton core components
================================================

:mod:`skeletor.core.compat` -- Compatibility adapters
-----------------------------------------------------

.. automodule:: skeletor.core.compat

:mod:`skeletor.core.json` -- JSON utilities
-------------------------------------------

.. automodule:: skeletor.core.json
    :members:

:mod:`skeletor.core.log` -- Logging
-----------------------------------

.. automodule:: skeletor.core.log
    :members:

:mod:`skeletor.core.util` -- Utilities
--------------------------------------

.. automodule:: skeletor.core.util
    :members:

:mod:`skeletor.core.version` -- Library version
-----------------------------------------------

.. automodule:: skeletor.core.version
    :members:

:mod:`skeletor.util` -- Reusable utilities
==========================================

:mod:`skeletor.util.config` -- Configuration file readers
---------------------------------------------------------

.. automodule:: skeletor.util.config
    :members:

:mod:`skeletor.util.decorators` -- Function decorators for managing contexts
----------------------------------------------------------------------------

.. automodule:: skeletor.util.decorators
    :members:

:mod:`skeletor.util.string` -- String utilities
-----------------------------------------------

.. automodule:: skeletor.util.string
    :members:

:mod:`skeletor.db` -- SQLAlchemy powertools
===========================================

:mod:`skeletor.db.context` -- Default database context
------------------------------------------------------

.. automodule:: skeletor.db.context
    :members:

:mod:`skeletor.db.decorators` -- Decorators for providing contexts
------------------------------------------------------------------

.. automodule:: skeletor.db.decorators
   :members:

.. autofunction:: skeletor.db.decorators.query
.. autofunction:: skeletor.db.decorators.mutator
.. autofunction:: skeletor.db.decorators.staticmethod_query
.. autofunction:: skeletor.db.decorators.staticmethod_mutator
.. autofunction:: skeletor.db.decorators.classmethod_query
.. autofunction:: skeletor.db.decorators.classmethod_mutator

:mod:`skeletor.db.schema` -- Schema definitions
-----------------------------------------------

.. automodule:: skeletor.db.schema
    :members:

:mod:`skeletor.db.sql` -- SQLAlchemy helpers and utilities
----------------------------------------------------------

.. automodule:: skeletor.db.sql
    :members:

:mod:`skeletor.db.table` -- Query SQLAlchemy tables
---------------------------------------------------

.. automodule:: skeletor.db.table
    :members:
