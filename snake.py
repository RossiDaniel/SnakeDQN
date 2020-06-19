#take from https://www.edureka.co/blog/snake-game-with-pygame/

import pygame
import time
import random

pygame.init()

#dimensioni della schermata di gioco
width = 800
height = 600

#colori
white = (255,255,255)
blue = (50,153,213)
red = (255,0,0)
black = (0,0,0)
yellow = (255,255,102)
green = (0,255,0)


#creiamo la schermata
dis = pygame.display.set_mode((width,height))
pygame.display.update()
pygame.display.set_caption('snake by daniel')

snake_block  = 10
snake_speed = 30

clock = pygame.time.Clock()

font_style = pygame.font.SysFont("bahnschrift",25)
score_style = pygame.font.SysFont("comicsans",35)
def your_score(score):
    value = score_style.render("Your Score:" + str(score),True,yellow)
    dis.blit(value,[0,0])

def our_snake(snake_blocks,snake_list):
    for x in snake_list:
        pygame.draw.rect(dis,black,[x[0],x[1],snake_block,snake_block])

def message(msg,color):
    mesg = font_style.render(msg,True,color)
    dis.blit(mesg,[width/2,height/2])

def gameLoop():
    game_over = False

    x1 = width/2
    y1 = height/2

    x1_change = 0
    y1_change = 0

    snake_list = []
    snake_len = 1

    foodx = random.randrange(0, width - snake_block,10)
    foody = random.randrange(0, height - snake_block,10)

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                if event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                if event.key == pygame.K_UP:
                    x1_change = 0
                    y1_change = -snake_block
                if event.key == pygame.K_DOWN:
                    x1_change = 0
                    y1_change = snake_block
        if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
            game_over = True

        x1 += x1_change
        y1 += y1_change
        dis.fill(blue)

        pygame.draw.rect(dis,green, [foodx,foody,snake_block,snake_block])
        snake_head = (x1,y1)
        snake_list.append(snake_head)

        if len(snake_list) > snake_len:
            del snake_list[0]
        
        for x in snake_list[:-1]:
            if x == snake_head:
                game_over = True

        our_snake(snake_block,snake_list)
        your_score(snake_len-1)
        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = random.randrange(0, width - snake_block,10)
            foody = random.randrange(0, height - snake_block,10)
            snake_len +=1
        clock.tick(snake_speed) 

    message("GAME OVER",red)
    pygame.display.update()
    time.sleep(2)
    pygame.quit()
    quit()

gameLoop()