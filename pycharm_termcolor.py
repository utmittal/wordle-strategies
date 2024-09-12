import termcolor


def colored(*args, **kwargs):
    return termcolor.colored(force_color=True, *args, **kwargs)


def cprint(*args, **kwargs):
    return termcolor.cprint(force_color=True, *args, **kwargs)
