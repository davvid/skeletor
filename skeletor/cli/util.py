def confirm(user_msg, default=True):
    msg = user_msg + ' ' + (default and '[Y/n]' or '[y/N]') + '? '
    result = raw_input(msg)
    if not result:
        return default

    return result.lower() in ('y', 'yes')
