import numpy as np
import random

def random_distribution(width,height,snake_list,k=1):
    x = np.arange(width)
    y = np.arange(height)
    cart = np.transpose([np.tile(x, len(y)), np.repeat(y, len(x))])

    weight = np.ones((height,width))
    for (i,j) in snake_list:
        weight[j,i] = 0
    
    weight = np.ravel(weight)
    Pweights = weight/weight.sum(axis=0,keepdims=1)

    return cart[np.random.choice(len(cart),1,p=Pweights)[0]]

switch_actions = [(0,1),(0,-1),(-1,0),(1,0)]
#0 = UP
#1 = DOWN
#2 = LEFT
#3 = RIGHT

colors = {"white" : (255,255,255),
"blue" : (50,153,213),
"red" : (255,0,0),
"black" : (0,0,0),
"yellow" : (255,255,102),
"green" : (0,255,0)}

def generate_fruit_certain_distance(width,height,snake_list,distance=2):
    snake_head = snake_list[len(snake_list)-1]
    
    while True:
        x = snake_head[0] + random.randint(-distance,distance)
        y = snake_head[1] + random.randint(-distance,distance)
        x_s = min(max(0,x),width-1)
        y_s = min(max(0,y),height-1)
        if(snake_head != (x_s,y_s)):
            return [x_s,y_s]

def angle_between(p1, p2):
    ang1 = np.arctan2(*p1[::-1])
    ang2 = np.arctan2(*p2[::-1])
    return np.rad2deg((ang1 - ang2) % (2 * np.pi))