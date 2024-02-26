
import random
import math
import re
import time

import ConsoleLog
import VisualiseScript

World_size = 20     #how big (box) do you want the world to be1
Simulation_Length = 200     #how many turns in simulation

#how many of each agents do you want to start with, stores their numbers each turn
Num_dandelion = [50];
#TODO: add Num_berrybush = [30];
#TODO: add Num_fox = [30];
#fixme: Make it that rabbits can't eat apple trees or they'll be unstoppable
Num_cow = [20];
Num_rabbit = [10];
Num_tiger = [10];
Num_wolf = [5];
#fixme: Random bug that makes animals (tigers and wolves) not insta starve and instead linger for hundreds of turns, avg hunger staying almost same, seems to be bug in order or hunger starvation (animal spawn with negative hunger)
Max_flowers = 30       #how many flowers can be
GrowthPerTurn = 3      #how many flowers spawn per turn
Maximum_hunger = 50     #maximum hunger a creature can have in its belly
Reproduce_age = 5   #minimum age before can breed
Max_hunger_to_reproduce = 40    #at which hunger value is highest chance to breed
Base_reproduce_chance = 0.75     #maximum reproduce chance (at max hunger)
DeathAge = 30       #at how old do animals 100% die (sigmoid)
World_size_spawn_tolerance = 1.03      #tolerance to world size to prevent overpopulation
Personal_animal_limit = pow(World_size, 2) * 0.7       #how much % of the world can a single population have before its forbidden from spawning
Predator_bigger_prey_fight_chance = 0.5     #for prey 1 size larger, chance to fight it. This is 1/5 worth for 2 size larger
Predator_bigger_prey_win_chance = 0.6       #for prey 1 size larger, chance for predator to kill it, else it dies. This is 1/5 worth for 2 size larger
Well_fed_buff = 0.2        #at maximum hunger, preys base chance for victory is multiplied by this much
Animal_breed_cooldown = 1

Window_width = 800
Window_height = 800

Console_log_start_position = False
Console_log_check_for_food = False
Console_log_found_food = False
Console_log_was_eaten = False
Console_log_death_starvation = False
Console_log_death_oldage = False
Console_log_death_battle = False
Console_log_born = True
Console_log_random_move = False
Console_log_reproduce_chance = True
Console_log_fight_big = False
Console_log_worldtoosmalltobreed = False

Visualise_population_toggle = True
Visualise_hunger_toggle = False
Visualise_simulation_toggle = True

Sim_speed = 0

#---------------------------------------------------------------------------

if Visualise_simulation_toggle == True:
    VisualiseScript.VisualiseSimulationInit(width=Window_width, height=Window_height, worldsize=World_size)


DiedInBattle = False
#Check if world is big enough for all agents
SumAllAgents = [Num_cow[-1]+Num_dandelion[-1]+Num_tiger[-1]+Num_wolf[-1]+Num_rabbit[-1]]
if pow(World_size, 2) < SumAllAgents[-1]:
    raise Exception("World can't be smaller than amount of objects to spawn")

