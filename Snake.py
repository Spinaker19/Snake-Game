class Snake():

    #direction -> (-1,0) =>Left
            # -> (0,-1) => UP
            # -> (1, 0) => Right
            # -> (0, 1) => Down 

    def __init__(self, direction, snake_cases, cases) -> None:
        self.__direction = direction
        self.__snake_cases = snake_cases #-> liste contenant les cases constituat le serpent
        self.__cases = cases #-> liste contenant toutes les cases

    def add(self, case):
        self.__snake_cases.append(case)

    def set_direction(self, direction):
        self.__direction = direction
    
    def get_direction(self):
        return self.__direction

    def draw(self, screen):
        for case in self.__snake_cases:
            case.draw(screen, (8, 255, 8))

    def move(self, screen):
        #Sans doute pas le plus opti

        #Get index of head case
        #modulo 20 to avoid out of bound
        index_x = self.__snake_cases[0].get_coord()[0]+self.__direction[0]
        index_y = self.__snake_cases[0].get_coord()[1]+self.__direction[1]
        self.__snake_cases.insert(0, self.__cases[index_x%20][index_y%20])
        
        self.draw(screen)

        #remove the last case of the snake -> avance
        print(self.__cases[index_x][index_y].is_fruit())
        if(not self.__cases[index_x][index_y].is_fruit()):
            self.__snake_cases[-1].draw(screen)
            self.__snake_cases.remove(self.__snake_cases[-1])
        