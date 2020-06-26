import env
import UI
import model
import time
import numpy as np
import random
from tqdm import tqdm
import math
import utility as ut

class controller:
    def __init__(self):
        self.width = 20
        self.height = 20
        self.block = int(800/self.width)
        self.env = env.SnakeEnv(self.width,self.height)
        self.model = model.DQM(self.width,self.height)

        self.global_score = 0
        self.epsilon = 0.70

    def refreshUI(self):
        self.UI.fill()
        self.UI.draw_snake(self.env.snake_body)
        self.UI.draw_fruit(self.env.fruit)
        self.UI.score(self.env.score)
        self.UI.update()

        self.UI.clock.tick(10)
        time.sleep(1)


    def play_with_UI(self):
        for _ in range(10):
            self.UI = UI.snakeuUI(self.width*self.block,self.height*self.block,self.block)
            self.env.random_start()
            self.model.load_trained_model()
            while self.env.stop_game() == False:

                q_values = self.model.predict_q_values(self.env.field)
                print(q_values)
                action = np.argmax(q_values[0])

                transition = self.env.transition(action)
                self.model.add_train_data(transition)
                self.global_score = max(self.global_score,self.env.score)
                self.refreshUI()
            self.UI.gameover()

    def trainIA(self):
        #self.model.load_trained_model()
        gm = 50
        distance = 1
        while True:
            reward_medio = 0
            mosse_medie = 0
            score_medio = 0

            for _ in tqdm(range(gm)):
                self.env.random_start()
                self.distance = int(distance)
                while self.env.stop_game() == False:
                    action = self.choose_action()
                    transition = self.env.transition(action)
                    self.model.add_train_data(transition)
                    self.global_score = max(self.global_score,self.env.score)                    
                    mosse_medie += 1

                reward_medio += self.env.total_reward
                score_medio += self.env.score

            self.model.train()
            distance += 0.5
            gm += 10
            self.epsilon -= 0.05
            print("risultati iterazione corrente:",mosse_medie/gm,reward_medio/gm,len(self.model.buffer),score_medio/gm,self.global_score)

    def choose_action(self):            
        rewards = self.env.reward()
        action = np.argmax(rewards)
        random_action = [i for i, j in enumerate(rewards) if j == rewards[action]]
        action = (random.sample(random_action,k=1))[0]
        
        """
        if rewards[action] == -1:
            
            degrees = ut.angle_between((0,0),(self.env.fruit[0]-self.env.snake_head[0],self.env.fruit[1]-self.env.snake_head[1]))
            vector_choice = 3

            if degrees >= 45 and degrees <= 135: vector_choice = 1
            if degrees >= 135 and degrees <= 225: vector_choice =  2
            if degrees >= 225 and degrees <= 315: vector_choice =  0

            if rewards[vector_choice] != -100:
                action = vector_choice
        """
        if len(self.model.buffer) >= self.model.size_buffer:
            q_values = self.model.predict_q_values(self.env.field)
            q_action = np.max(q_values[0])
            random_action = [i for i, j in enumerate(q_values[0]) if j == q_action]
            qaction = (random.sample(random_action,k=1))[0]

            if(rewards[qaction] < rewards[action]):
                qaction = action

            return qaction
        
        return action
