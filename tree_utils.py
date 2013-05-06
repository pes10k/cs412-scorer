from tag_utils import simple_tag, is_valid_tag, simplify_tags
from cmd_utils import log

semi_tree_roots = ('SINV', 'S', 'FRAG', 'X')


def child_tags(tree):
    return [subtree.node for subtree in tree]


def nearest_root(tree):
    if tree.parent().node == "ROOT":
        return None
    elif tree.parent().node in semi_tree_roots:
        return tree.parent().node
    else:
        return nearest_root(tree.parent())


def simplify_tree(tree, remove_starting_cc=False, trim_adjecent_prop_nouns=False,
                  normalize_sent_roots=False, normalize_case=False,
                  normalize_plural=False,
                  collapse_redundant_sbar=True):
    """Do some transformations on a parse tree to normalize it.  Currently:
        - Remove CD when they're paired with a noun
        - Stripping off conjunction from the beginning of the sentence / root
        of the tree
        - Remove proper nouns that are next to each other
    """
    if normalize_plural:
        plural_transforms = dict(
            NNS='NN',
            NNPS='NNP',
        )
        for a_tree in tree.subtrees(lambda x: x.node in plural_transforms):
            a_tree.node = plural_transforms[a_tree.node]

    if normalize_case:
        case_transforms = dict(
            VBD='VB',
            VBG='VB',
            VBN='VB',
            VBP='VB',
            VBZ='VB'
        )
        for a_tree in tree.subtrees(lambda x: x.node in case_transforms):
            a_tree.node = case_transforms[a_tree.node]

    if normalize_sent_roots:
        for a_tree in tree.subtrees(lambda x: x.node in semi_tree_roots):
            a_tree.node = "S"

    if trim_adjecent_prop_nouns:
        np_trees = list(tree.subtrees(lambda x: x.node == "NP"))
        if len(np_trees) > 0:
            for np_tree in np_trees:
                num_leaves = len(np_tree)
                change = False
                if num_leaves >= 2:
                    for i in range(0, num_leaves - 1):
                        if not change:
                            if np_tree[i].node == "NNP" and np_tree[i + 1].node == "NNP":
                                np_tree.remove(np_tree[i + 1])
                                change = True

    if remove_starting_cc:
        useful_roots = list(tree.subtrees(lambda x: x.node in semi_tree_roots))
        if len(useful_roots) > 0:
            useful_root = useful_roots[0]
            if useful_root[0].node == "CC":
                useful_root.remove(useful_root[0])
                log("REMOVED CC from start of sentence", 2)

    cd_trees = tree.subtrees(lambda x: x.node == "CD")
    for cd_tree in cd_trees:
        parent_node = cd_tree.parent()
        if parent_node.node == "NP":
            parent_node_children = [parent_node[i].node for i in range(0, len(parent_node))]
            if "CD" in parent_node_children and ("NN" in parent_node_children or "NNS" in parent_node_children):
                parent_node.remove(cd_tree)
                log("REMOVED only child CD node", 2)

    if collapse_redundant_sbar:
        for sbar_tree in tree.subtrees(lambda x: x.node == 'SBAR'):
            if len(sbar_tree) == 1 and sbar_tree[0].node in semi_tree_roots:
                sbar_child = sbar_tree[0]
                sbar_parent = sbar_tree.parent()
                index = sbar_parent.index(sbar_tree)
                sbar_parent.remove(sbar_tree)
                sbar_tree.remove(sbar_child)
                sbar_parent.insert(index, sbar_child)
                log("Collapsed SBAR", 2)


def lexical_rules(tree, cutoff=0):
    bad_tags = ('X', 'FRAG', 'ROOT')
    rules = dict()
    for subtree in tree.subtrees(lambda x: is_valid_tag(x.node) and len(x) > 0 and x.node.split('-')[0] not in bad_tags):
        productions = [n.node.split('-')[0] for n in subtree if not isinstance(n, str) and is_valid_tag(n.node) and len(subtree) > 0]
        if len(productions) > 0 and len(set(bad_tags).intersection(productions)) == 0:
            prod = (subtree.node.split('-')[0], tuple(productions))
            rules[prod] = rules.get(prod, 0) + 1
    return rules


def transitions_in_tree(tree):
    transitions = []
    for subtree in tree.subtrees():
        num_children = len(subtree)
        children = []
        for c_index in range(0, num_children):
            node = subtree[c_index]

            if node.__class__ == str:
                continue

            simple_node = simple_tag(node.node)
            if is_valid_tag(simple_node):
                children.append(simple_node)
        simplified_transitions = simplify_tags(children)
        if len(simplified_transitions) > 1:
            transitions.append(simplified_transitions)
    return transitions
