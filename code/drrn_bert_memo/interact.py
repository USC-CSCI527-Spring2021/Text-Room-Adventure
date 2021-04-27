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

observation, info = env.reset()
done = False
while not done:
    # Take an action in the environment using the step fuction.
    # The resulting text-observation, reward, and game-over indicator is returned.
    print(observation)
    print('valid actions', env.get_valid_actions())

    action = input('> ')

    observation, reward, done, info = env.step(action)

    # Total score and move-count are returned in the info dictionary
    print('Total Score', info['score'], 'Moves', info['moves'])

print('Scored', info['score'], 'out of', env.get_max_score())
