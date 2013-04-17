import hmm_utils
import cmd_utils
import stanford_parser

counts = hmm_utils.get_transition_counts()

parse_stdin = cmd_utils.cmd_flag('--parse', None)
score_stdin = cmd_utils.cmd_flag('--score', None)
transition_count = cmd_utils.cmd_arg('--count', None)
transition_prob = cmd_utils.cmd_arg('--prob', None)

if score_stdin or parse_stdin:
    import tree_utils

    trees = stanford_parser.parse(cmd_utils.get_stdin())

    for tree in trees:
        print tree
        if score_stdin:
            sentence_transitions = tree_utils.transitions_in_tree(tree)
            sentence_probs = []
            for transition in sentence_transitions:
                print "Transitions: %s" % (transition)
                probs = hmm_utils.prob_of_all_transitions(transition, counts, gram_size=3)
                print "Probs: %s" % (probs)
                sentence_probs += probs
            total = 1
            for prob in sentence_probs:
                total *= prob
            print "Total: %f" % (total,)

elif transition_count:
    print "Count: %d" % (counts[transition_count],)
elif transition_prob:
    transitions = transition_prob.split("@")
    bottom = counts["@".join(transitions[:-1])]
    top = counts[transition_prob]
    print "Prob: (%d/%d) -> %f" % (top, bottom, float(top)/bottom)
else:
    print "Error: Nothing to test"
