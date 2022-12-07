import pygame
import pygame_gui
from pygame_gui.elements import UIButton, UILabel, UITextEntryLine
import sys
from Snake import Snake
from Case import Case
import random
import json

class Game():

    def __init__(self) -> None:
        # pygame.init()
        # self.__case_size = 20
        # self.__size = (int(input("Width: "))*self.__case_size, int(input("Height: "))*self.__case_size)
        # self.__screen = pygame.display.set_mode(self.__size)
        # self.__cases = []
        # self.__snake = None
        # self.__score = 0

        pygame.init()
        self.__case_size = 20
        self.__size = (300, 300)
        self.__screen = pygame.display.set_mode(self.__size)
        self.__cases = []
        self.__snake = None
        self.__score = 0
        self.__manager = pygame_gui.UIManager(self.__size)

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

    def increment_score(self):
        self.__score +=1

    def menu(self):
        
        clock = pygame.time.Clock()
        label_width = UILabel(pygame.Rect(100,50,50, 50), "width : ", self.__manager)
        width = UITextEntryLine(pygame.Rect(150, 50, 50, 50), self.__manager)
        label_height = UILabel(pygame.Rect(100,100,50, 50), "height : ", self.__manager)
        height = UITextEntryLine(pygame.Rect(150, 100, 50, 50), self.__manager)
        play = UIButton(pygame.Rect(100,150,100,50), "Play !",self.__manager)
        breaker = False
        while True:
            time_delta = clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == play: breaker = True

                self.__manager.process_events(event)
            
            self.__manager.update(time_delta/1000)
            self.__manager.draw_ui(self.__screen)
            if breaker: break
            pygame.display.flip()
        
        self.__size = (int(width.text)*self.__case_size, int(height.text)*self.__case_size)
        self.__screen = pygame.display.set_mode(self.__size)
        self.__manager = pygame_gui.UIManager(self.__size)
        self.run()

    def run(self):
        pygame.draw.rect(self.__screen, (0, 0, 0), pygame.Rect(0, 0, self.__size[0], self.__size[1]))

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
            
            if spawn_fruit == 15: spawn_fruit = self.draw_fruit()

            spawn_fruit+=1
            if not self.__snake.move(self.__screen): break
            pygame.display.flip()

        self.game_over() 


    def game_over(self):
        pygame.draw.rect(self.__screen, (0, 0, 0), pygame.Rect(0, 0, self.__size[0], self.__size[1]))
        
        #init UImanager
        manager = pygame_gui.UIManager(self.__size)

        #init UI
        width = self.__size[0]/2
        height = self.__size[1]/10
        left = self.__size[0]/4
        top = self.__size[1]/4
        game_over = UILabel(pygame.Rect(left, top-height, width, height), "Game over", manager)
        score_label = UILabel(pygame.Rect(left, top, width, height), "Your score is {}".format(self.__score), manager)
        pseudo_entry = UITextEntryLine(pygame.Rect(left, top+height, width, height), manager)
        submit_button = UIButton(pygame.Rect(left, top+ 2*height, width, height), "Submit !",manager)
        data = self.readJSON()
        #Optimiser ????????????????????????????????????
        #Afficher les 3 derniers...
        i=0
        for elem in data:
            UILabel(pygame.Rect(left, top+(i+3)*height, width, height), elem + str(data[elem]), manager)
            i +=1
        scoreboard = UILabel(pygame.Rect(left, top+(i+3)*height, width, height), "", manager)
        replay_buton = UIButton(pygame.Rect(0, self.__size[1]-height*2, width/2, height), "Replay",manager)
        exit_button = UIButton(pygame.Rect(0, self.__size[1]-height, width/2, height), "Exit",manager)

        breaker = False

        clock = pygame.time.Clock()

        while True:
            time_delta = clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    button = event.ui_element
                    if button == replay_buton: 
                        breaker = True
                    if button == exit_button:
                        sys.exit()
                    if button == submit_button and pseudo_entry.text != "":
                        pseudo = pseudo_entry.text
                        pseudo_entry.set_text("")
                        text = "{} {}".format(pseudo, self.__score)
                        scoreboard.set_text(text)
                        self.writeJSON(pseudo, self.__score)

                manager.process_events(event)
            
            manager.update(time_delta/1000)
            if breaker: break
            manager.draw_ui(self.__screen)
            pygame.display.flip()
        
        self.__cases = []
        self.run()


    def writeJSON(self, player, score):
        file = open("scoreboard.json", 'r')
        data = json.load(file)
        data[player] = score
        json.dump(data, open("scoreboard.json", 'w'))
        #Améliorer pour classer par score ?
        #Faire un classement par taille de grille de jeu ?

    def readJSON(self):
        file = open("scoreboard.json", 'r')
        return json.load(file)


Game().menu()
#Create a class Score ?
#Create a class End_game ?
#So that the snake class doesnt need the main class but only the score one.