#Generate the world X in Y, filled with None to show empty cells, starts from XY = 0, ends at at World_size - 1
World_agent_list_x_y = [[None for _ in range(World_size)] for _ in range(World_size)] #stores all agent instances
class Agent:
    def __init__(self, name, type, perception, speed, size, hunger):

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
        self.age = 1
        self.breedcooldown = 0

        if self.type != "Plant":
            if self.size == "Small": #gives babies 1 turn worth of food
                self.hunger = hunger + 0
            elif self.size == "Medium":
                self.hunger = hunger + 0
            elif self.size == "Large":
                self.hunger = hunger + 0
            else:
                raise Exception("Not supported agent size")

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
        elif "Rabbit" in agent.name:
            Rabbits_list.remove(agent)
        elif "Tiger" in agent.name:
            Tigers_list.remove(agent)
        elif "Dandelion" in agent.name:
            Dandelion_list.remove(agent)
        elif "Wolf" in agent.name:
            Wolf_list.remove(agent)



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
                    ConsoleLog.CheckForFood(self, direction[0], direction[1], True, World_agent_list_x_y, Console_log_check_for_food)
                    continue
                else:
                    ConsoleLog.CheckForFood(self, direction[0], direction[1], False, World_agent_list_x_y, Console_log_check_for_food)

                #if we found food, eat it and go there:
                if World_agent_list_x_y[direction[0]][direction[1]].type == self.food:
                    if self.FightOrFlight(World_agent_list_x_y[direction[0]][direction[1]]) == True:   #check prey size, if prey is bigger chance to fight it is smaller

                        if self.Fight(World_agent_list_x_y[direction[0]][direction[1]]) == True:    #predator won and ate the meal

                            self.Hunger(True, World_agent_list_x_y[direction[0]][direction[1]].size, direction)  # track hunger levels, pass food that was eaten
                            Agent.RemoveAgent(World_agent_list_x_y[direction[0]][direction[1]])  # delete the agent being eaten

                            #update new position
                            World_agent_list_x_y[self.x][self.y] = None
                            World_agent_list_x_y[direction[0]][direction[1]] = self
                            self.x = direction[0]
                            self.y = direction[1]

                            return #end the search
                        else:   #predator lost and died
                            global DiedInBattle
                            DiedInBattle = True #pass this to main loop
                            return
                    else:
                        continue #prey not worth the risk, keep searching
        self.RandomMove(directions_x_y)
    def RandomMove(self, directions_x_y):
        if self.speed == 1: #simplest case, just move and end turn
            for direction in directions_x_y:
                if direction[0] >= World_size or direction[1] >= World_size or direction[0] < 0 or direction[1] < 0 or World_agent_list_x_y[direction[0]][direction[1]] != None:
                    continue # prevents moving beyond edge of world or into another Agent and fucking things up
                random.choice(directions_x_y)
                ConsoleLog.RandomMove(self, direction[0], direction[1], Console_log_random_move)

                World_agent_list_x_y[self.x][self.y] = None
                World_agent_list_x_y[direction[0]][direction[1]] = self
                self.x = direction[0]
                self.y = direction[1]
                self.Hunger(False) #track hunger levels, didnt eat
                return
    def FightOrFlight(self, prey_agent):
        '''The less hunger, more desperate for a meal, at 50% hunger the modifier becomes 1, above 50% hunger it probably wont risk, below it will'''
        if prey_agent.type == "Plant":
            return True     #plants don't fight back
        desperation = 0.5 / (self.hunger / Maximum_hunger)
        preySize = prey_agent.size
        preyType = prey_agent.type

        if (self.size == "Small" and preySize == "Medium") or (self.size == "Medium" and preySize == "Large") and preyType != "Plant": #1 size difference
            if round(random.random(), 2) <= Predator_bigger_prey_fight_chance * desperation:
                return True #predator will fight
            else:
                return False    #predator doesn't fight
        elif (self.size == "Small" and preySize == "Large") and preyType != "Plant": #2 size difference
            if round(random.random(), 2) <= (Predator_bigger_prey_fight_chance/5) * desperation:    # predator is VERY unlikely to fight
                return True
            else:
                return False  # predator doesn't fight
        else:
            return True #large can eat anything
    def Fight(self, prey_agent):
        '''at 50% hunger prey has 50% Well_fed_buff worth'''
        if prey_agent.type == "Plant":
            return True     #plants don't fight back

        prey_power = round(Well_fed_buff * (prey_agent.hunger / Maximum_hunger), 2)     #Well fed prey gets a boost to their combat power
        if (self.size == "Small" and prey_agent.size == "Medium") or (self.size == "Medium" and prey_agent.size == "Large"): #1 size difference
            total_win_chance = round(Predator_bigger_prey_win_chance - prey_power * Predator_bigger_prey_win_chance, 2)
            if round(random.random(), 2) <= (total_win_chance):

                ConsoleLog.FightBig(self, prey_agent, total_win_chance, prey_power, Console_log_fight_big)
                return True #predator won the fight
            else:
                ConsoleLog.DiedInBattle(self, prey_agent.name, Console_log_death_battle)
                return False    #predator lost the fight and died

        elif (self.size == "Small" and prey_agent.size == "Large"):       #probably suicide for small guy but let him try
            total_win_chance = round((Predator_bigger_prey_win_chance/5 - prey_power * (Predator_bigger_prey_win_chance/5)), 2)
            if round(random.random(), 2) <= (total_win_chance):
                    ConsoleLog.FightBig(self, prey_agent, total_win_chance, prey_power, Console_log_fight_big)

                    return True #David beat the goliath
            else:
                ConsoleLog.DiedInBattle(self, prey_agent.name, Console_log_death_battle)
                return False    #predator lost the fight and died
        else:
            return True #large predator automatically wins



    def Hunger(self, ate=False, preySize="Small", direction=[69, 69]):
        #Function to track Agents hunger level
        #If food was eaten, how much nourishment does it give
        if ate == True:
            if preySize == "Small":
                worth = 6
                ConsoleLog.AgentWasEaten(self, direction[0], direction[1], World_agent_list_x_y, worth, Console_log_was_eaten)
                ConsoleLog.FoundFood(self, direction[0], direction[1], World_agent_list_x_y, worth, Console_log_found_food)
                self.hunger = self.hunger + worth

            elif preySize == "Medium":
                worth = 9
                ConsoleLog.AgentWasEaten(self, direction[0], direction[1], World_agent_list_x_y, worth, Console_log_was_eaten)
                ConsoleLog.FoundFood(self, direction[0], direction[1], World_agent_list_x_y, worth, Console_log_found_food)
                self.hunger = self.hunger + worth
            else:
                worth = 26
                ConsoleLog.AgentWasEaten(self, direction[0], direction[1], World_agent_list_x_y, worth, Console_log_was_eaten)
                ConsoleLog.FoundFood(self, direction[0], direction[1], World_agent_list_x_y, worth, Console_log_found_food)
                self.hunger = self.hunger + worth #big animals nourish for longer
            if self.hunger > Maximum_hunger:
                self.hunger = Maximum_hunger
            return #grace period, if food was found, don't use reserves or check for starvation

        #depending on Agent size, food depletes at different rate
        if self.size == "Small":
            self.hunger = self.hunger - 1 #lose 1 point worth of hunger
        elif self.size == "Medium":
            self.hunger = self.hunger - 2
        else:
            self.hunger = self.hunger - 4 #bigger animals need more food


    @staticmethod
    def HungerReproduceSigmoid(hunger):
        sigmoid_slope = 7.0
        hunger_factor = hunger / Max_hunger_to_reproduce  # Normalizes hunger between 0 and 1
        return round(1 / (1 + math.exp(-sigmoid_slope * (hunger_factor - 0.5))), 2) #more well fed, more chance to breed

    def Starvation_Age_Battle_Death(self, DiedInBattle=False):
        '''Handles all kinds of deaths'''
        self.age = self.age + 1

        if DiedInBattle == True:
            self.RemoveAgent(self) #Cow killed you bro
            return

        if self.hunger <= 0:
            ConsoleLog.DeathStarvation(self, Console_log_death_starvation)
            self.RemoveAgent(self) #starve
            return
        else:
            sigmoid_slope = 20.0
            death_factor = self.age / DeathAge  # Normalizes chance to die between 0 and 1

            if round(1 / (1 + math.exp(-sigmoid_slope * (death_factor - 0.5))), 2) >= round(random.random(), 2):  # older you are, more likely to perish
                ConsoleLog.DeathOldAge(self, Console_log_death_oldage)
                self.RemoveAgent(self)  # die of old age
            return

    def Reproduce(self): #Is called directly, Handles reproducing and aging

        if self.age > Reproduce_age:
            if self.breedcooldown > 0:      #Introduces a breeding cooldown
                self.breedcooldown = self.breedcooldown - 1
                return
            else:
                self.breedcooldown = Animal_breed_cooldown

            sigm = Agent.HungerReproduceSigmoid(self.hunger)
            rnd = round(random.random(), 2)
            mult = round(Base_reproduce_chance * sigm, 2)

            ConsoleLog.ReproduceChance(self, Base_reproduce_chance, sigm, mult, rnd, Console_log_reproduce_chance)
            if rnd <= mult:

                UpdatedAnimalSum = len(Tigers_list) + len(Dandelion_list) + len(Cows_list) + len(Wolf_list) + len(Rabbits_list) #need to update this when adding more animals

                if pow(World_size, 2) < (round(UpdatedAnimalSum * World_size_spawn_tolerance, 1)):

                    ConsoleLog.WorldTooSmallTooBreed(Console_log_worldtoosmalltobreed)
                    return

                elif "Tiger" in self.name:
                    if len(Tigers_list) > Personal_animal_limit:
                        print("Tigers have reached population limit")
                        return
                    babyname = int(re.search(r"(\d+)$", self.name).group(1)) #use regular expression to extract the generation of parent
                    babyname = "Tiger_" + str(babyname+1) #make name with new generation number
                    newborn = SpawnTiger(name=babyname, perception=self.perception, speed=self.speed, hunger=self.hunger)
                elif "Cow" in self.name:
                    if len(Cows_list) > Personal_animal_limit:
                        print("Cows have reached population limit")
                        return
                    babyname = int(re.search(r"(\d+)$", self.name).group(1))
                    babyname = "Cow_" + str(babyname+1)
                    newborn = SpawnCow(name=babyname, perception=self.perception, speed=self.speed, hunger=self.hunger)
                elif "Rabbit" in self.name:
                    if len(Rabbits_list) > Personal_animal_limit:
                        print("Rabbits have reached population limit")
                        return
                    babyname = int(re.search(r"(\d+)$", self.name).group(1))
                    babyname = "Rabbit_" + str(babyname+1)
                    newborn = SpawnRabbit(name=babyname, perception=self.perception, speed=self.speed, hunger=self.hunger)
                elif "Wolf" in self.name:
                    if len(Wolf_list) > Personal_animal_limit:
                        print("Wolves have reached population limit")
                        return
                    babyname = int(re.search(r"(\d+)$", self.name).group(1)) #use regular expression to extract the generation of parent
                    babyname = "Wolf_" + str(babyname+1) #make name with new generation number
                    newborn = SpawnWolf(name=babyname, perception=self.perception, speed=self.speed, hunger=self.hunger)
                ConsoleLog.Born(newborn, Console_log_born)

        def Mutate():
            #todo: gene evo mutate func
            return




