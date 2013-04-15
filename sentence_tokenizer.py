import stanford_parser
import tree_utils
import hmm_utils
import essay_utils

counts = hmm_utils.get_transition_counts()


def _possible_sentences_in_line(line, min_sentence_len=3):
    sentences = [[line]]
    words = line.replace(".", "").split()
    num_words = len(words)
    if num_words >= 6:
        sentences += [[" ".join(words[0:i]), " ".join(words[i:])] for i in range(min_sentence_len, num_words - min_sentence_len)]
    return sentences


def prod(nums):
    total = 1
    for num in nums:
        total *= num
    return num


def avg_prob(nums):
    return sum(nums)/len(nums)

essay_index = 0
for essay in essay_utils.essays[2:]:
    essay_index += 1
    print "Working on Essay: %d" % (essay_index,)
    for line in essay:
        print " -- Working on: %s" % (line,)
        all_possible_sentences = _possible_sentences_in_line(line)
        all_possible_sentence_probs = []
        for possible_sentences in all_possible_sentences:
            print " -- -- Examining: %s" % (possible_sentences,)
            prob_for_sentences = []
            for possible_sentence in possible_sentences:
                sentence_tree = stanford_parser.parse(possible_sentence)[0]
                sentence_transitions = tree_utils.transitions_in_tree(sentence_tree)
                sentence_probs = []
                for transition in sentence_transitions:
                    probs = hmm_utils.prob_of_all_transitions(transition, counts, gram_size=3)
                    sentence_probs += probs
                prob_for_sentences.append(prod(sentence_probs))
            print " -- -- %f:" % (avg_prob(prob_for_sentences),)
            all_possible_sentence_probs.append(avg_prob(prob_for_sentences))
        max_prob = max(all_possible_sentence_probs)
        parse_for_max_prob = all_possible_sentences[all_possible_sentence_probs.index(max_prob)]
        print " -- -- MAX Prob: %f" % (max_prob,)
        print " -- -- Parse for max prob: %s" % (parse_for_max_prob,)
        print " -- -- Num Sentences: %d" % (len(parse_for_max_prob),)
        print " -------------"
