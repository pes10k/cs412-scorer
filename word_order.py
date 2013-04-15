import stanford_parser
import nltk
import essay_utils


def np_vp_order_check(tree):
    wrong = 0
    print tree
    for st in tree.subtrees():
        try:
            node_1 = st[0]
            node_2 = st[1]
            # print "Comparing Nodes (%s, %s)" % (node_1.node, node_2.node)
            if node_1.node == "VP" and node_2.node == "NP":
                wrong += 1
        except IndexError:
            pass
    return wrong

essay_index = 13
for essay in [essay_utils.essays[essay_index]]:
    essay_index += 1
    print "Parsing Essay %d" % (essay_index,)

    line_index = 0
    for line in essay:
        line_index += 1

        print " - Checking line %d" % (line_index,)
        parse_text = stanford_parser.parse(line)
        # print " - Tagging: %s" % (parse_text,)

        try:
            tree = nltk.Tree.parse(parse_text)
            print " --- Num Wrong: %d" % (np_vp_order_check(tree),)
        except ValueError, e:
            print " * Parsing Error"
            print " * Line: %s" % (line,)
            print " * Error: %s" % (e.message,)
            print " * Args: %s" % (str(e.args),)
