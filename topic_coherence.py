import sentence_tokenizer
import parsers
from cache_utils import cache_get, cache_set
from nltk.corpus import wordnet
from nltk.stem.porter import PorterStemmer
from cmd_utils import log


stemmer = PorterStemmer()
noun_tags = ('NN', 'NNS',)


work_words = ('work', 'school', 'student', 'boss')
family_words = ('family', 'mom', 'dad', 'cousins', 'aunt', 'uncle', 'mother', 'father', 'husband', 'wife', 'son', 'daughter', 'brother', 'sister', 'children', 'boyfriend', 'girlfriend', 'children', 'child', 'i')
root_words = family_words

#root_words = ('family', 'work', 'school', 'home', 'homeland', 'mom', 'dad', 'cousins', 'aunt', 'uncle', 'mother', 'father', 'husband', 'wife', 'son', 'daughter', 'boss', 'sister', 'brother', 'children', 'child', 'talk', 'time', 'day', 'year', 'school', 'student', 'i')
# methods = ('hypernyms', 'member_meronyms', 'hyponyms', 'member_holonyms')
methods = ('hypernyms', 'hyponyms',)


def build_words(start_words, key=None, use_cache=True, max_depth=3):
    if use_cache:
        wordbank = cache_get('wordbank', 'words_{0}'.format(key))
        if wordbank is not None:
            return wordbank
    words = set()
    for start_word in start_words:
        words.add(start_word)
        for wb_word in wordnet.synsets(start_word, wordnet.NOUN):
            for method in methods:
                new_words = getattr(wb_word, method)()
                for a_word in [a_new_word for a_new_word in new_words]:
                    words.add(a_word.name.split(".")[0].replace("_", "-"))
                    if max_depth > 0:
                        words.update(build_words([a_word.name], key=None, use_cache=False, max_depth=(max_depth-1)))
                        # for lemma in a_word.lemmas:
                        #     words.update(build_words(lemma.name.split(".")[-1].replace("_", "-"), use_cache=False, max_depth=(max_depth-1)))
    if use_cache:
        cache_set('wordbank', 'words', 'words_{0}'.format(key))
    return words


def stemmed_words(words, key=False, use_cache=False):
    if use_cache:
        stemmed_wordbank = cache_get('stemmed_wordbank', 'words_{0}'.format(key))
        if stemmed_wordbank is not None:
            return stemmed_wordbank
    words = set([stemmer.stem(a_word) for a_word in build_words(words, key)])
    if use_cache:
        cache_set('stemmed_wordbank', 'words_{0}'.format(key), words)
    return words


def parse(text):
    log("Checking for coherence in '{0}'".format(text), 2)

    family_hits = []
    family_stem_words = stemmed_words(family_words, 'family_words')
    for sentence in sentence_tokenizer.parse(text):
        tree = parsers.parse(sentence)[0]
        family_hits += [(a_tree.node, a_tree[0].lower(), stemmer.stem(a_tree[0].lower()) in family_stem_words) for a_tree in tree.subtrees(lambda x: x.node in noun_tags)]
    log("Family hits: {0}".format(family_hits), 4)
    family_hit_values = (len([hit for hit in family_hits if hit[2]]), len(family_hits))
    log("%d/%d" % family_hit_values, 3)

    work_hits = []
    work_stem_words = stemmed_words(work_words, 'work_words')
    for sentence in sentence_tokenizer.parse(text):
        tree = parsers.parse(sentence)[0]
        work_hits += [(a_tree.node, a_tree[0].lower(), stemmer.stem(a_tree[0].lower()) in work_stem_words) for a_tree in tree.subtrees(lambda x: x.node in noun_tags)]
    log("Work hits: {0}".format(work_hits), 4)
    work_hit_values = (len([hit for hit in work_hits if hit[2]]), len(work_hits))
    log("%d/%d" % work_hit_values, 3)

    return family_hit_values[0], work_hit_values[0], work_hit_values[1]
