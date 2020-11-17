#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Created on 17-11-2020 09:10:58

    [Description]
"""
__author__ = "Benedict Wilkins"
__email__ = "benrjw@gmail.com"
__status__ = "Development"

from gym.envs.registration import register

from . import envs

__all__ = ('envs',)

register(id='Connect4-v0', entry_point='connect4.envs:Connect4')

if __name__ == "__main__":

    import gym

    env = gym.make("Connect4-v0")