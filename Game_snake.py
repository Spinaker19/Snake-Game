import pygame
import pygame_gui
from pygame_gui.elements import UIButton, UILabel
import sys
from Snake import Snake
from Case import Case

class Game():

    def __init__(self) -> None:
        pygame.init()
        self.__case_size = 20
        self.__size = (int(input("Width: "))*self.__case_size, int(input("Height: "))*self.__case_size)
        self.__screen = pygame.display.set_mode(self.__size)
        self.__manager = pygame_gui.UIManager(self.__size)
        self.__cases = []
        self.__snake = None

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
    
    def draw(self):
        self.__snake.move(self.__screen)

    def run(self):
        for i in range(int(self.__size[0]/self.__case_size)):
            row = []
            for j in range(int(self.__size[1]/self.__case_size)):
                c = Case(self.__case_size-1, (233,236,107), ((i)*self.__case_size,(j)*self.__case_size), (i, j))
                c.draw(self.__screen)
                row.append(c)
            self.__cases.append(row)
        
        #Drawing the snake
        head = self.__cases[int(self.__size[0]/(2*self.__case_size))][int(self.__size[1]/(2*self.__case_size))]
        self.__snake = Snake((0,-1), [head], self.__cases)
        self.__snake.add(self.__cases[head.get_coord()[0]][head.get_coord()[1]+1])
        self.__snake.add(self.__cases[head.get_coord()[0]][head.get_coord()[1]+2])

        self.__snake.draw(self.__screen)

        clock = pygame.time.Clock()
        while True:
            
            #framerate -> speed of the snake
            time_delta = clock.tick(10)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                
                self.process_events(event)
                self.__manager.process_events(event)
            
            self.__manager.update(time_delta/1000)
            self.draw()
            self.__manager.draw_ui(self.__screen)
            pygame.display.flip()

Game().run()  