"""Use the stanford parser to generate a parse trees etc.  This
is pretty hacky, and just ammounts to running a java command and piping
things back into python, but thursday is pretty close so what can I do?
"""
import os
from subprocess import Popen, PIPE, STDOUT
from nltk.tree import ParentedTree


def _standford_parser_cmd(format='oneline'):
    parser_dir = os.path.realpath(os.path.join("contrib", "stanford-parser"))
    cmd_parts = ('java', '-mx150m', '-cp', parser_dir + "/*:",
                 'edu.stanford.nlp.parser.lexparser.LexicalizedParser',
                 '-outputFormat', format,
                 'edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz',
                 '-')
    return cmd_parts


def _exec_cmd(cmd, input):
    p = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    response = p.communicate(input=input)[0]
    return response


def parse(sentence, use_cache=True):
    response = _exec_cmd(_standford_parser_cmd(), sentence)

    # throw away the garbgage we don't want from the parser's response.
    # this could probably get us in trouble since it'll hide errors etc,
    # but we got deadlines....
    trees = [ParentedTree.parse(line) for line in response.split("\n") if len(line) > 2 and line[0] == "(" and line[-1] == ")"]
    return trees


def dependences(sentence, use_cache=True):
    import re

    if not hasattr(dependences, '_dep_regex'):
        dependences._dep_regex = re.compile(r'(?P<dep_name>.*?)\((?P<first_word>.*?)-(?P<first_loc>\d+), (?P<second_word>.*?)-(?P<second_loc>\d+)\)')

    response = _exec_cmd(_standford_parser_cmd(format='typedDependenciesCollapsed'), sentence)
    deps = response.split("\n")[3:-4]
    matches = []
    for dep in deps:
        a_match = dependences._dep_regex.search(dep)
        if a_match:
            matches.append(a_match.groupdict())
    return matches
