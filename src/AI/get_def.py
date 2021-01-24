import nltk
from nltk.corpus import wordnet
from googletrans import Translator


def get_def(word):
	translator = Translator()
	word = translator.translate(word, dest='en')
	word_ = str(word.text)
	#print(word_)
	defi = wordnet.synsets(word_.lower())
	defi = defi[0].definition()
	#print(defi)
	return str(translator.translate(defi, dest=word.src).text), str(word.src)


#print(get_def(input()))