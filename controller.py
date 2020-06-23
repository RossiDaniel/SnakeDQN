import env
import UI
import model
import time
import numpy as np

class controller:
    def __init__(self):
        self.width = 10
        self.height = 10
        self.block = 10
        self.env = env.SnakeEnv(self.width,self.height)
        self.model = model.DQM(self.width,self.height)

        self.global_score = 0

    def refreshUI(self):
        self.UI.fill()
        self.UI.draw_snake(self.env.snake_body)
        self.UI.draw_fruit(self.env.fruit)
        self.UI.score(self.env.score)
        self.UI.update()

        self.UI.clock.tick(10)
        time.sleep(1)


    def play_with_UI(self):
        self.UI = UI.snakeuUI(self.width*self.block,self.height*self.block,self.block)
        self.env.random_start()
        while self.env.stop_game() == False:
            action = self.choose_action()            
            transition = self.env.transition(action)
            self.model.add_train_data(transition)
            self.global_score = max(self.global_score,self.env.score)
            self.refreshUI()
        self.UI.gameover()

    def play_without_UI(self):
        self.env.print_field()
        
        i = 0
        while self.env.stop_game() == False:
            #print(self.env.field)
            self.env.update_field()
            action = 1
            self.env.next_state(1)
            if i > 0:
                break
            else:
                i+=1
    
    def trainIA(self):
        gameover_before_train = 0

        while True:
            self.env.random_start()
            while self.env.stop_game() == False:
                action = self.choose_action()            
                transition = self.env.transition(action)
                self.model.add_train_data(transition)
                self.global_score = max(self.global_score,self.env.score)
             
            gameover_before_train = gameover_before_train + 1

            if(gameover_before_train == 100):
                print("inizio training modello")
                self.model.train()
                print("fine training modello ",gameover_before_train," ",len(self.model.buffer)," ",self.global_score)
                gameover_before_train = 0

    def choose_action(self):
        q_values = self.model.predict_q_values(self.env.field)
        action = np.argmax(q_values[0])
        if q_values[0][action] == 0:
            return random.randint(4)
        return action