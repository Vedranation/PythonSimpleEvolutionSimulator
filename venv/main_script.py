
import random

world_size = 20 #how big (box) do you want world to be

#Generate the world X in Y, filled with None to show empty cells, starts from XY = 0

World_list_x_y = [[None for _ in range(world_size)] for _ in range(world_size)]

print(World_list_x_y[0][0]) #Check coordinates X=13 Y=7

class Agent:
    def __init__(self, who):

        #Register what type of agent is bring created
        if who == "Plant":
            self.who = "Plant"
        elif who == "Herbivore":
            self.who = "Herbivore"
        elif who == "Carnivore":
            self.who = "Carnivore"
        else:
            raise Exception("Not supported agent type")


        self.FindFreeSpot()


    def FindFreeSpot(self):
        self.x = random.randint(0, world_size-1)
        self.y = random.randint(0, world_size-1)

        #Loop until a free spot is found
        while World_list_x_y[self.x][self.y] != None:
            self.x = random.randint(0, world_size-1)
            self.y = random.randint(0, world_size-1)
        World_list_x_y[self.x][self.y] = self.who
        return self.x, self.y


Plant = Agent("Plant")
Rhino = Agent("Herbivore")

