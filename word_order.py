import stanford_parser
import essay_utils
import tree_utils
import hmm_utils
from cmd_utils import cmd_essay_index
from sentence_tokenizer import parse_sentences
from pprint import pprint


correct_scores = (
    (0, 0, 0, 0, 0, 0, 0,),
)


counts = hmm_utils.get_transition_counts()


def tags_appear_in_order(haystack, needles):
    needle_len = len(needles)
    for i in range(0, len(haystack) - needle_len + 1):
        if haystack[i] == needles[0]:
            if needles[1] in haystack[i+1:]:
                return True
    return False


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
    sub_trees = list(tree.subtrees(lambda x: x.node in sub_tree_nodes))
    num_errors = 0
    if len(sub_trees) > 0:
        num_tags = len(tags)
        for a_tree in sub_trees:
            sub_trees_nodes = list([t.node for t in a_tree])
            # print sub_tree_nodes
            # print sub_trees_nodes
            num_missing_tags = sum([0 if tags[i] in sub_trees_nodes else 1 for i in range(0, num_tags)])
            if num_missing_tags == 0 and tags_appear_in_order(sub_trees_nodes, tags):
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


def num_order_issues(sentence):
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
    tree = stanford_parser.parse(sentence)[0]
    print tree

    tree_utils.simplify_tree(tree, trim_adjecent_prop_nouns=True,
                             normalize_sent_roots=True,
                             normalize_plural=True,
                             normalize_case=True)
    print sentence
    print tree
    problem_counts = []
    problem_counts += ["VP->NP in S"] * num_forbidden_orders(tree, ("S",), ('VP', 'NP'))
    problem_counts += ["NP->VP in SINV"] * num_forbidden_orders(tree, ('SINV',), ('NP', 'VP'))
    problem_counts += ["NN->JJ in NP"] * num_forbidden_orders(tree, ('NP',), ('NN', 'JP'))

    problem_counts += ["PP->VB in VP"] * num_forbidden_orders(tree, ('VP',), ('PP', 'VB'))
    problem_counts += ["NP->VP in VP"] * num_forbidden_orders(tree, ('VP',), ('NP', 'VP'))

    problem_counts += ["S->VP in S"] * num_forbidden_orders(tree, ('S',), ('S', 'VP'))

    problem_counts += ["S->VB in VP"] * num_forbidden_orders(tree, ('VP',), ('S', 'VB'))
    # problem_counts += ["VB->VP in VP"] * num_forbidden_orders(tree, ('VP',), ('VB', 'VP'))


    problem_counts += ["NP->RBR in ADVP"] * num_forbidden_orders(tree, ('ADVP',), ('NP', 'RBR'))
    problem_counts += ["NN->DT in NP"] * num_forbidden_orders(tree, ('NP',), ('NN', 'DT'))
    problem_counts += ["NNP->DT in NP"] * num_forbidden_orders(tree, ('NP',), ('NNP', 'DT'))
    problem_counts += ["NN->CD in NP"] * num_forbidden_orders(tree, ('NP',), ('NN', 'CD'))
    problem_counts += ["NNP->CD in NP"] * num_forbidden_orders(tree, ('NP',), ('NNP', 'CD'))

    problem_counts += ['PP->NP in S'] * num_forbidden_orders(tree, ('S',), ('PP', 'NP'))

    return problem_counts


def transition_stats(sentence):
    """Calculates HMM based probabilities base on the transitions in the parse
    tree"""
    sentence_tree = stanford_parser.parse(sentence)[0]
    tree_utils.simplify_tree(sentence_tree, trim_adjecent_prop_nouns=True,
                             normalize_sent_roots=True)
    transitions = tree_utils.transitions_in_tree(sentence_tree)

    product = 1
    probs = []
    for transition in transitions:
        transition_probs = hmm_utils.prob_of_all_transitions(transition, counts, gram_size=3)
        for a_prob in transition_probs:
            product *= a_prob
            probs.append(a_prob)

    stats = dict(
        min=min(probs),
        avg=sum(probs)/len(probs),
        prod=product
    )
    return stats


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

if __name__ == "__main__":

    essay_index = cmd_essay_index()
    for essay in [essay_utils.essays[essay_index]]:
        for line in essay:
            for sentence in parse_sentences(line):
                print num_order_issues(sentence)
