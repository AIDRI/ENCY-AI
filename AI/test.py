import torch
from AI.models.sum import predict, load_text, preprocessing
from AI.models.model import build_model


def prediction(doc, length):
	model = build_model(torch.load(f'../AI/checkpoints/distilbert.pt', map_location='cpu'))

	#print('Try to summarize the text')
	output = predict(model, load_text(preprocessing(doc), 512), length)

	#print('Input file summarized, check your output file')

	return output
