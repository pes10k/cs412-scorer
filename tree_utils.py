from tag_utils import simple_tag, is_valid_tag, simplify_tags


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
