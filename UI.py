#take from https://www.edureka.co/blog/snake-game-with-pygame/

import pygame
import time
import random
import utility as ut

pygame.init()

class snakeuUI:
    def __init__(self,width,height,block):
        self.width = width
        self.height = height
        self.snake_block = block
        self.dis = pygame.display.set_mode((width,height))
        pygame.display.update()
        pygame.display.set_caption('snake by daniel')

        #SETTAGGI VARI
        self.dis = pygame.display.set_mode((self.width,self.height))
        self.frames = 30
        self.clock = pygame.time.Clock()

        #FONT
        self.font_style = pygame.font.SysFont("bahnschrift",20)
        self.score_style = pygame.font.SysFont("comicsans",20)

    def score(self,score):
        value = self.score_style.render("Your Score:" + str(score),True,ut.colors['yellow'])
        self.dis.blit(value,[0,0])

    def draw_snake(self,snake_list):
        for xy in snake_list:
            self.draw('black',xy)

    def message(self,msg,color):
        mesg = self.font_style.render(msg,True,ut.colors[color])
        self.dis.blit(mesg,[self.width/2,self.height/2])

    def draw_fruit(self,xy):
        self.draw('green',xy)

    def gameover(self):
        self.message("GAME OVER",'red')
        pygame.display.update()
        time.sleep(0.5)
        #pygame.quit()
        #quit()

    def draw(self,color,xy):
        pygame.draw.rect(self.dis,ut.colors[color],[xy[0]*self.snake_block,xy[1]*self.snake_block,self.snake_block,self.snake_block])

    def fill(self):
        self.dis.fill(ut.colors['blue'])
    def update(self):
        pygame.display.update()

    def frames(self):
        #print("ciao",10,"ciao")
        #self.clock.tick(10)
        pass
    
