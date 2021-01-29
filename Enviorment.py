import numpy as np
import random
import cv2
import time
from threading import Thread
class Render():
    def __init__(self, fieldsize):
        self.w_size = fieldsize * 10
        self.title = "Snake"
        self.red = (0,0,255)
        self.white = (255,255,255)  
        self.blue = (255,0,0)                          
    def render(self, game_field):
        self.image = np.zeros((self.w_size,self.w_size,3)).astype(np.uint8)
        for i , row in enumerate(game_field):
            for j, val in enumerate(row):
                if val >= 1:
                    self.image = cv2.rectangle(self.image, (j* 10, i * 10),(j* 10 +10, i * 10 + 10), self.red)
                if val == -1:
                    self.image = cv2.rectangle(self.image, (j* 10, i * 10),(j* 10 +10, i * 10 + 10), self.white)
                if val == 2:
                    self.image = cv2.rectangle(self.image, (j* 10, i * 10),(j* 10 +10, i * 10 + 10), self.blue)
        cv2.imshow(self.title, self.image)
        cv2.waitKey(80)
class Enviorment():
    def __init__(self,render=False):
        self.steps = 0
        self.current_dir = 4
        self.apple_x = 0
        self.apple_y = 0
        self.fieldsize = 21
        if render:
            self.rend = Render(self.fieldsize)
        self.snake = [[10,10],[10,11]]
        self.gen_game_field()
        self.draw_snake()
        self.reward = 0
        self.create_apple()
    def gen_game_field(self):
        self.game_field = np.zeros((self.fieldsize, self.fieldsize))
        self.game_field[:,0] = -1
        self.game_field[:, self.fieldsize -1] = -1
        self.game_field[0] = -1
        self.game_field[self.fieldsize - 1] = -1
    def draw_snake(self):
        self.game_field[self.apple_y][self.apple_x] = 5
        for i, val in enumerate(self.snake):
            if i == 0:
                self.game_field[val[0]][val[1]] = 2
            else:
                self.game_field[val[0]][val[1]] = -1
    def move_snake(self, direction):
        ''' 
        0 = left
        1 = up
        2 = right
        3 = down
        '''
        for i, val in enumerate(self.snake):
            i +=1
            if i < len(self.snake):
                self.snake[-i] = [self.snake[-i -1][0], self.snake[-i -1][1]]
        
        if direction == 0:
            if self.current_dir != 2:
                self.snake[0][1] = self.snake[0][1] - 1
                self.current_dir = 0
            else:
                self.snake[0][1] = self.snake[0][1] + 1

        if direction == 1: 
            if self.current_dir != 3:
                self.snake[0][0] = self.snake[0][0] - 1
                self.current_dir = 1
            else:
                self.snake[0][0] = self.snake[0][0]  + 1

        if  direction == 2: 
            if self.current_dir != 0:
                self.snake[0][1] = self.snake[0][1] + 1
                self.current_dir = 2
            else:
                self.snake[0][1] = self.snake[0][1] - 1
        
        if direction == 3: 
            if self.current_dir != 1:
                self.snake[0][0] = self.snake[0][0]  + 1
                self.current_dir = 3
            else:
                self.snake[0][0] = self.snake[0][0] - 1

        self.snake_head_val = self.game_field[self.snake[0][0]][self.snake[0][1]]
        self.reward = 0
        self.is_border_touched()
        self.is_apple()
        self.gen_game_field()
        self.draw_snake()
        self.steps += 1
    def is_border_touched(self):
        if self.snake_head_val == -1:
            self.snake_dead()
    def snake_dead(self):
        self.reward = self.snake_head_val
        self.steps = 0
        self.respawn_snake()
    def respawn_snake(self):
        self.snake = [[10,10],[10,11]] 
    def get_game_field(self):
        return self.game_field   
    def get_reward(self):
        return self.reward
    def create_apple(self):
        self.game_field[self.apple_y][self.apple_x] = 0
        while True:
            self.apple_x = random.randint(1, self.fieldsize -1)
            self.apple_y = random.randint(1, self.fieldsize -1)
            if self.game_field[self.apple_y][self.apple_x] != -1 and self.game_field[self.apple_y][self.apple_x] != 2:
                break
    def is_apple(self):
        if self.snake_head_val >= 1:
            self.reward = 1
            self.create_apple()
            self.snake.append(self.snake[-1])
            self.steps = 0
    def render(self):
        self.rend.render(self.game_field)
    def kill_snake_after(self, step):
        if self.steps >= step:
            self.snake_dead()
            self.reward -= 1
if __name__ == "__main__":
    env = Enviorment(render=False)
    for i in range(1000):
        reward = env.get_reward()
        direction = random.randint(0,3)
        env.move_snake(direction)