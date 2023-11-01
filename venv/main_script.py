
import random
import math
import re

World_size = 20     #how big (box) do you want world to be
Simulation_Length = 15      #how many turns in simulation

#how many of each agents do you want, don't touch Original_num thats for post simulation debug
Num_dandelion = 80; Original_num_dandelion = Num_dandelion
Num_cow = 30; Original_num_Cow = Num_cow
Num_tiger = 30; Original_num_Tiger = Num_tiger


Reproduce_age = 5   #minimum age before can breed
Max_hunger_to_reproduce = 40    #at which hunger value is highest chance to breed
Base_reproduce_chance = 0.2     #maximum reproduce chance (at max hunger)

#---------------------------------------------------------------------------


#Check if world is big enough for all agents
SumAllAgents = Num_cow + Num_dandelion + Num_tiger
if pow(World_size, 2) < SumAllAgents:
    raise Exception("World can't be smaller than amount of objects to spawn")

#Generate the world X in Y, filled with None to show empty cells, starts from XY = 0, ends at at World_size - 1
World_agent_list_x_y = [[None for _ in range(World_size)] for _ in range(World_size)] #stores all agent instances
class Agent:
    def __init__(self, name, type, perception, speed, size):

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
        self.size = size
        self.age = 0;

        if self.size == "Small": #big animals need more food, spawns bigger animals with bigger reservoir
            self.hunger = 10
        elif self.size == "Medium":
            self.hunger = 15
        elif self.size == "Large":
            self.hunger = 20
        else:
            raise Exception("Not supposed agent size")

        self.FindFreeSpot()  # find a free spot to spawn

    def FindFreeSpot(self):
        self.x = random.randint(0, World_size-1)
        self.y = random.randint(0, World_size-1)

        #Loop until a free spot is found
        while World_agent_list_x_y[self.x][self.y] != None:
            self.x = random.randint(0, World_size-1)
            self.y = random.randint(0, World_size-1)
        World_agent_list_x_y[self.x][self.y] = self

    @staticmethod
    def RemoveAgent(agent): #Removes an agent from both the type list and agent list.
        World_agent_list_x_y[agent.x][agent.y] = None

        # Remove from respective list
        if "Cow" in agent.name:
            Cows_list.remove(agent)
        elif "Tiger" in agent.name:
            Tigers_list.remove(agent)
        # No need to remove plants from a list because they get respawned


    def SearchForFood(self): #Is called directly, handles Food, movement and roam
        directions_x_y = []
        if self.perception >= 1: #lowest perception, only sees up down left right
            directions_x_y.append([self.x + 1, self.y])  # right
            directions_x_y.append([self.x - 1, self.y])  # left
            directions_x_y.append([self.x, self.y + 1])  # up
            directions_x_y.append([self.x, self.y - 1])  # down
            random.shuffle(directions_x_y) #randomise choice selection

            for direction in directions_x_y:
                if direction[0] >= World_size or direction[1] >= World_size or direction[0] < 0 or direction[1] < 0: #prevents checking beyond edge of world
                    continue

                if World_agent_list_x_y[direction[0]][direction[1]] == None:

                    #print(f"{self.name} X: {self.x} Y: {self.y}  |  check X: {direction[0]} Y:{direction[1]}  |  found: None") #console log
                    continue
                #else:
                    #print(f"{self.name} [{self.x},{self.y}]  |  check: [{direction[0]},{direction[1]}]  |  found: {World_agent_list_x_y[direction[0]][direction[1]].name}")

                #if we found food, eat it and go there:

                if World_agent_list_x_y[direction[0]][direction[1]].type == self.food:
                    print(f"{self.name} found food! Food is: {World_agent_list_x_y[direction[0]][direction[1]].name}, Hunger: {self.hunger}") #Find specific instance to eat

                    if World_agent_list_x_y[direction[0]][direction[1]].type == "Plant": #if we just ate a plant:
                        self.Hunger(True, World_agent_list_x_y[direction[0]][direction[1]].size)  # track hunger levels, pass food that was eaten
                        World_agent_list_x_y[direction[0]][direction[1]].FindFreeSpot() #respawn plant

                    else:
                        self.Hunger(True, World_agent_list_x_y[direction[0]][direction[1]].size)  # track hunger levels, pass food that was eaten
                        Agent.RemoveAgent(World_agent_list_x_y[direction[0]][direction[1]])  # delete the agent being eaten

                    #update new position
                    World_agent_list_x_y[self.x][self.y] = None
                    World_agent_list_x_y[direction[0]][direction[1]] = self
                    self.x = direction[0]
                    self.y = direction[1]

                    return #end the search
        self.RandomMove(directions_x_y)
    def RandomMove(self, directions_x_y):
        if self.speed == 1: #simplest case, just move and end turn
            for direction in directions_x_y:
                if direction[0] >= World_size or direction[1] >= World_size or direction[0] < 0 or direction[1] < 0 or World_agent_list_x_y[direction[0]][direction[1]] != None:
                    continue # prevents moving beyond edge of world or into another Agent and fucking things up
                random.choice(directions_x_y)
                print(f"{self.name} moved from [{self.x},{self.y}] to [{direction[0]},{direction[1]}], Hunger: {self.hunger}")

                World_agent_list_x_y[self.x][self.y] = None
                World_agent_list_x_y[direction[0]][direction[1]] = self
                self.x = direction[0]
                self.y = direction[1]
                self.Hunger(False) #track hunger levels, didnt eat
                return

    def Hunger(self, ate=False, size="Small"):
        #Function to track Agents hunger level
        #If food was eaten, how much nourishment does it give
        if ate == True:
            if size == "Small":
                self.hunger = self.hunger + 4
            elif size == "Medium":
                self.hunger = self.hunger + 8
            else:
                self.hunger = self.hunger + 16 #big animals nourish for longer
            return #grace period, if food was found, don't use reserves or check for starvation
        #depending on Agent size, food depletes at different rate
        if self.size == "Small":
            self.hunger = self.hunger - 1 #lose 1 point worth of hunger
        elif self.size == "Medium":
            self.hunger = self.hunger - 2
        else:
            self.hunger = self.hunger - 4 #bigger animals need more food
        #starve
        if self.hunger <= 0:
            self.RemoveAgent(self) #starve
            return

    @staticmethod
    def HungerReproduceSigmoid(hunger):
        sigmoid_slope = 7.0
        hunger_factor = hunger / Max_hunger_to_reproduce  # Normalizes hunger between 0 and 1
        return round(1 / (1 + math.exp(-sigmoid_slope * (hunger_factor - 0.5))), 2) #more well fed, more chance to breed

    def Reproduce(self): #Is called directly, Handles reproducing and aging
        if pow(World_size, 2) < SumAllAgents:
            print("World too small to breed!")
            self.age = self.age + 1
            return
        if self.age > Reproduce_age:
            if Base_reproduce_chance * Agent.HungerReproduceSigmoid(self.hunger) <= round(random.random(), 2):
                if "Tiger" in self.name:

                    babyname = int(re.search(r"(\d+)$", self.name).group(1)) #use regular expression to extract the generation of parent
                    babyname = "Tiger_" + str(babyname+1) #make name with new generation number
                    newborn = SpawnTiger(name=babyname, perception=self.perception, speed=self.speed)
                elif "Cow" in self.name:

                    babyname = int(re.search(r"(\d+)$", self.name).group(1))
                    babyname = "Cow_" + str(babyname+1)
                    newborn = SpawnCow(name=babyname, perception=self.perception, speed=self.speed)
                print(f"{newborn.name} was born with perception {newborn.perception}, speed {newborn.speed}")
        self.age = self.age + 1




