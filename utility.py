import numpy as np
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

switch_actions = [(0,-1),(0,1),(-1,0),(1,0)]
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