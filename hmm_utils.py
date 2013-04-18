import os
import nltk
from tag_utils import sets_of_tags, serialize_tags
import cPickle as pickle
import tree_utils


def prob_of_all_transitions(transitions, counts, gram_size=2):
    transitions = ['START'] + transitions
    probs = []
    for i in range(0, len(transitions) - gram_size + 1):
        sub_transitions = transitions[i:(i+gram_size)]
        probs.append(prob_of_transition(sub_transitions, counts))
    return probs


def prob_of_transition(transition, counts):
    top = serialize_tags(transition)
    count_top = counts[top]
    bottom = serialize_tags(transition[:-1])
    count_bottom = counts[bottom]
    prob = float(count_top) / count_bottom
    return prob


def store_transitions(tags):
    if not hasattr(store_transitions, '_counts'):
        store_transitions._counts = dict(START=0)
    store_transitions._counts['START'] += 1
    for a_chunk_size in range(1, 4):
        for set_of_tags in sets_of_tags(tags, chunk_size=min(a_chunk_size, len(tags))):
            serialized = serialize_tags(set_of_tags)
            store_transitions._counts.setdefault(serialized, 0)
            store_transitions._counts[serialized] += 1


def get_transition_counts():
    file_name = 'penn_transition_counts.data'

    try:
        f = open(os.path.join('cache', file_name), 'rb')
        data = pickle.load(f)
        f.close()
        return data
    except (IOError, EOFError):
        print "Building counts from Penn Treebank corpus"
        f = open(os.path.join('cache', file_name), 'wb')

        for sentence in nltk.corpus.treebank.parsed_sents():
            all_transitions = tree_utils.transitions_in_tree(sentence)
            for transitions in all_transitions:
                transitions = ['START'] + transitions
                if len(transitions) > 1:
                    store_transitions(transitions)

        print "Finished building tag counts"
        pickle.dump(store_transitions._counts, f)
        f.close()
        return store_transitions._counts