Cows_list = [] #initialise lists to store agents
Rabbits_list = []
Dandelion_list = []
Tigers_list = []
Wolf_list = []

Cows_hunger = [] #stores average hunger values every turn
Rabbits_hunger = []
Tigers_hunger = []
Wolf_hunger = []
def CalculateAverageHunger(animal_list):
    average = 0
    for i in animal_list:
        average = average + i.hunger
    if len(animal_list) == 0:
        return 0
    average = average / len(animal_list)
    return round(average, 1)
#Function to spawn agents
def SpawnDandelion(name="Dandelion_1", type="Plant", perception=0, speed=0, size="Small", hunger=20): # input default name, type, perception, speed, size, and starting hunger, unless overwritten by parent
    Dandelion = Agent(name, type, perception, speed, size, hunger)
    Dandelion_list.append(Dandelion)
    return Dandelion
def SpawnCow(name="Cow_1", type="Herbivore", perception=1, speed=1, size="Large", hunger=25):
    Cow = Agent(name, type, perception, speed, size, hunger)
    Cows_list.append(Cow)
    return Cow
def SpawnRabbit(name="Rabbit_1", type="Herbivore", perception=1, speed=1, size="Small", hunger=25):
    Rabbit = Agent(name, type, perception, speed, size, hunger)
    Rabbits_list.append(Rabbit)
    return Rabbit
