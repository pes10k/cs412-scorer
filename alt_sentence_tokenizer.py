import essay_utils
import stanford_parser
import cmd_utils

essay_index = int(cmd_utils.cmd_arg('--essay', 1)) - 1

correct_answers = []

essay = essay_utils.essays[essay_index]

for line in essay:
    print "-----"
    print line
    parse_trees = stanford_parser.parse(line)
    for parse_tree in parse_trees:
        print parse_tree



