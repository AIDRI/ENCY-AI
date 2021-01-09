import torch
import torch.nn as nn
from transformers import DistilBertConfig, DistilBertModel
from AI.models.encdec import final_layer

class distilbert(nn.Module):
    def __init__(self):
        super().__init__()
        config = DistilBertConfig()
        self.model = DistilBertModel(config)            

    def forward(self, string, mask):
        first_l = self.model(input_ids=string, attention_mask=mask)[0]
        return first_l


class build_model(nn.Module):
    def __init__(self, ckpt):
        super().__init__()
        self.distilbert = distilbert()
        self.final_layer = final_layer(self.distilbert.model.config.hidden_size, df=2048, heads=8, dropout=0.25, n=2)
        self.load_state_dict(ckpt, strict=False)
        self.to('cpu')

    def forward(self, doc, gen_class, msource, mclasses):
        first_l = self.distilbert(doc, msource)
        out = self.final_layer(first_l[torch.arange(first_l.size(0)).unsqueeze(1), gen_class] * mclasses[:, :, None].float(), mclasses).squeeze(-1)
        return out, mclasses