def SpawnTiger(name="Tiger_1", type="Carnivore", perception=1, speed=1, size="Large", hunger=25):
    Tiger = Agent(name, type, perception, speed, size, hunger)
    Tigers_list.append(Tiger)
    return Tiger
def SpawnWolf(name="Wolf_1", type="Carnivore", perception=1, speed=1, size="Medium", hunger=25):
    Wolf = Agent(name, type, perception, speed, size, hunger)
    Wolf_list.append(Wolf)
    return Wolf
def RespawnVegetation():
    # respawn plants every turn
    UpdatedAnimalSum = len(Tigers_list) + len(Dandelion_list) + len(Cows_list) + len(Wolf_list) + len(Rabbits_list)  # need to update this when adding more animals

    if pow(World_size, 2) < (round(UpdatedAnimalSum * World_size_spawn_tolerance, 1)):
        print("World too small to grow!")
        return
    if Num_dandelion[-1]+GrowthPerTurn <= Max_flowers:
        for j in range(GrowthPerTurn):
            SpawnDandelion()
    elif (Num_dandelion[-1]+GrowthPerTurn/2) <= Max_flowers: #spawns half
        for j in range(round(GrowthPerTurn/2)):
            SpawnDandelion()
    else:
        return


#spawn amount of agents we want
for i in range(Num_dandelion[0]):
    SpawnDandelion()

