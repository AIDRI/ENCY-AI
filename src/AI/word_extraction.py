import yake

<<<<<<< HEAD
def word_extraction(doc):
	s = yake.KeywordExtractor(n=1, top=5)
=======
def word_extraction(doc, langage):
	s = yake.KeywordExtractor(n=2, top=5, lan=langage)
>>>>>>> b6da4932e2c69480297be1405f8583b1bdda1d54
	k = s.extract_keywords(doc)
	return k
