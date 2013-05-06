from tree_utils import nearest_root, child_tags, lexical_rules
import parsers
import sentence_tokenizer
import cmd_utils
import cache_utils
from cmd_utils import log


def num_sbar_problems(tree):
    bad_sbars = tree.subtrees(lambda x: x.node == "SBAR" and (x.parent().node not in ('S', 'SINV', 'VP' or "IN" not in child_tags(x))))

    # Filter out the sbar problems that are already causing tag problems (so we don't double count issues")
    bad_sbar_problems = [a_tree for a_tree in bad_sbars if nearest_root(a_tree.parent()) not in ('FRAG', 'X')]
    return len(bad_sbar_problems)


def num_tag_problems(tree):
    bad_tag_problems = list(tree.subtrees(lambda x: x.node in ('X', 'FRAG') and len(set(child_tags(x)).intersection(('X', 'FRAG'))) == 0))
    num_problems = len(bad_tag_problems)
    return num_problems


def parse(text):
    treebank_rules = get_treebank_rules(cutoff=0)

    sentence_probs = []
    for line in text.split("\n"):
        sentences = sentence_tokenizer.parse(line)

        for sentence in sentences:

            # Add a period to the end of the sentence, which sometimes
            # forces a better parse
            #if sentence[-1] not in ('.', '!', '?'):
#                    sentence += '.'

            parse_trees = parsers.parse(sentence)
            for tree in parse_trees:
                if cmd_utils.cmd_log_level() > 2:
                    print tree.pprint()

                evindenced_lexical_rules = set(lexical_rules(tree).keys())
                differences = evindenced_lexical_rules.difference(treebank_rules)

                bad_generations = len(differences)
                log("Found {0} bad generations ({1})".format(bad_generations, differences), 3)

                #bad_parse_prob = 1 if prob == 0 else 0
                #log("Scored {0} for prob {1}".format(bad_parse_prob, prob), 3)

                bad_tag_problems = num_tag_problems(tree)
                log("Found {0} X or FRAG tags".format(bad_tag_problems), 3)

                bad_sbar_problems = num_sbar_problems(tree)
                log("Found {0} bad SBAR issues".format(bad_sbar_problems), 3)

                total_problems = bad_sbar_problems + bad_tag_problems + bad_generations
                log("In '{0}'".format(sentence), 2)
                log("Found {0} sentence formation problems".format(total_problems), 1)
                sentence_probs.append(total_problems)
    return sentence_probs


def get_treebank_rules(cutoff=0, include_counts=False):
    all_rules = cache_utils.cache_get('treebank_rules', 'rules')
    if not all_rules:
        log('Generating lexical rules from Penn Treebank', 4)
        from nltk.corpus import treebank
        all_rules = dict()
        for tree in treebank.parsed_sents():
            for rule, count in lexical_rules(tree).items():
                all_rules[rule] = all_rules.get(rule, 0) + count

        cache_utils.cache_set('treebank_rules', 'rules', all_rules)

    if include_counts:
        return {k: v for (k, v) in all_rules.items() if v > cutoff}
    else:
        rules_set = set([rule for rule, count in all_rules.items() if count > cutoff])
        return rules_set