Cows_list = [] #initialise lists to store agents
Dandelion_list = []
Tigers_list = []

#Function to spawn agents
def SpawnDandelion(name="Dandelion_1", type="Plant", perception=0, speed=0, size="Small"): # input default name, type, perception, speed, size, unless overwritten by parent
    Dandelion = Agent(name, type, perception, speed, size)
    Dandelion_list.append(Dandelion)
    return Dandelion
def SpawnCow(name="Cow_1", type="Herbivore", perception=1, speed=1, size="Large"):
    Cow = Agent(name, type, perception, speed, size)
    Cows_list.append(Cow)
    return Cow
def SpawnTiger(name="Tiger_1", type="Carnivore", perception=1, speed=1, size="Large"):
    Tiger = Agent(name, type, perception, speed, size)
    Tigers_list.append(Tiger)
    return Tiger

#spawn amount of agents we want
for i in range(Num_dandelion):
    SpawnDandelion()

for i in range(Num_cow):
    SpawnCow()
for i in range(Num_tiger):
    SpawnTiger()

#console log
# for i in Cows_list:
#     print(f"Cows are at: X: {i.x} Y: {i.y}")
# for i in Dandelion_list:
#     print(f"Dandelions are at: X: {i.x} Y: {i.y}")
# for i in Tigers_list:
#     print(f"Tigers are at: X: {i.x} Y: {i.y}")
print(f"World started with {Num_dandelion} Dandelions, {Num_cow} Cows, and {Num_tiger} Tigers")
#simulate Simulation_Length turns (main loop)
for i in range(Simulation_Length):
    print(f"\n\n----------Turn {i+1}----------")
    print(f"There are: {len(Dandelion_list)} Dandelions, {len(Cows_list)} Cows, and {len(Tigers_list)} Tigers, Total: {SumAllAgents}\n\n")
    for cows in Cows_list[:]:   #This creates shallow copies of the lists, allowing processing of all animals even if some get deleted.
                                #This is because if animal is killed, list index will shift without updating current loop index, and make next
                                #animal be skipped from processing, causing bunch of bugs
        cows.SearchForFood()
        cows.Reproduce()
    print("")
    for tigers in Tigers_list[:]:
        tigers.SearchForFood()
        tigers.Reproduce()

    Num_cow = len(Cows_list)
    Num_dandelion = len(Dandelion_list)
    Num_tiger = len(Tigers_list)
    SumAllAgents = Num_cow + Num_dandelion + Num_tiger
#report results
print("\n\n----------SIMULATION END----------")
print(f"World started with {Original_num_dandelion} Dandelions, {Original_num_Cow} Cows, and {Original_num_Tiger} Tigers, Total: {(Original_num_Tiger + Original_num_dandelion + Original_num_Cow)}")
print(f"World ended with {Num_dandelion} Dandelions, {Num_cow} Cows, and {Num_tiger} Tigers, Total: {SumAllAgents}")