import math
import torch
import torch.nn as nn
import torch.nn.functional as F

from AI.models.utils import GaussELU, get_shape


class ForwardPos(nn.Module):
	def __init__(self, inputdim, outputdim):
		super().__init__()
		self.weight1 = nn.Linear(inputdim, outputdim)
		self.weight2 = nn.Linear(outputdim, inputdim)
		self.normalisation = nn.LayerNorm(inputdim)
		self.activation = GaussELU
		self.dropout = nn.Dropout(0.15)

	def forward(self, x):
		residual = x
		out = self.dropout(self.weight2(self.dropout(self.activation(self.weight1(self.normalisation(x)))))) + residual
		return out


class EncodingPos(nn.Module):
    def __init__(self, d, n=5000):
        pe = torch.zeros(n, d)
        position = torch.arange(0, n).unsqueeze(1)
        div_term = torch.exp((torch.arange(0, d, 2, dtype=torch.float) * -(math.log(10000.0) / d)))
        pe[:, 0::2] = torch.sin(position.float() * div_term)
        pe[:, 1::2] = torch.cos(position.float() * div_term)
        pe = pe.unsqueeze(0)
        super().__init__()
        self.register_buffer("pe", pe)


class MultiHeadAttn(nn.Module): #found the base of the multi head attention on github (not totally mine)
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
                k = get_shape(self.wk(q), bs, hl_n, hl)
                v = get_shape(self.wk(q), bs, hl_n, hl)

                if cache is not None:
                    if cache["self_keys"] is not None: k = torch.cat((cache["self_keys"].to('cpu'), k), dim=2)
                    if cache["self_values"] is not None: v = torch.cat((cache["self_values"].to('cpu'), v), dim=2)
                    cache["self_keys"] = k
                    cache["self_values"] = v

            elif type == "context":
                q = self.wq(q)
                if cache is not None:
                    if cache["memory_keys"] is None: k = get_shape(self.wk(k), bs, hl_n, hl); v = shape(self.wv(v), bs, hl_n, hl)
                    else: k, v = cache["memory_keys"], cache["memory_values"]
                    cache["memory_keys"] = k
                    cache["memory_values"] = v
                else:
                    k = get_shape(self.wk(k), bs, hl_n, hl)
                    v = get_shape(self.wv(v), bs, hl_n, hl)
        else:
            k = get_shape(self.wk(k), bs, hl_n, hl)
            v = get_shape(self.wv(v), bs, hl_n, hl)
            q = self.wq(q)
        q = get_shape(q, bs, hl_n, hl)
        klength = k.size(2)
        qlength = q.size(2)
        q = q / hl**0.5
        scores = torch.matmul(q, k.transpose(2, 3))
        scores = scores.masked_fill(mask.unsqueeze(1).expand_as(scores).byte(), -1e18)
        attn = self.softmax(scores)
        tmp = torch.matmul(self.dropout(attn), v)
        context = tmp.transpose(1, 2).contiguous().view(bs, -1, hl_n * hl)
        output = self.final_linear(context)
        return output


class EncoderLayer(nn.Module):
    def __init__(self, n, heads, feed_forward_size, dropout=0.25):
        super().__init__()
        self.self_attn = MultiHeadAttn(heads, n)
        self.ff = ForwardPos(n, feed_forward_size)
        self.layer_norm = nn.LayerNorm(n, eps=1e-6)
        self.dropout = nn.Dropout(dropout)

    def forward(self, i, _input, mask):
        if i != 0: inputs = self.layer_norm(_input)
        else: inputs = _input
        att = self.self_attn(inputs, inputs, inputs, mask=mask.unsqueeze(1))
        return self.ff(self.dropout(att) + _input)


class final_layer(nn.Module):
    def __init__(self, dm, df, heads, dropout=0.25, n=0):
        super().__init__()
        self.n = n
        self.emb = EncodingPos(dm)
        self.transformer = nn.ModuleList([EncoderLayer(dm, heads, df, dropout) for _ in range(n)])
        self.layer_norm = nn.LayerNorm(dm, eps=1e-6)
        self.wo = nn.Linear(dm, 1, bias=True)
        self.sigmoid = nn.Sigmoid()

    def forward(self, v, mask):
        _, ns = v.size(0), v.size(1)
        x = v * mask[:, :, None].float() + self.emb.pe[:, :ns]
        for i in range(self.n): x = self.transformer[i](i, x, 1 - mask)
        x = self.layer_norm(x)
        return self.sigmoid(self.wo(x)).squeeze(-1) * mask.float()
