# -*- coding: utf-8 -*-
"""
@Author     : Fei Wang
@Contact    : fwang1412@gmail.com
@Time       : 2021/4/11 17:43
@Description: 
"""
from jericho import *
from jericho.template_action_generator import TemplateActionGenerator
from jericho.util import *
from jericho import FrotzEnv

rom_path = "../data/deephome.z5"
env = FrotzEnv(rom_path)
env.reset()

walkthrough = env.get_walkthrough()
expected = [env.step(act) for act in walkthrough]

env.reset()
for i, act in enumerate(walkthrough):
    print('valid actions', env.get_valid_actions())
    print('action:', act)
    obs, rew, done, info = env.step(act)
    print(obs)
    print('reward:', rew, 'done:', done, 'info:', info)

    print('\n---------------------------\n')
    print('iteration', i)


    # if i + 1 < len(walkthrough):
    #     fork = env.copy()
    #     for j, cmd in enumerate(walkthrough[i + 1:], start=i + 1):
    #         obs, rew, done, info = fork.step(cmd)
    #         assert (obs, rew, done, info) == expected[j]
