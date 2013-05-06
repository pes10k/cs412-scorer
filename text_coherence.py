import sentence_tokenizer
import parsers
import sys
import os

sys.path.insert(0, os.path.join("contrib", "nltk_contrib-master"))

from nltk_contrib.coref.tag import mxpost_tag


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
    sentences = sentence_tokenizer.parse(text)
    sentence_index = -1
    for sentence in sentences:
        sentence_index += 1
        pronoun_totals = [[], [], []]
        print sentence
        tree = parsers.parse(sentence)[0]
        pronoun_trees = tree.subtrees(lambda x: x.node in pronoun_tags)
        for pronoun_tree in pronoun_trees:
            # First total up all the first person pronouns
            for i in range(3):
                if pronoun_tree[0].__str__().lower() in pronouns[i]:
                    pronoun_totals[i].append(pronoun_tree[0].lower())
        print pronoun_totals
        if len(pronoun_totals[2]) > 0:
            print mxpost_tag(sentence)

