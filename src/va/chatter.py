import json
import torch
import torch.nn as nn
import random
import nltk
import numpy as np

from nltk.stem.porter import PorterStemmer

class NN(nn.Module):
	    def __init__(self, i_s, h_s, n):
	        super().__init__()
	        self.w1 = nn.Linear(i_s, h_s) 
	        self.w2 = nn.Linear(h_s, h_s) 
	        self.w3 = nn.Linear(h_s, n)

	    def forward(self, x):
	        return self.w3(nn.ReLU()(self.w2(nn.ReLU()(self.w1(x)))))


def chatter(doc):
	def load_file(name):
		with open(name, 'r') as f:
			data = json.load(f)
		return data

	data = load_file('va/intents.json')
	model_file = torch.load("va/checkpoints/data.pth")
	model = NN(model_file['i_s'], model_file['h_s'], model_file['o_s']).to('cpu')
	model.load_state_dict(model_file['state'])
	stemmer = PorterStemmer()

	inp = nltk.word_tokenize(doc)
	sentence_words = [stemmer.stem(word.lower()) for word in inp]
	X = np.zeros(len(model_file['w']), dtype=np.float32)
	for i, word in enumerate(model_file['w']):
		if word in sentence_words: 
			X[i] = 1

	X = torch.from_numpy(X.reshape(1, X.shape[0])).to('cpu')
	_, p = torch.max(model(X), dim=1)


	if torch.softmax(model(X), dim=1)[0][p.item()].item() > 0.75: 
		for par in data['intents']:
			if model_file['t'][p.item()] == par['tag']:
				responses = par['responses']
		return random.choice(responses)
	else:
		return 'Mmmh... be more explicit, i\'m just a poor robot who try to help you :)'