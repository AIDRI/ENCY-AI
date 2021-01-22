import yake

def word_extraction(doc):
	s = yake.KeywordExtractor(n=1, top=5)
	k = s.extract_keywords(doc[0])
	return k
