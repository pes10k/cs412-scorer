from nltk.parse import ShiftReduceParser
from nltk.corpus import treebank
from nltk.grammar import ContextFreeGrammar, Nonterminal


def get_descent_parser():
    productions = set(production for sent in treebank.parsed_sents()
                      for production in sent.productions())
    grammar = ContextFreeGrammar(Nonterminal('S'), list(productions))
    parser = ShiftReduceParser(grammar)
    return parser
