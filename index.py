import pygame
from pygame.locals import *
import time
import random

SIZE = 40

class Apple():
    def __init__(self, parent_screen):
        self.image = pygame.image.load(r"C:\Users\share\OneDrive\Desktop\time waste things\snake game jpgs\apple.jpg").convert()
        self.x = SIZE * 3
        self.y = SIZE * 3
        self.parent_screen = parent_screen

    def drew(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        max_range = (800 // SIZE) - 1
        self.x = random.randint(0, max_range) * SIZE
        self.y = random.randint(0, max_range) * SIZE

class Snake():
    def __init__(self, parent_screen, length):
        self.length = length
        self.parent_screen = parent_screen
        self.block = pygame.image.load(
            r"C:\Users\share\OneDrive\Desktop\time waste things\snake game jpgs\block.jpg").convert()
        self.x = [SIZE] * 40
        self.y = [SIZE] * 40
        self.direction = 'down'
    def increased_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def drew(self):
        self.parent_screen.fill((200, 200, 200))
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def move_right(self):
        self.direction = 'right'

    def move_left(self):
        self.direction = 'left'

    def walk(self):
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE
        if self.direction == 'right':
            self.x[0] += SIZE
        if self.direction == 'left':
            self.x[0] -= SIZE
        self.drew()


class Game():
    def __init__(self) -> object:
        pygame.init()
        self.screen = pygame.display.set_mode((800, 800))
        self.screen.fill((200, 200, 200))
        self.snake = Snake(self.screen, 1)
        self.snake.drew()
        self.apple = Apple(self.screen)
        self.apple.drew()
        self.running = True
        self.pause = False

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False

    def display_score(self):
        font = pygame.font.SysFont('arial',30)
        score = font.render(f"score : {self.snake.length}",True,(10,1,1))
        self.screen.blit(score,(600,10))
    def game_over(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f'''Game Over. Your score is : {self.snake.length} press enter to play the game. or press exit''' , True, (10, 1, 1))
        self.screen.blit(score, (400 - score.get_width() // 2, 400 - score.get_height() // 2))
        pygame.display.flip()

        while True :
            for event in pygame.event.get():
                if event.type == KEYDOWN :
                    if event.key == K_RETURN:
                        self.__init__()
                        self.run()
                    elif event.key == K_ESCAPE :
                        pygame.quit()
                        quit()

    def play(self):
        if self.pause:
            font = pygame.font.SysFont('arial', 30)
            score = font.render(f"Your score is : {self.snake.length} press p to play the game", True,(10, 1, 1))
            self.screen.blit(score, (400 - score.get_width() // 2, 400 - score.get_height() // 2))
            pygame.display.flip()
            return()

        self.snake.walk()
        self.apple.drew()
        self.display_score()
        pygame.display.flip()
         # apple and snake collision
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.snake.increased_length()
            self.apple.move()
        # snake and its body collision
        for i in range(3 , self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.running = False
                self.game_over()
        # snake with borders collision
        if self.snake.x[0] < 0 or self.snake.x[0] >= 800 or self.snake.y[0] < 0 or self.snake.y[0] >= 800:
            self.running = False
            self.game_over()


    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.running = False
                    if event.key == K_UP:
                        self.snake.move_up()
                    if event.key == K_DOWN:
                        self.snake.move_down()
                    if event.key == K_RIGHT:
                        self.snake.move_right()
                    if event.key == K_LEFT:
                        self.snake.move_left()
                    if event.key == K_p :
                        self.pause = not self.pause
                    if event.key == K_RETURN and not self.running :
                        self.__init__()
                elif event.type == QUIT:
                    self.running = False
            self.play()
            time.sleep(0.3)


if __name__ == "__main__":
    game = Game()
    game.run()



