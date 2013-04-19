import stanford_parser
import essay_utils
import tree_utils
from cmd_utils import cmd_essay_index, cmd_log_level, log
from sentence_tokenizer import parse_sentences
from cache_utils import cache_get, cache_set


def tags_appear_in_order(haystack, needles):
    indexes = [haystack.index(n) for n in needles if n in haystack]
    return sorted(indexes) == indexes


def num_tag_order_errors(tree, sub_tree_nodes, tags):
    sub_trees = list(tree.subtrees(lambda x: x.node in sub_tree_nodes))
    num_errors = 0
    if len(sub_trees) > 0:
        num_tags = len(tags)
        for a_tree in sub_trees:
            sub_trees_nodes = list([t.node for t in a_tree])
            # print sub_tree_nodes
            # print sub_trees_nodes
            num_missing_tags = sum([0 if tags[i] in sub_trees_nodes else 1 for i in range(0, num_tags)])
            if num_missing_tags == 0 and not tags_appear_in_order(sub_trees_nodes, tags):
                num_errors += 1
    return num_errors


def num_forbidden_orders(tree, sub_tree_nodes, tags):

    # Note that we flag nodes that have mis ordered children, so that we don't
    # double count the same error twice
    sub_trees = list(tree.subtrees(lambda x: x.node in sub_tree_nodes and not hasattr(x, '_has_error')))
    num_errors = 0
    if len(sub_trees) > 0:
        num_tags = len(tags)
        for a_tree in sub_trees:
            sub_trees_nodes = list([t.node for t in a_tree])
            # print sub_tree_nodes
            # print sub_trees_nodes
            num_missing_tags = sum([0 if tags[i] in sub_trees_nodes else 1 for i in range(0, num_tags)])
            if num_missing_tags == 0 and tags_appear_in_order(sub_trees_nodes, tags):

                # Add Flag to not over count errors
                a_tree._has_error = True
                num_errors += 1
    return num_errors


# def tags_appear_in_relative_order(source, tags):
#     """Checks to see if the given tags appear in the expected order.  Tags can
#     be missing, but if they do appear, the must be in the given expected order"""
#     pos_transition_rules = dict(
#         'VP'=[],
#         'NP'=['DT', 'CD', ]
#
# )


def issues_in_sentence(sentence, use_cache=True):
    """'Brute force' check for a bunch of possible word ordering issues.
    Specifically, looking for the following:
        - VP coming before NP in standard sentence
        - NP coming before VP in inverted sentence
        - JJ coming after Nount in NP
        - VB before PP in VP
        - VB before NP in VP
        - VP before S in standard sentence (with embedded sentences)
        - NN before CD in NP
        - NNP before CD in NP
    """
    if use_cache:
        result = cache_get('word_order_issues', sentence)
        if result is not None:
            return result

    tree = stanford_parser.parse(sentence)[0]
    tree_utils.simplify_tree(tree, trim_adjecent_prop_nouns=True,
                             normalize_sent_roots=True,
                             normalize_plural=True,
                             normalize_case=True)

    log("Looking for order issues in: %s" % (sentence,), 1)
    if cmd_log_level() >= 4:
        print "Simplified Parse Tree"
        print tree

    problems = []
    problems += ["VP->NP in S"] * num_forbidden_orders(tree, ("S",), ('VP', 'NP'))
    problems += ["NP->VP in SINV"] * num_forbidden_orders(tree, ('SINV',), ('NP', 'VP'))
    problems += ["NN->JJ in NP"] * num_forbidden_orders(tree, ('NP',), ('NN', 'JP'))

    problems += ["PP->VB in VP"] * num_forbidden_orders(tree, ('VP',), ('PP', 'VB'))
    problems += ["NP->VP in VP"] * num_forbidden_orders(tree, ('VP',), ('NP', 'VP'))

    problems += ["S->VP in S"] * num_forbidden_orders(tree, ('S',), ('S', 'VP'))

    problems += ["S->VB in VP"] * num_forbidden_orders(tree, ('VP',), ('S', 'VB'))
    # problems += ["VB->VP in VP"] * num_forbidden_orders(tree, ('VP',), ('VB', 'VP'))

    problems += ["NP->RBR in ADVP"] * num_forbidden_orders(tree, ('ADVP',), ('NP', 'RBR'))
    problems += ["NN->DT in NP"] * num_forbidden_orders(tree, ('NP',), ('NN', 'DT'))
    problems += ["NNP->DT in NP"] * num_forbidden_orders(tree, ('NP',), ('NNP', 'DT'))
    problems += ["NN->CD in NP"] * num_forbidden_orders(tree, ('NP',), ('NN', 'CD'))
    problems += ["NNP->CD in NP"] * num_forbidden_orders(tree, ('NP',), ('NNP', 'CD'))

    problems += ['PP->NP in S'] * num_forbidden_orders(tree, ('S',), ('PP', 'NP'))

    # Toggle?
    problems += ['NP->VP in NP'] * num_forbidden_orders(tree, ('NP',), ('NP', 'VP'))

    # Seems like it should be VB->ADVP->PP
    problems += ['VB->PP->ADVP in VP'] * num_forbidden_orders(tree, ('VP',), ('VB', 'PP', 'ADVP'))
    problems += ['VB->PP->SBAR in VP'] * num_forbidden_orders(tree, ('VP',), ('VB', 'PP', 'SBAR'))

    problems += ['NP->S in NP'] * num_forbidden_orders(tree, ('NP',), ('NP', 'S'))

    # Seems like the ADJP should be in a NP or somewhere else, not a sibling
    # of a noun phrase
    problems += ['NP->ADJP in S'] * num_forbidden_orders(tree, ('S',), ('NP', 'ADJP'))

    # Last, if there is an S w/ only one child, we call it a word order problem...
    problems += ['Single Child S'] * len(list(tree.subtrees(lambda x: x in tree_utils.semi_tree_roots and len(x) == 1)))

    if tree[0].node not in tree_utils.semi_tree_roots and not hasattr(tree[0], '_has_error'):
        tree[0]._has_error = True
        problems += ['No S Root']

    log("Found %d order issues" % (len(problems),), 1)
    log("Issues: %s", (problems,), 2)

    if use_cache:
        cache_set('word_order_issues', sentence, problems)

    return problems


# def transition_stats(sentence):
#     """Calculates HMM based probabilities base on the transitions in the parse
#     tree"""

#     sentence_tree = stanford_parser.parse(sentence)[0]
#     tree_utils.simplify_tree(sentence_tree, trim_adjecent_prop_nouns=True,
#                              normalize_sent_roots=True)
#     transitions = tree_utils.transitions_in_tree(sentence_tree)

#     product = 1
#     probs = []
#     for transition in transitions:
#         transition_probs = hmm_utils.prob_of_all_transitions(transition, counts, gram_size=3)
#         for a_prob in transition_probs:
#             product *= a_prob
#             probs.append(a_prob)

#     stats = dict(
#         min=min(probs),
#         avg=sum(probs)/len(probs),
#         prod=product
#     )
#     return stats


if __name__ == "__main__":

    essay_index = cmd_essay_index()
    for essay in [essay_utils.essays[essay_index]]:
        issues_in_text = []
        for line in essay:
            issues_in_line = []
            for sentence in parse_sentences(line):
                issues_in_sentence = issues_in_sentence(sentence)
                issues_in_text += issues_in_sentence
                issues_in_line += issues_in_sentence
    print issues_in_text

