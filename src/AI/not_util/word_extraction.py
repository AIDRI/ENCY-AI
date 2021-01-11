from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import itertools


def words_distance(string, word, words, n, nc):
	words_d = cosine_similarity(word, word)
	idx = list(cosine_similarity(string, word).argsort()[0][-nc:])
    
	words_of_interest = words_d[np.ix_(idx, idx)]
	sum_dist_min=1*10**100
	tmp = None
	for c in itertools.combinations(range(len(idx)), n):
		sum_dist_act = sum([words_of_interest[m][n] for m, n in zip(c, c) if not m == n])
		if sum_dist_act < sum_dist_min: tmp = c; sum_dist_min = sum_dist_act

	return [[words[y] for y in idx][i] for i in tmp]


def word_extraction(string, size=(1, 1), n=5, c=5):
	words_vectorize = CountVectorizer(ngram_range=size).fit([string]).get_feature_names()
	model = SentenceTransformer('distilbert-base-nli-mean-tokens')
	return words_distance(model.encode([string]), model.encode(words_vectorize), words_vectorize, n, c)