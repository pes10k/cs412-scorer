from tag_utils import simple_tag, is_valid_tag, simplify_tags


def simplify_tree(tree, remove_starting_cc=True):
    """Do some transformations on a parse tree to normalize it.  Currently:
        - Remove CD when they're paired with a noun
        - Stripping off conjunction from the beginning of the sentence / root
        of the tree
    """
    if remove_starting_cc:
        useful_roots = list(tree.subtrees(lambda x: x.node in ('SINV', 'S', 'FRAG', 'X')))
        if len(useful_roots) > 0:
            useful_root = useful_roots[0]
            if useful_root[0].node == "CC":
                useful_root.remove(useful_root[0])
                print "REMOVED CC from start of sentence"

    cd_trees = tree.subtrees(lambda x: x.node == "CD")
    for cd_tree in cd_trees:
        parent_node = cd_tree.parent()
        if parent_node.node == "NP":
            parent_node_children = [parent_node[i].node for i in range(0, len(parent_node))]
            if "CD" in parent_node_children and ("NN" in parent_node_children or "NNS" in parent_node_children):
                parent_node.remove(cd_tree)
                print "REMOVED only child CD node"


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
