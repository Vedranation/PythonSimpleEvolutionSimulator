
import random

world_size = 20 #how big (box) do you want world to be
Simulation_Length = 2 #how many turns in simulation
Num_dandelion = 10 #how many of each agents do you want
Num_cow = 10
Num_tiger = 10

if pow(world_size, 2) < Num_cow + Num_dandelion + Num_tiger: #Check if world is big enough for all agents
    raise Exception("World can't be smaller than amount of objects to spawn")

#Generate the world X in Y, filled with None to show empty cells, starts from XY = 0, ends at at world_size - 1
World_agent_list_x_y = [[None for _ in range(world_size)] for _ in range(world_size)] #stores all agent instances
class Agent:
    def __init__(self, name, type, perception, speed):

        #Register what type of agent is bring created
        if type == "Plant":
            self.type = "Plant"
        elif type == "Herbivore":
            self.type = "Herbivore"
            self.food = "Plant"
        elif type == "Carnivore":
            self.type = "Carnivore"
            self.food = "Herbivore"
        else:
            raise Exception("Not supported agent type")

        self.perception = perception
        self.speed = speed
        self.name = name
        self.FindFreeSpot() #find a free spot to spawn

    def FindFreeSpot(self):
        self.x = random.randint(0, world_size-1)
        self.y = random.randint(0, world_size-1)

        #Loop until a free spot is found
        while World_agent_list_x_y[self.x][self.y] != None:
            self.x = random.randint(0, world_size-1)
            self.y = random.randint(0, world_size-1)
        World_agent_list_x_y[self.x][self.y] = self

    @staticmethod
    def RemoveAgent(agent):
        """
        Removes an agent from both the type list and agent list.
        """
        World_agent_list_x_y[agent.x][agent.y] = None

        # Remove from respective list
        if agent.name == "Cow":
            Cows_list.remove(agent)
        elif agent.name == "Tiger":
            Tigers_list.remove(agent)
        # No need to remove plants from a list because they get respawned


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
                empty = False
                if World_agent_list_x_y[direction[0]][direction[1]] == None:
                    empty = True
                    print(f"{self.name} X: {self.x} Y: {self.y}  |  check X: {direction[0]} Y:{direction[1]}  |  found: None") #console log
                    continue
                else:
                    print(f"{self.name} X: {self.x} Y: {self.y}  |  check X: {direction[0]} Y:{direction[1]}  |  found: {World_agent_list_x_y[direction[0]][direction[1]].name}")

                #if we found food, eat it and go there:

                if World_agent_list_x_y[direction[0]][direction[1]].type == self.food:
                    print(f"Found food! Food is: {World_agent_list_x_y[direction[0]][direction[1]].name}") #Find specific instance to eat

                    if World_agent_list_x_y[direction[0]][direction[1]].type == "Plant": #if we just ate a plant:
                        World_agent_list_x_y[direction[0]][direction[1]].FindFreeSpot() #respawn plant
                    else:
                        Agent.RemoveAgent(World_agent_list_x_y[direction[0]][direction[1]])  # for the agent being eaten

                    World_agent_list_x_y[self.x][self.y] = None
                    World_agent_list_x_y[direction[0]][direction[1]] = self
                    self.x = direction[0]
                    self.y = direction[1]

                    break #end the search


Cows_list = [] #initialise lists to store agents
Dandelion_list = []
Tigers_list = []

#spawn agents
for i in range(Num_dandelion):
    Dandelion = Agent("Dandelion", "Plant", 0, 0) #input name, type, perception, speed
    Dandelion_list.append(Dandelion)
for i in range(Num_cow):
    Cow = Agent("Cow", "Herbivore", 1, 1)
    Cows_list.append(Cow)
for i in range(Num_tiger):
    Tiger = Agent("Tiger", "Carnivore", 1, 1)
    Tigers_list.append(Tiger)

#console log
for i in Cows_list:
    print(f"Cows are at: X: {i.x} Y: {i.y}")
for i in Dandelion_list:
    print(f"Dandelions are at: X: {i.x} Y: {i.y}")
for i in Tigers_list:
    print(f"Tigers are at: X: {i.x} Y: {i.y}")
print(f"World started with {Num_dandelion} Dandelions, {Num_cow} Cows, and {Num_tiger} Tigers")
#simulate Simulation_Length turns (main loop)
for i in range(Simulation_Length):
    print(f"\nTurn {i+1}\n")
    for cows in Cows_list:
        cows.SearchForFood()
    print("\n")
    for tigers in Tigers_list:
        tigers.SearchForFood()

#report results
print(f"World ended with {len(Dandelion_list)} Dandelions, {len(Cows_list)} Cows, and {len(Tigers_list)} Tigers")