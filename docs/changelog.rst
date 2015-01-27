Change Log
==========
Version 0.0.1 - January 2015
----------------------------
    * The initial skeletor release contains powerful decorators and utility
      classes for use with SQLAlchemy databases.
    * The core things needed to support a databse-backed application are
      configuration, logging, and database context/session management.
    * Configuration is used for getting credentials since they should
      not live alongside the library and application code.
    * Logging is needed for reporting database and application errors.
    * Database context management is needed to streamline the work needed
      to establish database connections and transactions.
    * Skeletor's database decorators allow you to tag a function as a
      "mutator", which means that calling it without an existing context will
      create a context, start a transation, and call into the function.  If
      the function raises any exceptions then the transaction is automatically
      rolled back by the database context manager.
