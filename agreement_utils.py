import sentence_tokenizer
import stanford_parser
import tree_utils
from cmd_utils import log


singluar_noun_tags = ('NN', 'NNP')
plural_noun_tags = ('NNS', 'NNPS')
# We manually disambiguate Pronouns
noun_tags = singluar_noun_tags + plural_noun_tags + ('PRP',)

plural_verb_tags = ('VBZ',)
singular_verb_tags = ('VBP',)
verb_tags = singular_verb_tags + plural_verb_tags

plural_prop_nouns = ('they', 'we', 'them', 'themselves', 'us', 'those')
singluar_prop_nouns = ('he', 'she', 'i', 'him', 'me', 'myself', 'it')


def check_node_agreement(tree_one, tree_two):

    # First determine which node is the noun node
    if tree_one.node in noun_tags:
        noun_tree, verb_tree = tree_one, tree_two
    else:
        verb_tree, noun_tree = tree_one, tree_two

    if noun_tree.node in singluar_noun_tags:
        noun_3rd_person = True
        noun_singular = True
    elif noun_tree.node in plural_noun_tags:
        noun_3rd_person = True
        noun_singular = False
    # In pronoun siutation and need to disambiguate
    elif noun_tree.node == "PRP":
        noun_3rd_person = not is_pronoun_first_person(noun_tree)
        noun_singular = is_pronoun_singluar(noun_tree)
    else:
        # Something wrong happened
        raise Exception("No noun tree in this agreement pair!")

    commanding_verb_tree = find_commanding_verb_tree(verb_tree)

    if commanding_verb_tree.node in singular_verb_tags:
        verb_singular = True
    elif commanding_verb_tree.node in plural_verb_tags:
        verb_singular = False
    else:
        raise Exception("No verb in this agrement pair!")

    log("Noun: Looks like %s is %s (%s)" % (noun_tree[0], 'Singular' if noun_singular else 'Plural', "3rd" if noun_3rd_person else "1st"), 2)
    log("Verb: Looks like %s is %s" % (commanding_verb_tree[0], 'Singular' if verb_singular else 'Plural'), 2)

    noun_1st_person = not noun_3rd_person
    is_vbp = commanding_verb_tree.node == "VBP"
    is_vbz = commanding_verb_tree.node == "VBZ"

    if noun_singular and noun_1st_person and is_vbp:
        return True
    elif noun_singular and noun_3rd_person and is_vbz:
        return True
    elif not noun_singular and noun_3rd_person and is_vbp:
        return True
    else:
        log("DONT LIKE COMBO: %s" % ({"verb_tag": commanding_verb_tree.node, "noun_1st_person": noun_1st_person, "noun_singular": noun_singular},), 2)
        return False


def find_commanding_verb_tree(tree):
    if tree.node in verb_tags:
        return tree
    else:
        parent_node = tree.parent()
        if not parent_node:
            return None
        else:
            for sibling in parent_node:
                if sibling.node in verb_tags:
                    return sibling
                elif sibling.node == "VP":
                    return list(sibling.subtrees(lambda x: x.node in verb_tags))[0]
            return find_commanding_verb_tree(parent_node)


def is_pronoun_first_person(tree):
    prop_noun = tree.leaves()[0].lower()
    return prop_noun == "i"


def is_pronoun_singluar(tree):
    prop_noun = tree.leaves()[0].lower()
    return prop_noun in singluar_prop_nouns


def is_sentence_root(tree):
    if not tree.node in tree_utils.semi_tree_roots:
        return False
    else:
        child_nodes = [c.node for c in tree]
        return "NP" in child_nodes and "VP" in child_nodes


def shallowest_noun_in_tree(tree):
    tree.subtrees(lambda x: x.node == "NN" or x.node == "NNS")


def node_in_tree(tree, value):
    subtrees = list(tree.subtrees(lambda x: value in x))
    return subtrees[0] if len(subtrees) > 0 else None


def parse(text, use_cache=False):
    lines = text.split("\n")
    for line in lines:
        sentences = sentence_tokenizer.parse(line, use_cache=True)
        for sentence in sentences:
            log("Looking for Sub-Verb agreement in '%s'" % (sentence,), 1)
            tree = stanford_parser.parse(sentence)[0]
            dependencies = stanford_parser.dependences(sentence)
            sub_verb_deps = [dep for dep in dependencies if dep['dep_name'] == 'nsubj']

            if len(sub_verb_deps) == 0:
                log("Couldn't find Subject-Verb dependency info", 1)
                continue

            for sub_verb in sub_verb_deps:
                first_node = node_in_tree(tree, sub_verb['first_word'])
                sec_node = node_in_tree(tree, sub_verb['second_word'])
                if first_node and sec_node:

                    log("First Dep Node: %s" % (first_node,), 2)
                    log("Sec Dep Node: %s" % (sec_node,), 2)

                    try:
                        is_agreement = check_node_agreement(first_node, sec_node)
                        log("Agreement in sentence? %s" % (is_agreement,), 1)
                    except Exception as e:
                        log("Error looking for agreement? %s" % (e.message,), 1)

                        # No agreement in pair.  Not sure how to handle.
                        # More exhaustive search?
