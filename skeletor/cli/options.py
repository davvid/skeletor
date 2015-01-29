def verbose(parser, options=('-v', '--verbose'), help='increase verbosity'):
    """Add -v and --verbose options to an ArgumentParser

    :param parser: an argparse.ArgumentParser instance
    :param options: overrides the default `-v, --verbose` options.
    :param help: overrides the default help text.

    """
    parser.add_argument(help=help, default=False, action='store_true', *options)
