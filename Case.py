import pygame

class Case():
    
    def __init__(self, size, color, coord_pixels, coord) -> None:
        self.__size = size
        self.__color = color
        self.__coord_pixels = coord_pixels
        self.__coord = coord
        self.__is_snake = False
        self.__is_fruit = False
        self.__is_spoiled = False

    def set_color(self, color):
        self.__color = color

    def get_coord(self):
        return self.__coord

    def set_is_fruit(self, bool):
        self.__is_fruit = bool

    def is_fruit(self):
        return self.__is_fruit

    def set_is_spoiled(self, bool):
        self.__is_spoiled = bool

    def is_spoiled(self):
        return self.__is_spoiled
    
    def is_snake(self):
        return self.__is_snake

    def set_is_snake(self,bool):
        self.__is_snake = bool

    def __str__(self) -> str:
        return '({}, {})'.format(self.__coord[0], self.__coord[1])
    
    #Print les infos quand l'objet est dans une liste
    #Peut être enlever à la fin du projet -> pratique pour dev
    def __repr__(self):
        return str(self)

    def draw(self, screen, color=None):
        if color == None: color = self.__color
        pygame.draw.rect(screen, color, pygame.Rect(self.__coord_pixels[0], self.__coord_pixels[1], self.__size, self.__size))