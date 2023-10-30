
import random

world_size = 20 #how big (box) do you want world to be


#Generate the world X in Y, filled with None to show empty cells, starts from XY = 0, ends at at world_size - 1
World_list_x_y = [[None for _ in range(world_size)] for _ in range(world_size)]

class Agent:
    def __init__(self, type, perception, speed):

        #Register what type of agent is bring created
        if type == "Plant":
            self.type = "Plant"
        elif type == "Herbivore":
            self.type = "Herbivore"
        elif type == "Carnivore":
            self.type = "Carnivore"
        else:
            raise Exception("Not supported agent type")

        self.perception = perception
        self.speed = speed

        self.FindFreeSpot() #find a free spot to spawn

    def FindFreeSpot(self):
        self.x = random.randint(0, world_size-1)
        self.y = random.randint(0, world_size-1)

        #Loop until a free spot is found
        while World_list_x_y[self.x][self.y] != None:
            self.x = random.randint(0, world_size-1)
            self.y = random.randint(0, world_size-1)
        World_list_x_y[self.x][self.y] = self.type
        return self.x, self.y

    def SearchForFood(self):
        directions_x_y = []
        if self.perception >= 1: #lowest perception, only sees up down left right
            directions_x_y.append([self.x + 1, self.y])  # right
            directions_x_y.append([self.x - 1, self.y])  # left
            directions_x_y.append([self.x, self.y + 1])  # up
            directions_x_y.append([self.x, self.y - 1])  # down
            random.shuffle(directions_x_y) #randomise choice selection

            for direction in directions_x_y:
                if direction[0] >= world_size or direction[1] >= world_size or direction[0] < 0 or direction[1] < 0: #prevents checking beyond edge of world
                    continue
                print(f"Cow X: {self.x} Y: {self.y}  |  check X: {direction[0]} Y:{direction[1]}  |  found: {World_list_x_y[direction[0]][direction[1]]}")



num_dandelion = 10 #how many of each agents do you want
num_cow = 5
Cows_list = []
Dandelion_list = []

if pow(world_size, 2) < num_cow + num_dandelion: #Check if world is big enough
    raise Exception("World can't be smaller than amount of objects to spawn")

#spawn agents
for i in range(num_dandelion):
    Dandelion = Agent("Plant", 0, 0) #input type, perception, speed
    Dandelion_list.append(Dandelion)
for i in range(num_cow):
    Cow = Agent("Herbivore", 1, 1)
    Cows_list.append(Cow)

for i in Cows_list:
    print(f"Cows are at: X: {i.x} Y: {i.y}")
for i in Dandelion_list:
    print(f"Dandelions are at: X: {i.x} Y: {i.y}")

#simulate 1 turn

for cows in Cows_list:
    cows.SearchForFood()
