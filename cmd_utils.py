import sys


def log(line, level=0, sep=' -- '):
    if cmd_log_level() is not None and cmd_log_level() >= level:
        print "%s %s" % (sep * level, line)


def get_stdin():
    lines = list(sys.stdin)
    return "\n".join([l.strip() for l in lines])


def get_stdin_lines():
    return [l for l in get_stdin().split("\n") if l and len(l) > 0]


def cmd_flag(name, default=None):
    return name in sys.argv


def cmd_arg(name, default=None):
    try:
        return sys.argv[sys.argv.index(name) + 1]
    except (ValueError, IndexError):
        return default


def cmd_test():
    if not hasattr(cmd_test, '_test_cmd_arg'):
        cmd_test._test_cmd_arg = cmd_arg('--test', None)
    return cmd_test._test_cmd_arg


def cmd_log_level():
    if not hasattr(cmd_log_level, '_log_level'):
        cmd_log_level._log_level = int(cmd_arg('--log', 0))
    return cmd_log_level._log_level


def cmd_essay_index():
    if not hasattr(cmd_essay_index, '_essay_index'):
        cmd_essay_index._essay_index = int(cmd_arg('--essay', 0)) - 1
    return cmd_essay_index._essay_index

