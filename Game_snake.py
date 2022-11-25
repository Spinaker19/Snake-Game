import pygame
import pygame_gui
from pygame_gui.elements import UIButton, UILabel
import sys
from Snake import Snake
from Case import Case
import random

class Game():

    def __init__(self) -> None:
        pygame.init()
        self.__case_size = 20
        self.__size = (int(input("Width: "))*self.__case_size, int(input("Height: "))*self.__case_size)
        self.__screen = pygame.display.set_mode(self.__size)
        self.__manager = pygame_gui.UIManager(self.__size)
        self.__cases = []
        self.__snake = None
        self.__score = 0

    def process_events(self, event):
        if event.type == pygame.KEYDOWN:
            #After 'and' is for preventing from turning around
            if event.key == pygame.K_LEFT and self.__snake.get_direction()[0] != 1:
                self.__snake.set_direction((-1,0))
            elif event.key == pygame.K_RIGHT and self.__snake.get_direction()[0] != -1:
                self.__snake.set_direction((1,0))
            elif event.key == pygame.K_UP and self.__snake.get_direction()[1] != 1:
                self.__snake.set_direction((0,-1))
            elif event.key == pygame.K_DOWN and self.__snake.get_direction()[1] != -1:
                self.__snake.set_direction((0,1))

    def draw_fruit(self):
        while True:
            index_x = random.randrange(0, len(self.__cases))
            index_y = random.randrange(0, len(self.__cases[0]))
            if not self.__cases[index_x][index_y].is_fruit() or not self.__cases[index_x][index_y].is_snake():
                self.__cases[index_x][index_y].draw(self.__screen, (0,0,255))
                self.__cases[index_x][index_y].set_is_fruit(True)
                break
        return 0

    def run(self):
        for i in range(int(self.__size[0]/self.__case_size)):
            row = []
            for j in range(int(self.__size[1]/self.__case_size)):
                c = Case(self.__case_size-1, (233,236,107), ((i)*self.__case_size,(j)*self.__case_size), (i, j))
                c.draw(self.__screen)
                row.append(c)
            self.__cases.append(row)
        
        #Drawing the snake
        self.__snake = Snake(self, (0,-1),self.__cases)
        head = self.__cases[int(self.__size[0]/(2*self.__case_size))][int(self.__size[1]/(2*self.__case_size))]
        self.__snake.add(head)
        self.__snake.add(self.__cases[head.get_coord()[0]][head.get_coord()[1]+1])
        self.__snake.add(self.__cases[head.get_coord()[0]][head.get_coord()[1]+2])

        self.__snake.draw(self.__screen)

        #Launch spawn of fruit
        spawn_fruit = 0

        clock = pygame.time.Clock()
        while True:
            
            #framerate -> speed of the snake
            time_delta = clock.tick(10)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                
                self.process_events(event)
                self.__manager.process_events(event)
            
            if spawn_fruit == 15: spawn_fruit = self.draw_fruit()

            spawn_fruit+=1
            self.__manager.update(time_delta/1000)
            if not self.__snake.move(self.__screen) : break
            self.__manager.draw_ui(self.__screen)
            pygame.display.flip()

    def increment_score(self):
        self.__score += 1

    def game_over(self):
        print('Game over')
        print('Your score is {}'.format(self.__score))
        sys.exit()
        #Make a variable 'state' that determine what the while loop will display
        # -> in Game display the game
        # -> Game over display the end screen

Game().run()