import inspect
import logging
import os
import pprint
import sys
import traceback

from skeletor.core import json


class TextDecorator(object):
    RESET = '\033[0m'
    BOLD = '\033[1;1m'
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[0;33m'

    def __init__(self, force=False):
        self.force = force
        self.has_tty = (hasattr(sys.stdout, 'fileno') and
                        os.isatty(sys.stdout.fileno()))

    def ansi(self, code, text):
        if not self.has_tty and not self.force:
            return text
        return code + text + self.RESET

    def bold(self, text):
        return self.ansi(self.BOLD, text)

    def yellow(self, text):
        return self.ansi(self.YELLOW, text)

    def green(self, text):
        return self.ansi(self.GREEN, text)

    def red(self, text):
        return self.ansi(self.RED, text)


class Formatter(logging.Formatter):
    """Custom formatter to allow a custom output format per level"""

    debug_fmt  = 'debug: %(module)s:%(lineno)d: %(msg)s'
    warn_fmt = 'warning: %(message)s'
    error_fmt  = 'error: %(message)s'
    info_fmt = '%(message)s'

    def __init__(self, fmt='%(levelno)s: %(msg)s'):
        logging.Formatter.__init__(self, fmt)

    def format(self, record):
        # Save the original format configured by the user
        # when the logger formatter was instantiated
        orig_fmt = self._fmt

        # Replace the original format with one customized by logging level
        if record.levelno == logging.DEBUG:
            self._fmt = self.debug_fmt

        elif record.levelno == logging.INFO:
            self._fmt = self.info_fmt

        elif record.levelno == logging.ERROR:
            self._fmt = self.error_fmt

        elif record.levelno == logging.WARN:
            self._fmt = self.warn_fmt

        # Call the original formatter class to do the grunt work
        result = super(Formatter, self).format(record)

        # Restore the original format configured by the user
        self._fmt = orig_fmt

        return result


class ConsoleHandler(logging.StreamHandler):
    """Pass logging.INFO to stdout, everything else to stderr"""

    def __init__(self, combine_stderr=False):
        logging.StreamHandler.__init__(self)
        self.stream = None
        self.combine_stderr = combine_stderr

    def emit(self, record):
        if self.combine_stderr:
            # Writing to stderr from within a test results in console noise
            # so force everything to stdout.  This means that we get good
            # debugging messages when something goes wrong since nose
            # captures stdout and only prints it when a test fails.
            self.stream = sys.stdout
        elif record.levelno == logging.INFO:
            self.stream = sys.stdout
        else:
            self.stream = sys.stderr
        logging.StreamHandler.emit(self, record)

    def flush(self):
        if (self.stream and hasattr(self.stream, 'flush') and
                not self.stream.closed):
            logging.StreamHandler.flush(self)


class Logger(object):

    def __init__(self, name):
        self.logger = logging.getLogger(name)
        self.debug = self.logger.debug
        self.error = self.logger.error
        self.info = self.logger.info
        self.warning = self.logger.warning

    def traceback(self):
        tb = sys.exc_info()[2]
        self.error(traceback.format_exc(tb))

    def json(self, obj, **kwargs):
        self.debug(json.dumps(obj, **kwargs)+'\n')

    def pprint(self, obj):
        for line in pprint.pformat(obj).splitlines():
            self.debug(line)

    def trace(self, msg, depth=1):
        self.debug(('+' * depth) + ' ' + msg)


def decorator(force=False):
    """Return a text decorator"""
    return TextDecorator(force=force)


def logger(name=None):
    """Return a module-scope logger"""
    # Get the caller's module and use its name
    if name is None:
        stack = inspect.stack()
        module = inspect.getmodule(stack[1][0])
        if hasattr(module, '__name__'):
            name = module.__name__

    return Logger(name)


def init(verbose, combine_stderr=False):
    """Initialize logging

    :param verbose: Enables debugging output

    """
    if verbose:
        level = logging.DEBUG
    else:
        level = logging.INFO

    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # Initialize the root logger
    console_handler = ConsoleHandler(combine_stderr=combine_stderr)
    console_handler.setFormatter(Formatter())
    root_logger.addHandler(console_handler)
