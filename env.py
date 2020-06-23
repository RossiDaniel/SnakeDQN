import numpy as np
import random
import utility as ut

class SnakeEnv:
    def __init__(self,width,height):
        self.width = width
        self.height = height

        #informazioni relative la singola partita
        #informazione sul serpente
        self.field = np.zeros((self.width,self.height,1))
        self.snake_head = (int(self.width/2),int(self.height/2))
        self.snake_body = ([self.snake_head])

        #informazioni sul frutto
        self.gen_fruit()
        #punteggio
        self.score = 0
        self.update_field()
    
    def reward(self,act=-1):
        rewards = np.zeros((4))
        for action in range(4):
            new_head,new_body,_ = self.move_snake(action)
            if self.hit_body(new_head,new_body) or self.hit_border(new_head,new_body):
                rewards[action] = -1
            if self.hit_fruit(new_head,new_body):
                rewards[action] = 1
            rewards[action] = -0.1

        if act != -1:
            return rewards[act]
        
        return rewards
        
    def hit_border(self,new_head,new_body):
        #-1 se sbatto contro le pareti
        return new_head[0] >= self.width or new_head[0] < 0 or new_head[1] >= self.height or new_head[1] < 0
    
    def hit_body(self,new_head,new_body):

        for x in new_body[:-1]:
            if x == new_head:
                return 1
        return 0
        
    def hit_fruit(self,new_head,new_body):
        return new_head == self.fruit
            
    def stop_game(self):
        return self.hit_body(self.snake_head,self.snake_body) or self.hit_border(self.snake_head,self.snake_body)
        
    def move_snake(self,action):
        new_head = tuple(map(sum, zip(self.snake_head, ut.switch_actions[action])))
        new_body = self.snake_body[1:] + [new_head]
        return new_head,new_body,self.snake_body[0]

    def next_state(self,action):
        self.snake_head,self.snake_body,start = self.move_snake(action)
        if self.hit_fruit(self.snake_head,self.snake_body):
            self.score += 1
            self.snake_body = [start] + self.snake_body
            self.gen_fruit()

    def transition(self,action):
        transition = [self.field,action,self.reward(action),0,self.hit_fruit(self.snake_head,self.snake_body)]
        self.next_state(action)
        self.update_field()
        transition[3] = self.field
        return transition

    def random_start(self):
        self.field = np.zeros((self.width,self.height,1))
        [sx,sy] = ut.random_distribution(self.width,self.height,[])
        [fx,fy] = ut.random_distribution(self.width,self.height,[(int(sx),int(sy))])
        self.snake_head = (int(sx),int(sy))
        self.snake_body = [self.snake_head]
        self.fruit = (int(fx),int(fy))
        self.score = 0

    def reset(self):
        self.field = np.zeros((self.width,self.height,1))
        self.snake_head = (self.width/2,self.height/2)
        self.snake_body = [self.snake_head]
        self.fruit = self.gen_fruit()
        self.score = 0

    def gen_fruit(self):
        [x,y] = ut.random_distribution(self.width,self.height,self.snake_body)
        self.fruit = (x,y)
        #self.fruit = (int(self.width/2),int(self.height/2)+random.randint(10,20))

    def update_field(self):
        self.field = np.zeros((self.width,self.height,1))
        if not self.stop_game():
            for x,y in self.snake_body:
                self.field[y][x][0] = 1
            self.field[self.snake_head[1],self.snake_head[0],0] = 2
            self.field[self.fruit[0],self.fruit[1],0] = 3
    
    def print_field(self):
        print(self.field.reshape(self.width,self.height))