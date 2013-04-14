import cPickle as pickle
import os


# Dumb global structures, just needed once through the whole
simple_tag_subs = dict(NNS='NN', NNPS='NNP', VBD='VB', VBG='VB', VBN='VB',
                       VBP='VB', VBZ='VBZ')


def simplify_tag(tag):
    if tag in simple_tag_subs:
        return simple_tag_subs[tag]
    else:
        return tag


def simplify_tags(tags):
    """Normalize tags, attepting to remove things like tense and singluar/plural"""
    simp_tags = []
    for tag in tags:
        if tag in simple_tag_subs:
            simp_tags.append(simple_tag_subs[tag])
        else:
            simp_tags.append(tag)
    return simp_tags


def is_valid_tag(tag):
    tags_to_ignore = ('``', '""', "''", '--', '-NONE-')
    return (tag not in tags_to_ignore and (len(tag) > 1 or (ord(tag) > 64 and ord(tag) < 91)))


def prune_tags(tags):
    return [tag for tag in tags if is_valid_tag(tag)]


def sent_as_tags(sentence):
    return [tag for word, tag in sentence if is_valid_tag]


def sub_tags_in_list(source_tags, end=0, size=1):
    start_index = end - size
    if start_index < 0:
        return (['START'] * abs(start_index + 1)) + source_tags[max(start_index, 0):(end + 1)]
    else:
        return source_tags[start_index + 1:(end + 1)]


def sets_of_tags(tags, chunk_size=1):
    tags_len = len(tags)
    return [((['START'] * (abs(min(i - chunk_size + 1, 0)))) + tags[max(i - chunk_size + 1, 0):i + 1]) for i in range(0, tags_len)]


def serialize_tags(tags):
    return "@".join(tags)


def get_cached_counts(file_name='tag_counts.data', worker_func=None):
    print "using cached file " + file_name
    try:
        f = open(os.path.join('cache', file_name), 'r')
        data = pickle.load(f)
        f.close()
        print "Successfully loaded cached tag data from Penn Treebank corpus"
        return data
    except (IOError, EOFError):
        import nltk.corpus
        print "Building counts from Penn Treebank corpus"

        f = open(os.path.join('cache', file_name), 'w')
        tags_counts = dict()
        i = 0
        for sentence in nltk.corpus.treebank.tagged_sents():
            tags_counts.setdefault('START', 0)
            tags_counts['START'] += 1
            i += 1
            print "Parsing Sentence %d" % (i,)
            tags = sent_as_tags(sentence)

            if worker_func:
                tags = worker_func(tags)

            for a_chunk_size in range(1, 6):
                for set_of_tags in sets_of_tags(tags, chunk_size=a_chunk_size):
                    serialized = serialize_tags(set_of_tags)
                    tags_counts.setdefault(serialized, 0)
                    tags_counts[serialized] += 1
        print "Finished building tag counts"
        pickle.dump(tags_counts, f)
        f.close()
        return tags_counts
