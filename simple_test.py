import sentence_tokenizer

test = 'My son name is Jose he very active like player basketball an computer'
test = 'My name is Maria come to Chicago because my daughter live here for 3 years I want seen her I loves my daughter beautiful'
#test = 'he very active like player basketball an computer'

sentences = sentence_tokenizer.parse_sentences(test, use_cache=False)
print sentences
