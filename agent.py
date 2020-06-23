import numpy as np
class Agent:
    def __init__(self):
        pass

    def next_move(self,reward):
        return np.argmax(reward)
