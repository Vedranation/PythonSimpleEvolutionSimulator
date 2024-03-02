
import random
import math
import re
import time

import ConsoleLog
import VisualiseScript
import GlobalsStateManager

GSM = GlobalsStateManager.GlobalsManager #Encapsulate all globals

#how many of each agents do you want to start with, stores their numbers each turn

#TODO: add Num_berrybush = [30];

#TODO: add Num_goat = [30];
#TODO: add stone or impassable terrain
#TODO: make animals babies spawn near parents
#TODO: make predators able to see fleeing prey
#TODO: refactor globals
#TODO: move Agent to its own script

#---------------------------------------------------------------------------

if GSM.Visualise_simulation_toggle == True:
    VisualiseScript.VisualiseSimulationInit(GSM)


DiedInBattle = False
#Check if world is big enough for all agents
GSM.SumAllAgents = [GSM.Num_cow[-1]+GSM.Num_dandelion[-1]+GSM.Num_tiger[-1]+GSM.Num_wolf[-1]+GSM.Num_rabbit[-1]+GSM.Num_appletree[-1]+GSM.Num_fox[-1]]
if pow(GSM.World_size, 2) < GSM.SumAllAgents[-1]:
    raise Exception("World can't be smaller than amount of objects to spawn")

#Generate the world X in Y, filled with None to show empty cells, starts from XY = 0, ends at at GSM.World_size - 1
GSM.World_agent_list_x_y = [[None for _ in range(GSM.World_size)] for _ in range(GSM.World_size)] #stores all agent instances
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
            if self.size == "Small": #gives babies 1 turn worth of food - can cause numeric instability
                self.hunger = hunger + 0
            elif self.size == "Medium":
                self.hunger = hunger + 0
            elif self.size == "Large":
                self.hunger = hunger + 0
            else:
                raise Exception("Not supported agent size")

        self.FindFreeSpot()  # find a free spot to spawn

    def FindFreeSpot(self):
        self.x = random.randint(0, GSM.World_size-1)
        self.y = random.randint(0, GSM.World_size-1)

        #Loop until a free spot is found
        while GSM.World_agent_list_x_y[self.x][self.y] != None:
            self.x = random.randint(0, GSM.World_size-1)
            self.y = random.randint(0, GSM.World_size-1)
        GSM.World_agent_list_x_y[self.x][self.y] = self

    @staticmethod
    def RemoveAgent(agent): #Removes an agent from both the type list and agent list.
        GSM.World_agent_list_x_y[agent.x][agent.y] = None

        # Remove from respective list
        if "Cow" in agent.name:
            GSM.Cows_list.remove(agent)
        elif "Rabbit" in agent.name:
            GSM.Rabbits_list.remove(agent)
        elif "Tiger" in agent.name:
            GSM.Tigers_list.remove(agent)
        elif "Dandelion" in agent.name:
            GSM.Dandelion_list.remove(agent)
        elif "Wolf" in agent.name:
            GSM.Wolf_list.remove(agent)
        elif "Appletree" in agent.name:
            GSM.Appletree_list.remove(agent)
        elif "Fox" in agent.name:
            GSM.Fox_list.remove(agent)



    def SearchForFood(self): #Is called directly, handles Food, movement and roam
        directions_x_y = []
        if self.perception >= 1: #lowest perception, only sees up down left right
            directions_x_y.append([self.x + 1, self.y])  # right
            directions_x_y.append([self.x - 1, self.y])  # left
            directions_x_y.append([self.x, self.y + 1])  # up
            directions_x_y.append([self.x, self.y - 1])  # down
            random.shuffle(directions_x_y) #randomise choice selection

            for direction in directions_x_y:
                if direction[0] >= GSM.World_size or direction[1] >= GSM.World_size or direction[0] < 0 or direction[1] < 0: #prevents checking beyond edge of world
                    continue

                if GSM.World_agent_list_x_y[direction[0]][direction[1]] == None:
                    ConsoleLog.CheckForFood(self, direction[0], direction[1], True, GSM.World_agent_list_x_y, GSM.Console_log_check_for_food)
                    continue
                else:
                    ConsoleLog.CheckForFood(self, direction[0], direction[1], False, GSM.World_agent_list_x_y, GSM.Console_log_check_for_food)

                #if we found food, eat it and go there:
                if GSM.World_agent_list_x_y[direction[0]][direction[1]].type == self.food:
                    if self.food == "Plant": #herbivore eat
                        if self.HerbivoreNoEatBig(GSM.World_agent_list_x_y[direction[0]][direction[1]]) == True:
                            self.Hunger(True, GSM.World_agent_list_x_y[direction[0]][direction[1]].size,
                                        direction)  # track hunger levels, pass food that was eaten
                            Agent.RemoveAgent(
                                GSM.World_agent_list_x_y[direction[0]][direction[1]])  # delete the agent being eaten

                            # update new position
                            GSM.World_agent_list_x_y[self.x][self.y] = None
                            GSM.World_agent_list_x_y[direction[0]][direction[1]] = self
                            self.x = direction[0]
                            self.y = direction[1]
                            return  # end the search
                        else:
                            continue #small herbivores don't eat bigger size food

                    if self.FightOrFlight(GSM.World_agent_list_x_y[direction[0]][direction[1]]) == True:   #carnivore eat: check prey size, if prey is bigger chance to fight it is smaller

                        if self.Fight(GSM.World_agent_list_x_y[direction[0]][direction[1]]) == True:    #predator won and ate the meal

                            self.Hunger(True, GSM.World_agent_list_x_y[direction[0]][direction[1]].size, direction)  # track hunger levels, pass food that was eaten
                            Agent.RemoveAgent(GSM.World_agent_list_x_y[direction[0]][direction[1]])  # delete the agent being eaten

                            #update new position
                            GSM.World_agent_list_x_y[self.x][self.y] = None
                            GSM.World_agent_list_x_y[direction[0]][direction[1]] = self
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
                if direction[0] >= GSM.World_size or direction[1] >= GSM.World_size or direction[0] < 0 or direction[1] < 0 or GSM.World_agent_list_x_y[direction[0]][direction[1]] != None:
                    continue # prevents moving beyond edge of world or into another Agent and fucking things up
                random.choice(directions_x_y)
                ConsoleLog.RandomMove(self, direction[0], direction[1], GSM.Console_log_random_move)

                GSM.World_agent_list_x_y[self.x][self.y] = None
                GSM.World_agent_list_x_y[direction[0]][direction[1]] = self
                self.x = direction[0]
                self.y = direction[1]
                self.Hunger(False) #track hunger levels, didnt eat
                return
    def HerbivoreNoEatBig(self, plant_agent):
        'simple function to ensure all herbivores only eat food same size or smaller'
        if self.size == "Large":
            return True
        elif self.size == "Medium":
            if plant_agent.size == "Large":
                return False
            else:
                return True
        else:
            if plant_agent.size == "Small":
                return True
            else:
                return False
    def FightOrFlight(self, prey_agent):
        '''The less hunger, more desperate for a meal, at 50% hunger the modifier becomes 1, above 50% hunger it probably wont risk, below it will'''
        desperation = 0.5 / (self.hunger / GSM.Maximum_hunger)
        preySize = prey_agent.size
        preyType = prey_agent.type

        if (self.size == "Small" and preySize == "Medium") or (self.size == "Medium" and preySize == "Large") and preyType != "Plant": #1 size difference
            if round(random.random(), 2) <= GSM.Predator_bigger_prey_fight_chance * desperation:
                return True #predator will fight
            else:
                return False    #predator doesn't fight
        elif (self.size == "Small" and preySize == "Large") and preyType != "Plant": #2 size difference
            if round(random.random(), 2) <= (GSM.Predator_bigger_prey_fight_chance/5) * desperation:    # predator is VERY unlikely to fight
                return True
            else:
                return False  # predator doesn't fight
        else:
            return True #large can eat anything
    def Fight(self, prey_agent):
        '''at 50% hunger prey has 50% GSM.Well_fed_buff worth'''
        if prey_agent.type == "Plant":
            return True     #plants don't fight back

        prey_power = round(GSM.Well_fed_buff * (prey_agent.hunger / GSM.Maximum_hunger), 2)     #Well fed prey gets a boost to their combat power
        if (self.size == "Small" and prey_agent.size == "Medium") or (self.size == "Medium" and prey_agent.size == "Large"): #1 size difference
            total_win_chance = round(GSM.Predator_bigger_prey_win_chance - prey_power * GSM.Predator_bigger_prey_win_chance, 2)
            if round(random.random(), 2) <= (total_win_chance):

                ConsoleLog.FightBig(self, prey_agent, total_win_chance, prey_power, GSM.Console_log_fight_big)
                return True #predator won the fight
            else:
                ConsoleLog.DiedInBattle(self, prey_agent.name, GSM.Console_log_death_battle)
                return False    #predator lost the fight and died

        elif (self.size == "Small" and prey_agent.size == "Large"):       #probably suicide for small guy but let him try
            total_win_chance = round((GSM.Predator_bigger_prey_win_chance/5 - prey_power * (GSM.Predator_bigger_prey_win_chance/5)), 2)
            if round(random.random(), 2) <= (total_win_chance):
                    ConsoleLog.FightBig(self, prey_agent, total_win_chance, prey_power, GSM.Console_log_fight_big)

                    return True #David beat the goliath
            else:
                ConsoleLog.DiedInBattle(self, prey_agent.name, GSM.Console_log_death_battle)
                return False    #predator lost the fight and died
        else:
            return True #large predator automatically wins



    def Hunger(self, ate=False, preySize="Small", direction=[69, 69]):
        #Function to track Agents hunger level
        #If food was eaten, how much nourishment does it give
        if ate == True:
            if preySize == "Small":
                worth = 5
                ConsoleLog.AgentWasEaten(self, direction[0], direction[1], GSM.World_agent_list_x_y, worth, GSM.Console_log_was_eaten)
                ConsoleLog.FoundFood(self, direction[0], direction[1], GSM.World_agent_list_x_y, worth, GSM.Console_log_found_food)
                self.hunger = self.hunger + worth

            elif preySize == "Medium":
                worth = 9
                ConsoleLog.AgentWasEaten(self, direction[0], direction[1], GSM.World_agent_list_x_y, worth, GSM.Console_log_was_eaten)
                ConsoleLog.FoundFood(self, direction[0], direction[1], GSM.World_agent_list_x_y, worth, GSM.Console_log_found_food)
                self.hunger = self.hunger + worth
            else:
                worth = 26
                ConsoleLog.AgentWasEaten(self, direction[0], direction[1], GSM.World_agent_list_x_y, worth, GSM.Console_log_was_eaten)
                ConsoleLog.FoundFood(self, direction[0], direction[1], GSM.World_agent_list_x_y, worth, GSM.Console_log_found_food)
                self.hunger = self.hunger + worth #big animals nourish for longer
            if self.hunger > GSM.Maximum_hunger:
                self.hunger = GSM.Maximum_hunger
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
        hunger_factor = hunger / GSM.Max_hunger_to_reproduce  # Normalizes hunger between 0 and 1
        return round(1 / (1 + math.exp(-sigmoid_slope * (hunger_factor - 0.5))), 2) #more well fed, more chance to breed

    def Starvation_Age_Battle_Death(self, DiedInBattle=False):
        '''Handles all kinds of deaths'''
        self.age = self.age + 1

        if DiedInBattle == True:
            self.RemoveAgent(self) #Cow killed you bro
            return

        if self.hunger <= 0:
            ConsoleLog.DeathStarvation(self, GSM.Console_log_death_starvation)
            self.RemoveAgent(self) #starve
            return
        else:
            sigmoid_slope = 20.0
            death_factor = self.age / GSM.DeathAge  # Normalizes chance to die between 0 and 1

            if round(1 / (1 + math.exp(-sigmoid_slope * (death_factor - 0.5))), 2) >= round(random.random(), 2):  # older you are, more likely to perish
                ConsoleLog.DeathOldAge(self, GSM.Console_log_death_oldage)
                self.RemoveAgent(self)  # die of old age
            return

    def Reproduce(self): #Is called directly, Handles reproducing and aging

        if self.age > GSM.Reproduce_age:
            if self.breedcooldown > 0:      #Introduces a breeding cooldown
                self.breedcooldown = self.breedcooldown - 1
                return
            else:
                self.breedcooldown = GSM.Animal_breed_cooldown

            if self.hunger <= 0:    #prevents bizzare cases of 0 or negative hunger reproducing
                return

            sigm = Agent.HungerReproduceSigmoid(self.hunger)
            rnd = round(random.random(), 2)
            mult = round(GSM.Base_reproduce_chance * sigm, 2)

            ConsoleLog.ReproduceChance(self, GSM.Base_reproduce_chance, sigm, mult, rnd, GSM.Console_log_reproduce_chance)
            if rnd <= mult:

                UpdatedAnimalSum = len(GSM.Tigers_list) + len(GSM.Dandelion_list) + len(GSM.Cows_list) + len(GSM.Wolf_list) + len(GSM.Rabbits_list) + len(GSM.Appletree_list) + len(GSM.Fox_list) #need to update this when adding more animals

                if pow(GSM.World_size, 2) < (round(UpdatedAnimalSum * GSM.World_size_spawn_tolerance, 1)):

                    ConsoleLog.WorldTooSmallTooBreed(GSM.Console_log_worldtoosmalltobreed)
                    return

                elif "Tiger" in self.name:
                    if len(GSM.Tigers_list) > GSM.Personal_animal_limit:
                        ConsoleLog.PersonalPopulationLimit("Tiger", GSM.Console_log_personalpopulationlimit)
                        return
                    babyname = int(re.search(r"(\d+)$", self.name).group(1)) #use regular expression to extract the generation of parent
                    babyname = "Tiger_" + str(babyname+1) #make name with new generation number
                    newborn = SpawnTiger(name=babyname, perception=self.perception, speed=self.speed, hunger=self.hunger)
                elif "Cow" in self.name:
                    if len(GSM.Cows_list) > GSM.Personal_animal_limit:
                        ConsoleLog.PersonalPopulationLimit("Cow", GSM.Console_log_personalpopulationlimit)
                        return
                    babyname = int(re.search(r"(\d+)$", self.name).group(1))
                    babyname = "Cow_" + str(babyname+1)
                    newborn = SpawnCow(name=babyname, perception=self.perception, speed=self.speed, hunger=self.hunger)
                elif "Rabbit" in self.name:
                    if len(GSM.Rabbits_list) > GSM.Personal_animal_limit:
                        ConsoleLog.PersonalPopulationLimit("Rabbit", GSM.Console_log_personalpopulationlimit)
                        return
                    babyname = int(re.search(r"(\d+)$", self.name).group(1))
                    babyname = "Rabbit_" + str(babyname+1)
                    newborn = SpawnRabbit(name=babyname, perception=self.perception, speed=self.speed, hunger=self.hunger)
                elif "Wolf" in self.name:
                    if len(GSM.Wolf_list) > GSM.Personal_animal_limit:
                        ConsoleLog.PersonalPopulationLimit("Wolf", GSM.Console_log_personalpopulationlimit)
                        return
                    babyname = int(re.search(r"(\d+)$", self.name).group(1)) #use regular expression to extract the generation of parent
                    babyname = "Wolf_" + str(babyname+1) #make name with new generation number
                    newborn = SpawnWolf(name=babyname, perception=self.perception, speed=self.speed, hunger=self.hunger)
                elif "Fox" in self.name:
                    if len(GSM.Fox_list) > GSM.Personal_animal_limit:
                        ConsoleLog.PersonalPopulationLimit("Fox", GSM.Console_log_personalpopulationlimit)
                        return
                    babyname = int(re.search(r"(\d+)$", self.name).group(1)) #use regular expression to extract the generation of parent
                    babyname = "Fox_" + str(babyname+1) #make name with new generation number
                    newborn = SpawnFox(name=babyname, perception=self.perception, speed=self.speed, hunger=self.hunger)
                ConsoleLog.Born(newborn, GSM.Console_log_born)


            #todo: gene evo mutate func


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
    GSM.Dandelion_list.append(Dandelion)
    return Dandelion
