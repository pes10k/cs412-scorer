import sentence_tokenizer
from cmd_utils import log
import parsers
import re

pronoun_tags = ('PRP', 'PRP$', 'WP$', 'WP')
pronouns = (
    # first person pronouns
    ('i', 'me', 'my', 'mine', 'myself', 'we', 'us', 'our', 'ours', 'ourselves'),
    # second person pronouns
    ('you', 'your', 'yours', 'yourself', 'you', 'your', 'yours', 'yourselves'),
    # third person pronouns
    ('he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'they', 'them', 'their', 'theirs', 'themselves', 'itself', 'they', 'them', 'their', 'theirs', 'themselves',)
)


def parse(text):
    # Strip numbers out, since that seems to cause problems for my approach
    text = re.sub(r'\d+ ?', 'some ', text)

    sentences = sentence_tokenizer.parse(text)
    sentence_pronouns = []

    for sentence in sentences:
        log("Looking for pronouns in '{0}'".format(sentence), 2)

        pronoun_totals = [[], [], []]
        tree = parsers.parse(sentence)[0]
        pronoun_trees = tree.subtrees(lambda x: x.node in pronoun_tags)
        for pronoun_tree in pronoun_trees:
            # First total up all the first person pronouns
            for i in range(3):
                if pronoun_tree[0].lower() in pronouns[i]:
                    pronoun_totals[i].append(pronoun_tree[0])
        log("First Person '{0}'".format(pronoun_totals[0]), 3)
        log("Second Person '{0}'".format(pronoun_totals[1]), 3)
        log("Third Person '{0}'".format(pronoun_totals[2]), 3)
        sentence_pronouns.append(pronoun_totals)

    log("Pronouns found in text: %s" % (sentence_pronouns), 2)

    # If there are 3rd person pronouns in any sentence, we have to decide
    # if they are used correctly.  We do this in the following, very
    # expensive, but possibly correct manner.
    #
    # Start from the top down
    #   1. Look back 2 sentences and see if we can find a refernece.
    #       IF NOT - its an error and do no more
    #   2. If so, replace the refereneced word with "RUNNING"
    #      and search again, to see if there is a previous word it could refer
    #      to.
    #       IF NOT, its correct.  Replace the pronoun with the referenced word
    #       and continue
    #   3. Else, its not felicitous.  Give bad credit
    for i in range(len(sentences)):
        if len(sentence_pronouns[i][2]) > 0:
            pronoun_results = []
            for third_pronoun in sentence_pronouns[i][2]:
                all_sentences = sentences[max(0, i - 2):i + 1]
                norm_sentences = ". ".join([a_sen.strip(".") for a_sen in all_sentences]) + "."
                log("Looking for pronoun coherence for '{0}'".format(norm_sentences), 4)
                pronouns_refs = parsers.parse_coref(norm_sentences)

                log("Recieved co-references {0}".format(pronouns_refs), 5)

                found_bundle = False

                for j in range(len(pronouns_refs)):
                    if third_pronoun == pronouns_refs[j]['pronoun']:
                        found_bundle = pronouns_refs[j]
                        break

                if not found_bundle:
                    log("Found NO anticedent for {0}".format(third_pronoun), 3)
                    pronoun_results.append((third_pronoun, -1))
                else:
                    log("Found anticedent for {0}".format(third_pronoun), 3)
                    ref_index = int(found_bundle['ref_sentence']) - 1 + (i - 2)

                    sentences[ref_index] = sentences[ref_index].replace(found_bundle['ref'], 'RUNNING')
                    log("Replacing '{0}' with 'RUNNING'".format(found_bundle['ref']), 3)

                    altered_sentences = sentences[max(0, i - 2):i + 1]
                    norm_altered_sentences = ". ".join([a_sen.strip(".") for a_sen in altered_sentences]) + "."
                    log("New test sentences are '{0}'".format(norm_altered_sentences), 4)
                    altered_pronouns_refs = parsers.parse_coref(norm_altered_sentences)

                    if third_pronoun not in [a_ref['pronoun'] for a_ref in altered_pronouns_refs]:
                        log("Anticedent is unambigious!", 3)

                        pro_index = int(found_bundle['pronoun_sentence']) - 1 + (i - 2)
                        sentences[pro_index] = sentences[pro_index].replace(found_bundle['pronoun'], found_bundle['ref'])

                        pronoun_results.append((third_pronoun, found_bundle['ref']))
                    else:
                        log("Anticedent is ambigious", 3)
                        log("New Sentences: {0}".format(altered_pronouns_refs), 4)
                        pronoun_results.append((third_pronoun, .5))
            sentence_pronouns[i][2] = pronoun_results
    return sentence_pronouns
