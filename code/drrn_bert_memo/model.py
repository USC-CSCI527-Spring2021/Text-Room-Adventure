import numpy as np
import math
import torch
import torch.nn as nn
import torch.nn.functional as F
import random
import itertools
from util import pad_sequences
from memory import State
from transformers import AutoTokenizer, AutoModel

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


class DRRN(torch.nn.Module):
    """
        Deep Reinforcement Relevance Network - He et al. '16
    """

    def __init__(self, hidden_dim=768):
        super(DRRN, self).__init__()

        self.act_max_length = 16
        self.state_max_length = 1024
        self.look_max_length = 256
        self.inv_max_length = 256

        # self.batch_size = 16
        self.bert_tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
        self.bert_encoder = AutoModel.from_pretrained("bert-base-uncased")

        # for name, param in self.bert_encoder.named_parameters():
        #     param.requires_grad = False

        self.hidden = nn.Linear(hidden_dim, hidden_dim)
        self.act_scorer = nn.Linear(hidden_dim, 1)

    def str_to_token_ids(self, input_strs, max_length):
        """input str to token ids"""
        return self.bert_tokenizer(input_strs, max_length=max_length, truncation=True, padding='longest',
                                   return_tensors="pt")

    def bert_encode(self, actions, state, history, act_sizes):
        """ Runs the provided rnn on the input x. Takes care of packing/unpacking.

            x: list of unpadded input sequences
            Returns a tensor of size: len(x) x hidden_dim
        """
        input_strs = []
        act_id = 0
        for n_act, sta, his in zip(act_sizes, state, history):
            for i in range(n_act):
                str = actions[i] + ' [SEP] ' + sta
                # str = actions[i] + ' [SEP] ' + sta + ' [SEP] ' + ' [SEP] '.join(list(reversed(his)))
                # str = actions[i] + ' [SEP] ' + ' [SEP] '.join(list(reversed(his)))
                input_strs.append(str)
                act_id += 1
        batch_input = self.str_to_token_ids(input_strs, 512)

        cuda_input = {}
        for key, value in batch_input.items():
            cuda_input[key] = value.to('cuda')

        outputs = self.bert_encoder(
            **cuda_input,
            # token_type_ids=segment_ids
        )['pooler_output']

        return outputs

    def forward(self, state_batch, act_batch, history):
        """
            Batched forward pass.
            obs_id_batch: iterable of unpadded sequence ids
            act_batch: iterable of lists of unpadded admissible command ids

            Returns a tuple of tensors containing q-values for each item in the batch
        """
        # Zip the state_batch into an easy access format
        # state = State(*zip(*state_batch))
        state = state_batch
        # This is number of admissible commands in each element of the batch
        act_sizes = [len(a) for a in act_batch]
        # Combine next actions into one long list
        act_batch = list(itertools.chain.from_iterable(act_batch))
        # encode action and states
        z = self.bert_encode(act_batch, state, history, act_sizes)
        z = F.relu(self.hidden(z))
        act_values = self.act_scorer(z).squeeze(-1)
        # Split up the q-values by batch
        return act_values.split(act_sizes)

    def act(self, states, act_ids, history, sample=True, return_all=False):
        """ Returns an action-string, optionally sampling from the distribution
            of Q-Values.
        """
        act_values = self.forward(states, act_ids, history)

        if return_all:
            sorted, indices = act_values[0].sort(dim=0, descending=True)
            return indices, sorted

        if sample:
            act_probs = [F.softmax(vals, dim=0) for vals in act_values]
            act_idxs = [torch.multinomial(probs, num_samples=1).item() \
                        for probs in act_probs]
        else:
            act_idxs = [vals.argmax(dim=0).item() for vals in act_values]
        return act_idxs, act_values
