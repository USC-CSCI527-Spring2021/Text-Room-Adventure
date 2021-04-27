import pickle
import torch
import torch.nn as nn
import torch.nn.functional as F
from os.path import join as pjoin
from memory import ReplayMemory, Transition, State
from model import DRRN
from util import *
import logger
from transformers import get_linear_schedule_with_warmup

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


class DRRN_Agent:
    def __init__(self, args):
        self.gamma = args.gamma
        self.batch_size = args.batch_size
        self.accummulate_step = args.accummulate_step

        self.network = DRRN().to(device)
        self.memory = ReplayMemory(args.memory_size)
        self.save_path = args.output_dir
        self.clip = args.clip
        self.optimizer = torch.optim.Adam(self.network.parameters(),
                                          lr=args.learning_rate)

        # self.scheduler = get_linear_schedule_with_warmup(self.optimizer, num_warmup_steps=args.warmup_steps,
        #                                                  num_training_steps=args.max_steps)

    def observe(self, state, act, rew, next_state, next_acts, done, history):
        self.memory.push(state, act, rew, next_state, next_acts, done, history)

    def build_state(self, obs, infos):
        """ Returns a state representation built from various info sources. """
        # obs_ids = [self.network.str_to_token_ids(o, self.network.state_max_length) for o in obs]
        # look_ids = [self.network.str_to_token_ids(info['look'], self.network.look_max_length) for info in infos]
        # inv_ids = [self.network.str_to_token_ids(info['inv'], self.network.inv_max_length) for info in infos]
        # return [State(ob, lk, inv) for ob, lk, inv in zip(obs_ids, look_ids, inv_ids)]
        states = []
        for obs, info in zip(obs, infos):
            state = obs + info['look'] + info['inv']
            states.append(state)
        return states

    def encode(self, act_list):
        """ Encode a list of actions """
        # return [self.network.str_to_token_ids(o, self.network.act_max_length) for o in act_list]
        return act_list

    def act(self, states, poss_acts, history, sample=True, return_all=False):
        """ Returns a string action from poss_acts. """
        idxs, values = self.network.act(states, poss_acts, history, sample, return_all)

        if return_all:
            return None, idxs, values

        act_ids = [poss_acts[batch][idx] for batch, idx in enumerate(idxs)]
        return act_ids, idxs, values

    def update(self):
        if len(self.memory) < self.batch_size:
            return

        batch_loss = None
        num_per_step = int(self.batch_size/self.accummulate_step)
        for _ in range(self.accummulate_step):

            transitions = self.memory.sample(num_per_step)
            batch = Transition(*zip(*transitions))

            # Compute Q(s', a') for all a'
            # TODO: Use a target network???
            next_history = []
            for act, history in zip(batch.act, batch.history):
                next_history.append(history + [act])
            next_qvals = self.network(batch.next_state, batch.next_acts, next_history)
            # Take the max over next q-values
            next_qvals = torch.tensor([vals.max() for vals in next_qvals], device=device)
            # Zero all the next_qvals that are done
            next_qvals = next_qvals * (1 - torch.tensor(batch.done, dtype=torch.float, device=device))
            targets = torch.tensor(batch.reward, dtype=torch.float, device=device) + self.gamma * next_qvals

            # Next compute Q(s, a)
            # Nest each action in a list - so that it becomes the only admissible cmd
            nested_acts = tuple([[a] for a in batch.act])
            qvals = self.network(batch.state, nested_acts, batch.history)
            # Combine the qvals: Maybe just do a greedy max for generality
            qvals = torch.cat(qvals)

            loss = F.smooth_l1_loss(qvals, targets.detach())

            # Compute Huber loss
            if batch_loss is None:
                batch_loss = loss
            else:
                batch_loss += loss

        batch_loss /= num_per_step

        self.optimizer.zero_grad()
        batch_loss.backward()
        nn.utils.clip_grad_norm_(self.network.parameters(), self.clip)
        self.optimizer.step()
        # self.scheduler.step()

        return loss.item()

    def load(self):
        try:
            self.memory = pickle.load(open(pjoin(self.save_path, 'memory.pkl'), 'rb'))
            self.network = torch.load(pjoin(self.save_path, 'model.pt'))
        except Exception as e:
            print("Error saving model.")
            logging.error(traceback.format_exc())

    def save(self):
        try:
            pickle.dump(self.memory, open(pjoin(self.save_path, 'memory.pkl'), 'wb'))
            torch.save(self.network, pjoin(self.save_path, 'model.pt'))
        except Exception as e:
            print("Error saving model.")
            logging.error(traceback.format_exc())
