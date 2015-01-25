Skeletor - A reusable Python app skeleton
=========================================
This repository contains code for a sqlalchemy-based database API
and common application concerns such as logging and configuration.

Configuration Files
-------------------
Skeletor can read json files with special directives to include other files.
See (here)[tests/example.json] for an example.

Logging
-------
Instantiate a logger by doing:

    from skeletor.core import log

    logger = log.logger(__name__)

    def main():
        # call during application startup
        log.init(verbose=True)

    # elsewhere
    def example():
        logger.debug('hello world')
