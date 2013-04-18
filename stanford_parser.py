"""Use the stanford parser to generate a parse trees etc.  This
is pretty hacky, and just ammounts to running a java command and piping
things back into python, but thursday is pretty close so what can I do?
"""
import os
from subprocess import Popen, PIPE, STDOUT
from nltk.tree import ParentedTree


def _standford_parser_cmd():
    parser_dir = os.path.realpath(os.path.join("contrib", "stanford-parser"))
    cmd_parts = ('java', '-mx150m', '-cp', parser_dir + "/*:",
                 'edu.stanford.nlp.parser.lexparser.LexicalizedParser',
                 '-outputFormat', 'oneline',
                 'edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz',
                 '-')
    return cmd_parts


def parse(sentence, use_cache=True):
    p = Popen(_standford_parser_cmd(), stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    response = p.communicate(input=sentence)[0]

    # throw away the garbgage we don't want from the parser's response.
    # this could probably get us in trouble since it'll hide errors etc,
    # but we got deadlines....
    trees = [ParentedTree.parse(line) for line in response.split("\n") if len(line) > 2 and line[0] == "(" and line[-1] == ")"]
    return trees
