#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Created on 17-11-2020 09:11:31

    [Description]
"""
__author__ = "Benedict Wilkins"
__email__ = "benrjw@gmail.com"
__status__ = "Development"

import gym
import numpy as np

class Connect4Discrete(gym.spaces.Discrete):
    
    def __init__(self, n):
        super(Connect4Discrete, self).__init__(n)
    
    def sample(self, state):
        # only sample actions that are valid
        actions = np.arange(self.n)[self.mask(state)]
        assert len(actions) > 0 # NO VALID ACTIONS IN THIS STATE, GAME OVER?
        return np.random.choice(actions)

    def mask(self, state): 
        return (1 - np.abs(state[0,:])).astype(np.bool) # 0 for invalid, 1 for valid

    def is_valid(self, state, action):
        return state[0, action] == 0

class Connect4(gym.Env):

    def __init__(self, n=7):
        super(Connect4, self).__init__()
        self.n = 7
        self.state = np.zeros((self.n, self.n), dtype=np.float32) # n x n grid
        self.index = np.zeros(self.n, dtype=np.int8) + self.n - 1 # record of placement positions
        self.turn = 1 # 1 or -1 depending on the turn

        self.observation_space = gym.spaces.Box(-1,1,shape=self.state.shape, dtype=np.float32)
        self.action_space = Connect4Discrete(self.n) # n actions, place at the top of the board

        self.done = False

    def step(self, action):
        assert not self.done # THE GAME IS OVER, PLEASE CALL RESET
        assert self.action_space.is_valid(self.state, action) # NO MORE ACTIONS? THE GAME IS OVER! (SANITY CHECK)
        
        self.state[self.index[action], action] = self.turn
        self.done, reward = False, 0

        if self.action_space.mask(self.state).sum() == 0: # DRAW
            self.done, reward = True, 0
        elif self.check_done(self.index[action], action): # WIN!
            self.done, reward = True, 1

        self.index[action] -= 1
        self.turn = - self.turn
        return self.state, reward, self.done

    def check_done(self, i, j):
        def _done(x):
            idx, = np.diff(x).nonzero()
            idx += 1
            if x[0]: # If the start of condition is True prepend a 0
                idx = np.r_[0, idx]
            if x[-1]: # If the end of condition is True, append the length of the array
                idx = np.r_[idx, x.size] # Edit
            idx = idx.reshape(-1, 2)
            return np.any(np.diff(idx, axis=1) >= 4)

        t = self.state[i,j]
        return _done(self.state[i,:] == t) or  \
                _done( self.state[:,j] == t) or  \
                _done(np.diag(self.state, k = j - i) == t) or  \
                _done(np.diag(np.fliplr(self.state), k = (self.n - 1 - j) - i ) == t) 
    
    def reset(self):
        self.state = np.zeros((self.n, self.n), dtype=np.float32) # n x n grid
        self.index = np.zeros(self.n, dtype=np.uint8)  + self.n - 1 # record of placement positions
        return self.state 


if __name__ == "__main__":
    env = Connect4()
    state = env.reset()
    done = False
    print(state)
    while not done:
        print("---------------")
        action = env.action_space.sample(state)
        state, reward, done, *_ = env.step(action)
        
        print("ACTION:", action, done)
        print(state)