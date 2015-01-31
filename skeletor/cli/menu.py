from skeletor.core import log


class Menu(object):
    """Display and interact with a callback-based menu"""

    QUIT = 'quit'

    def __init__(self, title,
                 prompt='? ',
                 errormsg='invalid response, please try again',
                 fmt='%(key)s ... %(description)s',
                 underline='=',
                 get_input=None,
                 logger=None,
                 logger_name=None,
                 case_sensitive=False,
                 args=None,
                 kwargs=None):
        """Construct a menu

        :param title: menu title
        :param prompt: input prompt
        :param errormsg: error message to display when an invalid option is chosen
        :param get_input: :func:`func(str)` that returns a :class:`str` choice
        :param case_sensitive: makes responses case sensitive, otherwise Q == q.

        """
        self.title = title
        self.prompt = prompt
        self.errormsg = errormsg
        self.fmt = fmt
        self.underline = underline
        self.get_input = get_input or raw_input
        self.logger = logger or log.logger(logger_name or __name__)
        self.case_sensitive = case_sensitive
        #: Allows callbacks to accept custom arguments
        self.args = args or ()
        #: Allows callbacks to accept custom keyword arguments
        self.kwargs = kwargs or {}

    def present(self, options):
        """Present a menu of options

        :param options: a tuple of `(option, (description, callback))`
                        where `options` is a string that is expected to be
                        returned get_input, `description` is a description of
                        the options, and `callback` is either a callable or
                        :obj:`Menu.QUIT` to signify exiting the menu.

        e.g.

        .. sourcecode:: python

            from skeletor.core import log
            from skeletor.cli.menu import Menu

            log.init(True)

            def hello():
                print('oh hai')

            options = (
                ('c', ('say hello', hello)),
                ('q', ('quit', Menu.QUIT)),
            )
            Menu('example menu').present(options)

        """
        options_dict = dict(options)
        logger = self.logger
        title = self.title
        underline = self.underline

        while True:
            if title:
                logger.info(title)
            if underline:
                logger.info(underline * len(title))

            for key, (description , callback) in options:
                logger.info(self.fmt % dict(key=key, description=description))

            answer = self.get_input(self.prompt)
            idx = answer.strip()
            if not self.case_sensitive:
                idx = idx.lower()
            try:
                callback = options_dict[idx][1]
            except:
                logger.error(self.errormsg)
                continue

            logger.info('')
            if callback == self.QUIT:
                break
            callback(*self.args, **self.kwargs)
            logger.info('')


def confirm(user_msg, default=True, empty_chooses=True, get_input=None):
    """Confirm an action with a prompt

    :param user_msg: the text to display.
    :param default: the value to return when no input is given.
    :param empty_chooses: when True, empty values choose the default.
    :returns bool: whether "yes" was chosen.

    """
    if get_input is None:
        get_input = raw_input
    result = ''
    msg = user_msg + ' ' + (default and '[Y/n]' or '[y/N]') + '? '
    while result not in ('y', 'yes', 'n', 'no'):
        result = get_input(msg).lower()
        if empty_chooses and not result:
            return default

    return result in ('y', 'yes')
