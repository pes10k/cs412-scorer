"""Use the stanford parser to generate a parse trees etc.  This
is pretty hacky, and just ammounts to running a java command and piping
things back into python, but thursday is pretty close so what can I do?
"""
import os
from subprocess import Popen, PIPE, STDOUT
from nltk.tree import ParentedTree
import cPickle as pickle


def _standford_parser_cmd():
    parser_dir = os.path.realpath(os.path.join("contrib", "stanford-parser"))
    cmd_parts = ('java', '-mx150m', '-cp', parser_dir + "/*:",
                 'edu.stanford.nlp.parser.lexparser.LexicalizedParser',
                 '-outputFormat', 'oneline',
                 'edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz',
                 '-')
    return cmd_parts


def parse(sentence):
    p = Popen(_standford_parser_cmd(), stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    response = p.communicate(input=sentence)[0]

    # throw away the garbgage we don't want from the parser's response.
    # this could probably get us in trouble since it'll hide errors etc,
    # but we got deadlines....
    trees = [ParentedTree.parse(line) for line in response.split("\n") if len(line) > 2 and line[0] == "(" and line[-1] == ")"]
    return trees


_parser_cache = dict(
    cache=dict()
)


def cache_get(key):
    try:
        return _parser_cache['cache'][key]
    except KeyError:
        try:
            file_name = 'stanford_parses.data'
            f_read = open(os.path.join('cache', file_name), 'r')
            data = pickle.load(f_read)
            _parser_cache['cache'] = data
            f_read.close()
        except (IOError, KeyError):
            return False


def cache_set(cache_key, cache_value):
    _parser_cache['cache']
    file_name = 'stanford_parses.data'

    if cache_key in _parser_cache['cache'] and _parser_cache['cache'][cache_key] == cache_value:
        return False
    try:
        f = open(os.path.join('cache', file_name), 'r')
        data = pickle.load(f)
        data[cache_key] = cache_value
        _parser_cache['cache'][cache_key] = cache_value
        f.close()

        f_write = open(os.path.join('cache', file_name), 'wb')
        pickle.dump(data, f_write)
        f_write.close()
    except (IOError, EOFError):
        f = open(os.path.join('cache', file_name), 'w')
        data = {}
        data[cache_key] = cache_value
        _parser_cache['cache'][cache_key] = cache_value
        pickle.dump(data, f)
        f.close()
