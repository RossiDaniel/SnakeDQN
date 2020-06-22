import env
import UI
import model
import time

class controller:
    def __init__(self):
        self.width = 80
        self.height = 60
        self.block = 10
        self.env = env.SnakeEnv(self.width,self.height)

    def refreshUI(self):
        self.UI.fill()
        self.UI.draw_snake(self.env.snake_body)
        self.UI.draw_fruit(self.env.fruit)
        self.UI.score(self.env.score)
        self.UI.update()

        self.UI.clock.tick(10)
        #time.sleep(0.5)


    def play_with_UI(self):
        self.UI = UI.snakeuUI(self.width*self.block,self.height*self.block,self.block)
        i = 0
        while self.env.stop_game() == False:
            self.env.update_field()
            action = 1
            self.env.next_state(1)
            self.refreshUI()
            if i > 60:
                break
            else:
                i+=1
        self.UI.gameover()

    def play_without_UI(self):
        i = 0
        while self.env.stop_game() == False:
            self.env.update_field()
            action = 1
            self.env.next_state(1)
            if i > 60:
                break
            else:
                i+=1