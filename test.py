import torch
from models.sum import predict, load_text, preprocessing
from models.model import build_model

print('Loading Model')
model = build_model(checkpoint=torch.load(f'checkpoints/bert.pt', map_location='cpu'), bert_type='bert', device='cpu')

print('Try to summarize the text')
predict(model, load_text(preprocessing('test/inp.txt'), 512), 'test/out.txt', 10)

print('Input file summarized, check your output file')