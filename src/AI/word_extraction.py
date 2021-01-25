import yake

def word_extraction(doc, langage="en"):
	s = yake.KeywordExtractor(n=2, top=5, lan=langage)
	k = s.extract_keywords(doc)
	return k
