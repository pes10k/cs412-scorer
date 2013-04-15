import hmm_utils
import essay_utils
import cmd_utils
import stanford_parser
import tree_utils

essay_index = int(cmd_utils.cmd_arg('--essay', 0)) - 1
essay = essay_utils.essays[essay_index]

counts = hmm_utils.get_transition_counts()

score = 5

for sentence in essay:
    print "SENTENCE: " + sentence
    parse_tree = stanford_parser.parse(sentence)
    print parse_tree
    transitions = tree_utils.transitions_in_tree(parse_tree)
    sentence_probs = []
    for transition in transitions:
        try:
            probs = hmm_utils.prob_of_all_transitions(transition, counts, gram_size=3)
            print probs
            score -= len([prob for prob in probs if prob < 0.01])
        except KeyError:
            print "Got Bad Value"
            score -= 2

print "score for sentence is %d" % (score,)
