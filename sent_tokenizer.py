import nltk
from nltk.corpus import PlaintextCorpusReader

# change the root to where ever you have the essays at
corpus_root = '/Users/dianaroberts/Desktop/essayCorpus'
essays = PlaintextCorpusReader(corpus_root, '[0-9]*.txt')

# I am not sure if I have this reference to the essays correct... same with line 13
sents = essays.sents()
tokens = []
boundaries = set()
offset = 0
for sent in essays.sents():
  tokens.extend(sent)
	offset += len(sent)
	boundaries.add(offset-1)

def punct_features(tokens, i):
	return { 'Next-word-cap': tokens[i+1][0].isupper(),
			'prevword': tokens[i-1].lower(),
			'punct' : tokens[i],
			'prev-word-is-one-char': len(tokens[i-1]) == 1}

featuresets = [(punct_features(tokens,i)(i in boundaries))
	for i in range(1, len(tokens)-1)
	if tokens[i] in '.?!']

#this trains and evaluates a punctuation classifier
# not sure if we need it in the final version
size = int(len(featuresets)*0.1)
train_set, test_set = featuresets[size:], featuresets[:size]
classifier = nltk.NaiveBayesClassifier.train(train_set)
nltk.classify.accuracy(classifier, test_set)

#sentence segmentation
# I am also not sure if that is the proper way to add the next line character
# will test and figure it out. 
def segment_sentence(words):
	start = 0
	sents = []
	for i, word in enumerate(words) :
		if word in '.?!|\n' and classifier.classify(punct_features(words, i)) == True:
			sents.append(words[start:i+1])
			start = i+1
		if start < len(words):
			sents.append(words[start:])
		return sents
		