def SpawnAppletree(name="Appletree_1", type="Plant", perception=0, speed=0, size="Large", hunger=20): # input default name, type, perception, speed, size, and starting hunger, unless overwritten by parent
    Appletree = Agent(name, type, perception, speed, size, hunger)
    GSM.Appletree_list.append(Appletree)
    return Appletree
def SpawnCow(name="Cow_1", type="Herbivore", perception=1, speed=1, size="Large", hunger=25):
    Cow = Agent(name, type, perception, speed, size, hunger)
    GSM.Cows_list.append(Cow)
    return Cow
def SpawnRabbit(name="Rabbit_1", type="Herbivore", perception=1, speed=1, size="Small", hunger=25):
    Rabbit = Agent(name, type, perception, speed, size, hunger)
    GSM.Rabbits_list.append(Rabbit)
    return Rabbit
def SpawnTiger(name="Tiger_1", type="Carnivore", perception=1, speed=1, size="Large", hunger=25):
    Tiger = Agent(name, type, perception, speed, size, hunger)
    GSM.Tigers_list.append(Tiger)
    return Tiger
def SpawnWolf(name="Wolf_1", type="Carnivore", perception=1, speed=1, size="Medium", hunger=25):
    Wolf = Agent(name, type, perception, speed, size, hunger)
    GSM.Wolf_list.append(Wolf)
    return Wolf