for i in range(Num_cow[0]):
    SpawnCow()
for i in range(Num_rabbit[0]):
    SpawnRabbit()
for i in range(Num_tiger[0]):
    SpawnTiger()
for i in range(Num_wolf[0]):
    SpawnWolf()


print(f"World started with {Num_dandelion[0]} Dandelions, {Num_cow[0]} Cows, {Num_rabbit[0]} Rabbits, {Num_wolf[0]} Wolves and {Num_tiger[0]} Tigers")
ConsoleLog.StartPosition(Cows_list, Dandelion_list, Tigers_list, Wolf_list, Rabbits_list, Console_log_start_position)



#simulate Simulation_Length turns (main loop)
for i in range(Simulation_Length):

    RespawnVegetation()

    print(f"\n\n----------Turn {i+1}----------")
    print(f"There are: {len(Dandelion_list)} Dandelions, {len(Cows_list)} Cows, {len(Rabbits_list)} Rabbits, {len(Wolf_list)} Wolves, and {len(Tigers_list)} Tigers, Total: {SumAllAgents[-1]}\n\n")
    for cows in Cows_list[:]:   #This creates shallow copies of the lists, allowing processing of all animals even if some get deleted.
                                #This is because if animal is killed, list index will shift without updating current loop index, and make next
                                #animal be skipped from processing, causing bunch of bugs
        cows.SearchForFood()
        cows.Reproduce()
        cows.Starvation_Age_Battle_Death()

    print("")
    for rabbits in Rabbits_list[:]:
        rabbits.SearchForFood()
        rabbits.Reproduce()
        rabbits.Starvation_Age_Battle_Death()
    for tigers in Tigers_list[:]:
        DiedInBattle = False
        tigers.SearchForFood()
        if DiedInBattle == False:
            tigers.Reproduce()
            tigers.Starvation_Age_Battle_Death()
        else:
            tigers.Starvation_Age_Battle_Death(DiedInBattle=True)
    print("")
    for wolves in Wolf_list[:]:
        wolves.SearchForFood()
        if DiedInBattle == False:
            wolves.Reproduce()
            wolves.Starvation_Age_Battle_Death()
        else:
            wolves.Starvation_Age_Battle_Death(DiedInBattle=True)

    Num_cow.append(len(Cows_list))
    Num_dandelion.append(len(Dandelion_list))
    Num_tiger.append(len(Tigers_list))
    Num_wolf.append(len(Wolf_list))
    Num_rabbit.append(len(Rabbits_list))
    SumAllAgents.append(Num_dandelion[-1] + Num_cow[-1] + Num_tiger[-1] + Num_wolf[-1] + Num_rabbit[-1])

    Cows_hunger.append(CalculateAverageHunger(Cows_list))
    Tigers_hunger.append(CalculateAverageHunger(Tigers_list))
    Rabbits_hunger.append(CalculateAverageHunger(Rabbits_list))
    Wolf_hunger.append(CalculateAverageHunger(Wolf_list))

    if Visualise_simulation_toggle:
        VisualiseScript.VisualiseSimulationDraw(SumAllAgents, World_agent_list_x_y) #draw the display window
        time.sleep(Sim_speed)


#report results
print("\n\n----------SIMULATION END----------")
print(f"World started with {Num_dandelion[0]} Dandelions, {Num_cow[0]} Cows, {Num_rabbit[0]} Rabbits, {Num_wolf[0]} Wolves, and {Num_tiger[0]} Tigers, Total: {(SumAllAgents[0])}")
print(f"World ended at turn {Simulation_Length} with {Num_dandelion[-1]} Dandelions, {Num_cow[-1]} Cows, {Num_rabbit[-1]} Rabbits, {Num_wolf[-1]} Wolves, and {Num_tiger[-1]} Tigers, Total: {SumAllAgents[-1]}/{pow(World_size, 2) // World_size_spawn_tolerance}")

VisualiseScript.VisualisePopulation(Simulation_Length, Num_cow, Num_tiger, Num_dandelion, Num_wolf, Num_rabbit, Visualise_population_toggle)
VisualiseScript.VisualiseHunger(Simulation_Length, Cows_hunger, Rabbits_hunger, Tigers_hunger, Wolf_hunger, Visualise_hunger_toggle)

VisualiseScript.VisualiseSimulationQuit()