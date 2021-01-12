import torch
import torch.nn as nn
from transformers import DistilBertConfig, DistilBertModel
from AI.models.encdec import FinalEncoder

class Bert(nn.Module):
    def __init__(self):
        super().__init__()
        configuration = DistilBertConfig()
        self.model = DistilBertModel(configuration)            

    def forward(self, doc, s, mask):
        top_vec = self.model(input_ids=doc, attention_mask=mask)[0]
        return top_vec


class build_model(nn.Module):
    def __init__(self, checkpoint=None):
        super().__init__()
        self.bert = Bert()
        self.ext_layer = FinalEncoder(self.bert.model.config.hidden_size, d_ff=2048, heads=8, dropout=0.2, num_inter_layers=2)
        self.load_state_dict(checkpoint, strict=False)
        self.to('cpu')

    def forward(self, doc, s, c, mask, mask_c):
        v = self.bert(doc, s, mask)
        output = v[torch.arange(v.size(0)).unsqueeze(1), c]
        output = output * mask_c[:, :, None].float()
        acc = self.ext_layer(output, mask_c).squeeze(-1)
        return acc, mask_c
