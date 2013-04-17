import sys


def get_stdin():
    return "".join(sys.stdin).strip()


def cmd_flag(name, default=None):
    return name in sys.argv


def cmd_arg(name, default=None):
    try:
        return sys.argv[sys.argv.index(name) + 1]
    except (ValueError, IndexError):
        return default