def SpawnFox(name="Fox_1", type="Carnivore", perception=1, speed=1, size="Small", hunger=25):
    Fox = Agent(name, type, perception, speed, size, hunger)
    GSM.Fox_list.append(Fox)
    return Fox
def RespawnVegetation():
    # respawn plants every turn
    UpdatedAnimalSum = len(GSM.Tigers_list) + len(GSM.Dandelion_list) + len(GSM.Cows_list) + len(GSM.Wolf_list) + len(GSM.Rabbits_list) + len(GSM.Appletree_list) + len(GSM.Fox_list)# need to update this when adding more animals
    max_tiles = pow(GSM.World_size, 2)
    current_flower_amount = GSM.Num_dandelion[-1] + GSM.Num_appletree[-1]# + Num_berrybush[-1]
    total_growth_per_turn = GSM.Dandelion_growth_per_turn + GSM.Appletree_growth_per_turn + GSM.Berrybush_growth_per_turn

    if max_tiles <= (round((UpdatedAnimalSum + total_growth_per_turn) * GSM.World_size_spawn_tolerance)):
        ConsoleLog.WorldTooSmallTooGrow(GSM.Console_log_worldtoosmalltogrow)
        return
    if current_flower_amount + total_growth_per_turn <= GSM.Max_flowers:
        for j in range(GSM.Dandelion_growth_per_turn):
            SpawnDandelion()
        for j in range(GSM.Appletree_growth_per_turn):
            SpawnAppletree()
    elif (current_flower_amount + total_growth_per_turn/2) <= GSM.Max_flowers: #spawns half
        for j in range(GSM.Dandelion_growth_per_turn//2):
            SpawnDandelion()
        for j in range(GSM.Appletree_growth_per_turn//2):
            SpawnAppletree()
    else:
        return


#spawn amount of agents we want
for i in range(GSM.Num_dandelion[0]):
    SpawnDandelion()
for i in range(GSM.Num_appletree[0]):
    SpawnAppletree()
for i in range(GSM.Num_cow[0]):
    SpawnCow()
for i in range(GSM.Num_rabbit[0]):
    SpawnRabbit()
for i in range(GSM.Num_tiger[0]):
    SpawnTiger()
for i in range(GSM.Num_wolf[0]):
    SpawnWolf()
for i in range(GSM.Num_fox[0]):
    SpawnFox()

print(f"World started with {GSM.Num_dandelion[0]} Dandelions, {GSM.Num_appletree[0]} Apple trees, {GSM.Num_cow[0]} Cows, {GSM.Num_rabbit[0]} Rabbits, {GSM.Num_fox[0]} Foxes, {GSM.Num_wolf[0]} Wolves and {GSM.Num_tiger[0]} Tigers")
ConsoleLog.StartPosition(GSM.Cows_list, GSM.Dandelion_list, GSM.Appletree_list, GSM.Tigers_list, GSM.Wolf_list, GSM.Rabbits_list, GSM.Fox_list, GSM.Console_log_start_position)



#simulate GSM.Simulation_Length turns (main loop)
for i in range(GSM.Simulation_Length):

    RespawnVegetation()

    print(f"\n\n----------Turn {i+1}----------")
    print(f"There are: {len(GSM.Dandelion_list)} Dandelions, {len(GSM.Appletree_list)} Apple trees, {len(GSM.Cows_list)} Cows, {len(GSM.Rabbits_list)} Rabbits, {len(GSM.Fox_list)} Foxes, {len(GSM.Wolf_list)} Wolves, and {len(GSM.Tigers_list)} Tigers, Total: {GSM.SumAllAgents[-1]}\n\n")
    for cows in GSM.Cows_list[:]:   #This creates shallow copies of the lists, allowing processing of all animals even if some get deleted.
                                #This is because if animal is killed, list index will shift without updating current loop index, and make next
                                #animal be skipped from processing, causing bunch of bugs
        cows.SearchForFood()
        cows.Reproduce()
        cows.Starvation_Age_Battle_Death()

    print("")
    for rabbits in GSM.Rabbits_list[:]:
        rabbits.SearchForFood()
        rabbits.Reproduce()
        rabbits.Starvation_Age_Battle_Death()
    print("")
    for foxes in GSM.Fox_list[:]:
        DiedInBattle = False
        foxes.SearchForFood()
        if DiedInBattle == False:
            foxes.Reproduce()
            foxes.Starvation_Age_Battle_Death()
        else:
            foxes.Starvation_Age_Battle_Death(DiedInBattle=True)
    print("")
    for tigers in GSM.Tigers_list[:]:
        DiedInBattle = False
        tigers.SearchForFood()
        if DiedInBattle == False:
            tigers.Reproduce()
            tigers.Starvation_Age_Battle_Death()
        else:
            tigers.Starvation_Age_Battle_Death(DiedInBattle=True)
    print("")
    for wolves in GSM.Wolf_list[:]:
        wolves.SearchForFood()
        if DiedInBattle == False:
            wolves.Reproduce()
            wolves.Starvation_Age_Battle_Death()
        else:
            wolves.Starvation_Age_Battle_Death(DiedInBattle=True)

    GSM.Num_cow.append(len(GSM.Cows_list))
    GSM.Num_dandelion.append(len(GSM.Dandelion_list))
    GSM.Num_appletree.append(len(GSM.Appletree_list))
    GSM.Num_tiger.append(len(GSM.Tigers_list))
    GSM.Num_wolf.append(len(GSM.Wolf_list))
    GSM.Num_fox.append(len(GSM.Fox_list))
    GSM.Num_rabbit.append(len(GSM.Rabbits_list))
    GSM.SumAllAgents.append(GSM.Num_dandelion[-1] + GSM.Num_cow[-1] + GSM.Num_tiger[-1] + GSM.Num_wolf[-1] + GSM.Num_rabbit[-1] + GSM.Num_appletree[-1] + GSM.Num_fox[-1])

    GSM.Cows_hunger.append(CalculateAverageHunger(GSM.Cows_list))
    GSM.Tigers_hunger.append(CalculateAverageHunger(GSM.Tigers_list))
    GSM.Rabbits_hunger.append(CalculateAverageHunger(GSM.Rabbits_list))
    GSM.Wolf_hunger.append(CalculateAverageHunger(GSM.Wolf_list))
    GSM.Fox_hunger.append(CalculateAverageHunger(GSM.Fox_list))

    if GSM.Visualise_simulation_toggle:
        GSM.Sim_delay = VisualiseScript.EventHandler(GSM)
        VisualiseScript.VisualiseSimulationDraw(GSM, i) #draw the display window
        time.sleep(GSM.Sim_delay)


#report results
print("\n\n----------SIMULATION END----------")
print(f"World started with {GSM.Num_dandelion[0]} Dandelions, {GSM.Num_appletree[0]} Apple trees, {GSM.Num_cow[0]} Cows, {GSM.Num_fox[0]} Foxes, {GSM.Num_rabbit[0]} Rabbits, {GSM.Num_wolf[0]} Wolves, and {GSM.Num_tiger[0]} Tigers, Total: {(GSM.SumAllAgents[0])}")
print(f"World ended at turn {GSM.Simulation_Length} with {GSM.Num_dandelion[-1]} Dandelions, {GSM.Num_appletree[-1]} Apple trees, {GSM.Num_cow[-1]} Cows, {GSM.Num_rabbit[-1]} Rabbits, {GSM.Num_fox[0]} Foxes, {GSM.Num_wolf[-1]} Wolves, and {GSM.Num_tiger[-1]} Tigers, Total: {GSM.SumAllAgents[-1]}/{round(pow(GSM.World_size, 2) / GSM.World_size_spawn_tolerance)}")

VisualiseScript.VisualisePopulation(GSM)
VisualiseScript.VisualiseHunger(GSM)

VisualiseScript.VisualiseSimulationQuit()