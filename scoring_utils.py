"""Very simple command line interface for testing specific parts of this
package's functionality"""

import hmm_utils
import cmd_utils
import parsers

counts = hmm_utils.get_transition_counts()

# Flags that note that incode should be looked for in STDIN instead of
# in a test essay file
final_score_stdin = cmd_utils.cmd_flag('--final-score', None)
parse_stdin = cmd_utils.cmd_flag('--parse', None)
score_stdin = cmd_utils.cmd_flag('--score', None)
pronoun_stdin = cmd_utils.cmd_flag('--pronoun', None)
syntactic_formation_stdin = cmd_utils.cmd_flag('--syn-formation', None)
agreement_stdin = cmd_utils.cmd_flag('--agree', None)
sentence_parse_stdin = cmd_utils.cmd_flag('--sen-token', None)
word_order_parse_stdin = cmd_utils.cmd_flag('--word-order', None)


transition_count = cmd_utils.cmd_arg('--count', None)
transition_prob = cmd_utils.cmd_arg('--prob', None)


if score_stdin or parse_stdin:
    import tree_utils
    trees = parsers.parse(cmd_utils.get_stdin())
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
elif sentence_parse_stdin:
    import sentence_tokenizer
    sentences = sentence_tokenizer.parse_sentences(cmd_utils.get_stdin(), use_cache=False)
    print sentences
elif word_order_parse_stdin:
    import sentence_tokenizer
    import word_order
    lines = cmd_utils.get_stdin_lines()
    issues_in_text = []
    for line in lines:
        sentences = sentence_tokenizer.parse_sentences(line)
        for sentence in sentences:
            issues = word_order.issues_in_sentence(sentence, use_cache=False)
            print sentence
            print issues
            issues_in_text += issues
    print "Found %d issues" % (len(issues_in_text),)
    print "Issues: %s" % (issues_in_text,)
elif syntactic_formation_stdin:
    import syntactic_formation
    import math
    text = cmd_utils.get_stdin().strip()
    sentence_problems = syntactic_formation.parse(text)
    num_sentences_with_problems = sum([1 if count > 0 else 0 for count in sentence_problems])
    num_sentences = len(sentence_problems)
    print "Num Sentences: {0}".format(num_sentences)
    print "Num Problems: {0}".format(sum(sentence_problems))
    print "Sentences with problems: {0}".format(num_sentences_with_problems)
    print "Percent Correct: {0}/{1} ({2})".format(num_sentences - num_sentences_with_problems, num_sentences, 1 - (float(num_sentences_with_problems)/num_sentences))
    print "Score: {0}".format(math.floor((1 - (float(num_sentences_with_problems)/num_sentences)) * 5))
elif agreement_stdin:
    import agreement_utils
    text = cmd_utils.get_stdin().strip()
    print agreement_utils.parse(text)
elif pronoun_stdin:
    import text_coherence
    text = cmd_utils.get_stdin().strip()
    print text_coherence.parse(text)
elif final_score_stdin:
    import grade_utils
    text = cmd_utils.get_stdin().strip()

    print "Grading"
    print "----------"
    print text
    print "----------\n"
    for grade_type in grade_utils.implemented_grades:
        grade_for_test = grade_utils.grade_text(text, grade_type)
        if isinstance(grade_for_test, str):
            print "%s: %s" % (grade_type, grade_for_test)
        else:
            print "%s: %d" % (grade_type, grade_for_test)
    print "\n"
elif transition_count:
    print "Count: %d" % (counts[transition_count],)
elif transition_prob:
    transitions = transition_prob.split("@")
    bottom = counts["@".join(transitions[:-1])]
    top = counts[transition_prob]
    print "Prob: (%d/%d) -> %f" % (top, bottom, float(top)/bottom)
else:
    print "Error: Nothing to test"
