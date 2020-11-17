#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Created on 17-11-2020 09:11:31

    [Description]
"""
__author__ = "Benedict Wilkins"
__email__ = "benrjw@gmail.com"
__status__ = "Development"

import pygame # for a rendered/playable version of the game
import pygame.gfxdraw
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

    def __init__(self, n=(6,7)):
        super(Connect4, self).__init__()
        self.n = n
        self.state = np.zeros(n, dtype=np.float32) 
        print(self.state.shape)
        self.index = np.zeros(n[1], dtype=np.int8) + n[0] - 1 # record of placement positions
        self.turn = 1 # 1 or -1 depending on the turn

        self.observation_space = gym.spaces.Box(-1,1,shape=self.state.shape, dtype=np.float32)
        self.action_space = Connect4Discrete(n[1]) # n actions, place at the top of the board

        self.done = False

    def step(self, action):
        assert not self.done # THE GAME IS OVER, PLEASE CALL RESET
        assert self.action_space.is_valid(self.state, action) # NO MORE ACTIONS? THE GAME IS OVER! (SANITY CHECK)
        
        self.state[self.index[action], action] = self.turn
        self.done, reward = False, (0,0)

        if self.action_space.mask(self.state).sum() == 0: # DRAW
            self.done, reward = True, (0,0)
        elif self.check_done(self.index[action], action): # WIN!
            self.done, reward = True, (self.turn, -self.turn) # + 1 for winning, -1 for loosing

        self.index[action] -= 1
        self.turn = - self.turn
        print(self.state, self.index)
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
                _done(np.diag(np.fliplr(self.state), k = (self.n[1] - 1 - j) - i ) == t) 
    
    def reset(self):
        self.state = np.zeros(self.n, dtype=np.float32) # n x n grid
        self.index = np.zeros(self.n[1], dtype=np.uint8)  + self.n[0] - 1 # record of placement positions
        self.turn = 1 
        self.done = False
        return self.state 

class Connect4Vis(Connect4):

    def __init__(self, *args, display_size=(640,480), background_colour=(27, 100, 241)):
        super(Connect4Vis, self).__init__(*args)

        pygame.init()

        self.background_colour = background_colour
        self.colours = [(251, 216, 72), (255,255,255), (230, 76, 74)]
        self.display = pygame.display.set_mode(display_size)
        self.rendering = True
        self.render()

    def render(self, delay=1000):
        if self.rendering: 
            
            self.display.fill(self.background_colour)

            # draw the game board
            w, h = pygame.display.get_surface().get_size()
            r =  (min(w,h) - 10) / (2 * (min(self.n) + 1))
            inc = (min(w,h) - 10) / min(self.n)

            hindent = (w - (inc * self.n[1])) / 2
            vindent = (h - (inc * self.n[0])) / 2

            for i in range(self.n[1]):
                for j in range(self.n[0]):
                    c = self.colours[int(self.state[j,i]) + 1]
                    self.fill_circle((hindent + inc/2 + i * inc, vindent + inc/2 + j * inc), r, colour=c)

            pygame.display.update()
            self.wait(delay=delay)
            self.rendering = not self.should_quit()

        return self.rendering

    def should_quit(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                return True
        return False

    def wait(self, delay=1000):
        pygame.time.wait(delay)        

    def draw_circle(self, position, radius, colour=(255,255,255)):
        pygame.gfxdraw.aacircle(self.display, int(position[0]), int(position[1]), int(radius), colour)
    
    def fill_circle(self, position, radius, colour=(255,255,255)):
        pygame.gfxdraw.filled_circle(self.display, int(position[0]), int(position[1]), int(radius), colour)
        pygame.gfxdraw.aacircle(self.display, int(position[0]), int(position[1]), int(radius), colour)

if __name__ == "__main__":
    env = Connect4Vis()
    state = env.reset()
    done = False
    print(state)
    while not done:
        print("---------------")
        action = env.action_space.sample(state)
        state, reward, done, *_ = env.step(action)
        env.render()
        
        print("ACTION:", action, done)
        print(state)