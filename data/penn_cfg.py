import nltk
from nltk.corpus import treebank
from nltk.grammar import ContextFreeGrammar, Nonterminal

tbank_productions = set(production for sent in treebank.parsed_sents()
                        for production in sent.productions())
tbank_grammar = ContextFreeGrammar(Nonterminal('S'), list(tbank_productions))

print tbank_grammar.is_lexical()
