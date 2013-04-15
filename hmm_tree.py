import hmm_utils
import essay_utils
import cmd_utils
import stanford_parser
import tree_utils
import grade_utils

# essay_index = int(cmd_utils.cmd_arg('--essay', 0)) - 1
# essay = essay_utils.essays[essay_index]

counts = hmm_utils.get_transition_counts()

i = 0

for essay in essay_utils.essays:

    print "--------------\n"
    print "Scoring Essay: %d" % (i + 1,)
    sentences = 0
    score = 5

    for sentence in essay:
        parse_trees = stanford_parser.parse(sentence)

        for parse_tree in parse_trees:

            print parse_tree.flatten()
            sub_sentences = max(len(list(parse_tree.subtrees(lambda t: t.node == 'S'))), 1)
            sentences += sub_sentences
            print " -- Sentence Guess: %d" % (sub_sentences,)
            transitions = tree_utils.transitions_in_tree(parse_tree)
            sentence_probs = []
            change = 0
            for transition in transitions:
                try:
                    probs = hmm_utils.prob_of_all_transitions(transition, counts, gram_size=3)
                    # print "%s -> %s" % (transition, probs)
                    sentence_probs += probs
                    change += len([prob for prob in probs if prob < 0.01])

                except KeyError:
                    print " -- Got Bad Value"
                    change += 2
            # print " -- effect: -%d" % (change,)
            score -= change

    print " -- %s" % (str(sentence_probs),)
    print " -- AVG: %f" % (sum(probs)/len(probs),)
    print " -- Sentences: %d (score: %f)" % (sentences, grade_utils.grades[i][-2])
    print " -- got %f vs. %f" % (score, grade_utils.grades[i][0])
    i += 1
