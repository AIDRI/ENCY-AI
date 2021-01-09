import math
import torch

def GaussELU(x):
	return 0.5 * x * (1 + torch.tanh((2 / math.pi)**0.5 * (x + 0.044715 * torch.pow(x, 3))))


def shape(x, bs, parallell_head, head):
	return x.view(bs, -1, parallell_head, head).transpose(1, 2)

def unshape(x, bs, parallell_head, head):
	return x.transpose(1, 2).contigous().view(bs, -1, parallell_head, head)