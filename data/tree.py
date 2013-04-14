from nltk.parse import RecursiveDescentParser
from nltk.corpus import treebank
from nltk.grammar import ContextFreeGrammar, Nonterminal

tbank_productions = set(production for sent in treebank.parsed_sents()
                        for production in sent.productions())
grammar = ContextFreeGrammar(Nonterminal('S'), list(tbank_productions))
parser = RecursiveDescentParser(grammar)
