import sys
from tag_utils import get_cached_counts, prune_tags, simplify_tags, sub_tags_in_list, serialize_tags
from essay_utils import essay_sentences, essay_sent_tags, essay_sent
from hmm_utils import trim_starts


def cmd_arg(name):
    try:
        return sys.argv[sys.argv.index(name) + 1]
    except (ValueError, IndexError):
        return None

brown_tag_counts = get_cached_counts('simple_tag_counts.data', lambda x: prune_tags(simplify_tags(x)))
gram_size = 2
test_essay_index = cmd_arg('--essay') or 0
essay_probs = []

for sent_index in range(0, len(essay_sentences(test_essay_index))):

    test_tags = simplify_tags(prune_tags(essay_sent_tags(test_essay_index, sent_index)))
    test_sent = essay_sent(test_essay_index, sent_index)

    print test_sent
    print test_tags
    sent_probs = []

    for i in range(0, len(test_tags)):
        test_sub_tags = sub_tags_in_list(test_tags, end=i, size=gram_size)
        test_sub_tags = trim_starts(test_sub_tags)
        tag_str = serialize_tags(test_sub_tags)
        sub_tag_str = serialize_tags(test_sub_tags[:-1])
        prob = float(brown_tag_counts[tag_str]) / brown_tag_counts[sub_tag_str]
        sent_probs.append(prob)
        print "prob of %s is %d/%d (%f)" % (tag_str, brown_tag_counts[tag_str],
                                            brown_tag_counts[sub_tag_str], prob)
    essay_probs.append(sent_probs)

flat_essay_probs = []
for sent_probs in essay_probs:
    flat_essay_probs += sent_probs

essay_end_prob = float(sum(flat_essay_probs)) / len(flat_essay_probs)
print "Essay prob: %f/%d (%f)" % (sum(flat_essay_probs), len(flat_essay_probs),
                                  essay_end_prob)
