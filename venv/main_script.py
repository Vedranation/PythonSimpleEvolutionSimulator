
import random

world_size = 20 #how big (box) do you want world to be
Simulation_Length = 10 #how many turns in simulation
Num_dandelion = 60 #how many of each agents do you want
Num_cow = 15
Num_tiger = 15

if pow(world_size, 2) < Num_cow + Num_dandelion + Num_tiger: #Check if world is big enough for all agents
    raise Exception("World can't be smaller than amount of objects to spawn")

#Generate the world X in Y, filled with None to show empty cells, starts from XY = 0, ends at at world_size - 1
World_agent_list_x_y = [[None for _ in range(world_size)] for _ in range(world_size)] #stores all agent instances
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
        self.FindFreeSpot() #find a free spot to spawn
        self.size = size

        if self.size == "Small": #big animals need more food, spawns bigger animals with bigger reservoir
            self.hunger = 10
        elif self.size == "Medium":
            self.hunger = 15
        elif self.size == "Large":
            self.hunger = 20
        else:
            raise Exception("Not supposed agent size")

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

                if World_agent_list_x_y[direction[0]][direction[1]] == None:

                    #print(f"{self.name} X: {self.x} Y: {self.y}  |  check X: {direction[0]} Y:{direction[1]}  |  found: None") #console log
                    continue
                else:
                    print(f"{self.name} [{self.x},{self.y}]  |  check: [{direction[0]},{direction[1]}]  |  found: {World_agent_list_x_y[direction[0]][direction[1]].name}")

                #if we found food, eat it and go there:

                if World_agent_list_x_y[direction[0]][direction[1]].type == self.food:
                    print(f"Found food! Food is: {World_agent_list_x_y[direction[0]][direction[1]].name}, Hunger: {self.hunger}") #Find specific instance to eat

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
                if direction[0] >= world_size or direction[1] >= world_size or direction[0] < 0 or direction[1] < 0 or World_agent_list_x_y[direction[0]][direction[1]] != None:
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


Cows_list = [] #initialise lists to store agents
Dandelion_list = []
Tigers_list = []

#spawn agents
for i in range(Num_dandelion):
    Dandelion = Agent("Dandelion", "Plant", 0, 0, "Small") #input name, type, perception, speed, size
    Dandelion_list.append(Dandelion)
for i in range(Num_cow):
    Cow = Agent("Cow", "Herbivore", 1, 1, "Large")
    Cows_list.append(Cow)
for i in range(Num_tiger):
    Tiger = Agent("Tiger", "Carnivore", 1, 1, "Large")
    Tigers_list.append(Tiger)

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
    print(f"There are: {len(Dandelion_list)} Dandelions, {len(Cows_list)} Cows, and {len(Tigers_list)} Tigers\n\n")
    for cows in Cows_list[:]:   #This creates shallow copies of the lists, allowing processing of all animals even if some get deleted.
                                #This is because if animal is killed, list index will shift without updating current loop index, and make next
                                #animal be skipped from processing, causing bunch of bugs
        cows.SearchForFood()
    print("")
    for tigers in Tigers_list[:]:
        tigers.SearchForFood()

#report results
print(f"World ended with {len(Dandelion_list)} Dandelions, {len(Cows_list)} Cows, and {len(Tigers_list)} Tigers")