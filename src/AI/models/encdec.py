import math
import torch
import torch.nn as nn
import torch.nn.functional as F

from AI.models.utils import GaussELU, shape


class ForwardPos(nn.Module):
	def __init__(self, inputdim, outputdim):
		super().__init__()
		self.w1 = nn.Linear(inputdim, outputdim)
		self.w2 = nn.Linear(outputdim, inputdim)
		self.LayerNorm = nn.LayerNorm(inputdim)
		self.activation = GaussELU
		self.dropout = nn.Dropout(0.15)

	def forward(self, x):
		residual = x
		out = self.dropout(self.w2(self.dropout(self.activation(self.w1(self.LayerNorm(x)))))) + residual
		return out

class MultiHeadAttn(nn.Module): #found on github
	def __init__(self, hl_n, dim):
		self.hl = dim // hl_n
		self.dim = dim
		super().__init__()
		self.hl_n = hl_n
		self.wk = nn.Linear(dim, hl_n * self.hl)
		self.wv = nn.Linear(dim, hl_n * self.hl)
		self.wq = nn.Linear(dim, hl_n * self.hl)
		self.softmax = nn.Softmax(dim=-1)
		self.dropout = nn.Dropout(0.1)
		self.final_linear = nn.Linear(dim, dim)

	def forward(self, k, v, q, mask=None, cache=None, type=None):
		bs = k.size(0)
		hl = self.hl
		hl_n = self.hl_n
		klength = k.size(1)
		qlength = q.size(1)
		if cache is not None:
			if type == "self":
				q = self.wq(q)
				k = shape(self.wk(q), bs, hl_n, hl)
				v = shape(self.wk(q), bs, hl_n, hl)
				if cache is not None:
					if cache["self_keys"] is not None: k = torch.cat((cache["self_keys"].to('cpu'), k), dim=2)
					if cache["self_values"] is not None: v = torch.cat((cache["self_values"].to('cpu'), v), dim=2)
					cache["self_keys"] = k
					cache["self_values"] = v
			elif type == "context":
				q = self.wq(q)
				if cache is not None:
					if cache["memory_keys"] is None: k = shape(self.wk(k), bs, hl_n, hl); v = shape(self.wv(v), bs, hl_n, hl)
					else: k, v = cache["memory_keys"], cache["memory_values"]
					cache["memory_keys"] = k
					cache["memory_values"] = v
				else: k, v = shape(self.wk(k), bs, hl_n, hl), shape(self.wv(v), bs, hl_n, hl)
		else: k, v, q = shape(self.wk(k), bs, hl_n, hl), shape(self.wv(v), bs, hl_n, hl), self.wq(q)
		q = shape(q, bs, hl_n, hl)
		klength = k.size(2)
		qlength = q.size(2)
		q = q / hl**0.5
		a = torch.matmul(q, k.transpose(2, 3))
		a = a.masked_fill(mask.unsqueeze(1).expand_as(a).byte(), -1e18)
		attn = self.softmax(a)
		tmp = torch.matmul(self.dropout(attn), v)
		context = tmp.transpose(1, 2).contiguous().view(bs, -1, hl_n * hl)
		output = self.final_linear(context)
		return output


class PositionalEncoding(nn.Module):
	def __init__(self, dropout, dim, max_len=5000):
		pe = torch.zeros(max_len, dim)
		position = torch.arange(0, max_len).unsqueeze(1)
		div_term = torch.exp((torch.arange(0, dim, 2, dtype=torch.float) * -(math.log(10000.0) / dim)))
		pe[:, 0::2] = torch.sin(position.float() * div_term)
		pe[:, 1::2] = torch.cos(position.float() * div_term)
		pe = pe.unsqueeze(0)
		super().__init__()
		self.register_buffer("pe", pe)
		self.dropout = nn.Dropout(p=dropout)
		self.dim = dim

	def forward(self, e, ep=None):
		return self.dropout((e * self.dim**0.5) + self.pe[:, ep][:, None, :])

	def get_emb(self, e):
		return self.pe[:, : e.size(1)]


class TransformerEncoderLayer(nn.Module):
	def __init__(self, d_model, heads, d_ff, dropout):
		super().__init__()
		self.self_attn = MultiHeadAttn(heads, d_model)
		self.feed_forward = ForwardPos(d_model, d_ff)
		self.layer_norm = nn.LayerNorm(d_model, eps=1e-6)
		self.dropout = nn.Dropout(dropout)

	def forward(self, i, inputs, mask):
		if i != 0: n = self.layer_norm(inputs)
		else: n = inputs
		return self.feed_forward(self.dropout(self.self_attn(n, n, n, mask=mask.unsqueeze(1))) + inputs)


class FinalEncoder(nn.Module):
	def __init__(self, d_model, d_ff, heads, dropout, num_inter_layers=0):
		super().__init__()
		self.num_inter_layers = num_inter_layers
		self.pos_emb = PositionalEncoding(dropout, d_model)
		self.transformer_inter = nn.ModuleList([TransformerEncoderLayer(d_model, heads, d_ff, dropout) for _ in range(num_inter_layers)])
		self.layer_norm = nn.LayerNorm(d_model)
		self.wo = nn.Linear(d_model, 1, bias=True)
		self.sigmoid = nn.Sigmoid()

	def forward(self, top_vecs, mask):
		x = top_vecs * mask[:, :, None].float() + self.pos_emb.pe[:, :top_vecs.size(1)]
		for i in range(self.num_inter_layers): x = self.transformer_inter[i](i,x,1-mask)
		return self.sigmoid(self.wo(self.layer_norm(x))).squeeze(-1) * mask.float()
