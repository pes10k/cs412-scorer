from grammar_utils import get_descent_parser
import nltk
import os

parser = get_descent_parser()
essays = [open(os.path.join("data/", "%d.txt" % essay)).readlines() for essay in range(1, 20)]
sentences = essays[0]
for sentence in sentences[1:]:
    words = nltk.word_tokenize(sentence)
    tags = nltk.pos_tag(words)

    tag_swap = ["Chicago" if tag == "NNP" else word for word, tag in tags]
    for t in parser.nbest_parse(tag_swap):
        print t

