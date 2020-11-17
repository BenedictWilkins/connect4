#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Created on 17-11-2020 11:17:43

    [Description]
"""
__author__ = "Benedict Wilkins"
__email__ = "benrjw@gmail.com"
__status__ = "Development"

import gym

env = gym.make("Connect4-v1")

state = env.reset()
done = False
print(state)
while not done:
    print("---------------")
    action = env.action_space.sample(state)
    state, reward, done, *_ = env.step(action)
    
    print("ACTION:", action, done)
    print(state)
    env.render(delay=200)

while not env.should_quit():
    env.wait(delay=200)
