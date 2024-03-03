import random
import math
import re
import ConsoleLog

class Agent:
    def __init__(self, GSM, name, type, perception, speed, size, hunger):

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

        self.GSM = GSM  #store internal pointer to GlobalsStateManager
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

        self.x = random.randint(0, self.GSM.World_size-1)
        self.y = random.randint(0, self.GSM.World_size-1)

        #Loop until a free spot is found
        while self.GSM.World_agent_list_x_y[self.x][self.y] != None:
            self.x = random.randint(0, self.GSM.World_size-1)
            self.y = random.randint(0, self.GSM.World_size-1)
        self.GSM.World_agent_list_x_y[self.x][self.y] = self

    @staticmethod #fixme: pass GSM into this
    def RemoveAgent(GSM, agent): #Removes an agent from both the type list and agent list.

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
                if direction[0] >= self.GSM.World_size or direction[1] >= self.GSM.World_size or direction[0] < 0 or direction[1] < 0: #prevents checking beyond edge of world
                    continue

                if self.GSM.World_agent_list_x_y[direction[0]][direction[1]] == None:
                    ConsoleLog.CheckForFood(self, direction[0], direction[1], True, self.GSM.World_agent_list_x_y, self.GSM.Console_log_check_for_food)
                    continue
                else:
                    ConsoleLog.CheckForFood(self, direction[0], direction[1], False, self.GSM.World_agent_list_x_y, self.GSM.Console_log_check_for_food)

                #if we found food, eat it and go there:
                if self.GSM.World_agent_list_x_y[direction[0]][direction[1]].type == self.food:
                    if self.food == "Plant": #herbivore eat
                        if self.HerbivoreNoEatBig(self.GSM.World_agent_list_x_y[direction[0]][direction[1]]) == True:
                            self.Hunger(True, self.GSM.World_agent_list_x_y[direction[0]][direction[1]].size,
                                        direction)  # track hunger levels, pass food that was eaten
                            Agent.RemoveAgent(self.GSM, self.GSM.World_agent_list_x_y[direction[0]][direction[1]])  # delete the agent being eaten

                            # update new position
                            self.GSM.World_agent_list_x_y[self.x][self.y] = None
                            self.GSM.World_agent_list_x_y[direction[0]][direction[1]] = self
                            self.x = direction[0]
                            self.y = direction[1]
                            return  # end the search
                        else:
                            continue #small herbivores don't eat bigger size food

                    if self.FightOrFlight(self.GSM.World_agent_list_x_y[direction[0]][direction[1]]) == True:   #carnivore eat: check prey size, if prey is bigger chance to fight it is smaller

                        if self.Fight(self.GSM.World_agent_list_x_y[direction[0]][direction[1]]) == True:    #predator won and ate the meal

                            self.Hunger(True, self.GSM.World_agent_list_x_y[direction[0]][direction[1]].size, direction)  # track hunger levels, pass food that was eaten
                            Agent.RemoveAgent(self.GSM, self.GSM.World_agent_list_x_y[direction[0]][direction[1]])  # delete the agent being eaten

                            #update new position
                            self.GSM.World_agent_list_x_y[self.x][self.y] = None
                            self.GSM.World_agent_list_x_y[direction[0]][direction[1]] = self
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
                if direction[0] >= self.GSM.World_size or direction[1] >= self.GSM.World_size or direction[0] < 0 or direction[1] < 0 or self.GSM.World_agent_list_x_y[direction[0]][direction[1]] != None:
                    continue # prevents moving beyond edge of world or into another Agent and fucking things up
                random.choice(directions_x_y)
                ConsoleLog.RandomMove(self, direction[0], direction[1], self.GSM.Console_log_random_move)

                self.GSM.World_agent_list_x_y[self.x][self.y] = None
                self.GSM.World_agent_list_x_y[direction[0]][direction[1]] = self
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
        desperation = 0.5 / (self.hunger / self.GSM.Maximum_hunger)
        preySize = prey_agent.size
        preyType = prey_agent.type

        if (self.size == "Small" and preySize == "Medium") or (self.size == "Medium" and preySize == "Large") and preyType != "Plant": #1 size difference
            if round(random.random(), 2) <= self.GSM.Predator_bigger_prey_fight_chance * desperation:
                return True #predator will fight
            else:
                return False    #predator doesn't fight
        elif (self.size == "Small" and preySize == "Large") and preyType != "Plant": #2 size difference
            if round(random.random(), 2) <= (self.GSM.Predator_bigger_prey_fight_chance/5) * desperation:    # predator is VERY unlikely to fight
                return True
            else:
                return False  # predator doesn't fight
        else:
            return True #large can eat anything
    def Fight(self, prey_agent):
        '''at 50% hunger prey has 50% GSM.Well_fed_buff worth'''
        if prey_agent.type == "Plant":
            return True     #plants don't fight back

        prey_power = round(self.GSM.Well_fed_buff * (prey_agent.hunger / self.GSM.Maximum_hunger), 2)     #Well fed prey gets a boost to their combat power
        if (self.size == "Small" and prey_agent.size == "Medium") or (self.size == "Medium" and prey_agent.size == "Large"): #1 size difference
            total_win_chance = round(self.GSM.Predator_bigger_prey_win_chance - prey_power * self.GSM.Predator_bigger_prey_win_chance, 2)
            if round(random.random(), 2) <= (total_win_chance):

                ConsoleLog.FightBig(self, prey_agent, total_win_chance, prey_power, self.GSM.Console_log_fight_big)
                return True #predator won the fight
            else:
                ConsoleLog.DiedInBattle(self, prey_agent.name, self.GSM.Console_log_death_battle)
                return False    #predator lost the fight and died

        elif (self.size == "Small" and prey_agent.size == "Large"):       #probably suicide for small guy but let him try
            total_win_chance = round((self.GSM.Predator_bigger_prey_win_chance/5 - prey_power * (self.GSM.Predator_bigger_prey_win_chance/5)), 2)
            if round(random.random(), 2) <= (total_win_chance):
                    ConsoleLog.FightBig(self, prey_agent, total_win_chance, prey_power, self.GSM.Console_log_fight_big)

                    return True #David beat the goliath
            else:
                ConsoleLog.DiedInBattle(self, prey_agent.name, self.GSM.Console_log_death_battle)
                return False    #predator lost the fight and died
        else:
            return True #large predator automatically wins



    def Hunger(self, ate=False, preySize="Small", direction=[69, 69]):

        #Function to track Agents hunger level
        #If food was eaten, how much nourishment does it give
        if ate == True:
            if preySize == "Small":
                worth = 5
                ConsoleLog.AgentWasEaten(self, direction[0], direction[1], self.GSM.World_agent_list_x_y, worth, self.GSM.Console_log_was_eaten)
                ConsoleLog.FoundFood(self, direction[0], direction[1], self.GSM.World_agent_list_x_y, worth, self.GSM.Console_log_found_food)
                self.hunger = self.hunger + worth

            elif preySize == "Medium":
                worth = 9
                ConsoleLog.AgentWasEaten(self, direction[0], direction[1], self.GSM.World_agent_list_x_y, worth, self.GSM.Console_log_was_eaten)
                ConsoleLog.FoundFood(self, direction[0], direction[1], self.GSM.World_agent_list_x_y, worth, self.GSM.Console_log_found_food)
                self.hunger = self.hunger + worth
            else:
                worth = 26
                ConsoleLog.AgentWasEaten(self, direction[0], direction[1], self.GSM.World_agent_list_x_y, worth, self.GSM.Console_log_was_eaten)
                ConsoleLog.FoundFood(self, direction[0], direction[1], self.GSM.World_agent_list_x_y, worth, self.GSM.Console_log_found_food)
                self.hunger = self.hunger + worth #big animals nourish for longer
            if self.hunger > self.GSM.Maximum_hunger:
                self.hunger = self.GSM.Maximum_hunger
            return #grace period, if food was found, don't use reserves or check for starvation

        #depending on Agent size, food depletes at different rate
        if self.size == "Small":
            self.hunger = self.hunger - 1 #lose 1 point worth of hunger
        elif self.size == "Medium":
            self.hunger = self.hunger - 2
        else:
            self.hunger = self.hunger - 4 #bigger animals need more food


    @staticmethod
    def HungerReproduceSigmoid(GSM, hunger): #fixme: pass GSM into this
        sigmoid_slope = 7.0
        hunger_factor = hunger / GSM.Max_hunger_to_reproduce  # Normalizes hunger between 0 and 1
        return round(1 / (1 + math.exp(-sigmoid_slope * (hunger_factor - 0.5))), 2) #more well fed, more chance to breed

    def Starvation_Age_Battle_Death(self, DiedInBattle=False):
        '''Handles all kinds of deaths'''
        self.age = self.age + 1
        if DiedInBattle == True:
            self.RemoveAgent(self.GSM, self) #Cow killed you bro
            return

        if self.hunger <= 0:
            ConsoleLog.DeathStarvation(self, self.GSM.Console_log_death_starvation)
            self.RemoveAgent(self.GSM, self) #starve
            return
        else:
            sigmoid_slope = 20.0
            death_factor = self.age / self.GSM.DeathAge  # Normalizes chance to die between 0 and 1

            if round(1 / (1 + math.exp(-sigmoid_slope * (death_factor - 0.5))), 2) >= round(random.random(), 2):  # older you are, more likely to perish
                ConsoleLog.DeathOldAge(self, self.GSM.Console_log_death_oldage)
                self.RemoveAgent(self.GSM, self)  # die of old age
            return

    def Reproduce(self): #Is called directly, Handles reproducing and aging

        if self.age > self.GSM.Reproduce_age:
            if self.breedcooldown > 0:      #Introduces a breeding cooldown
                self.breedcooldown = self.breedcooldown - 1
                return
            else:
                self.breedcooldown = self.GSM.Animal_breed_cooldown

            if self.hunger <= 0:    #prevents bizzare cases of 0 or negative hunger reproducing
                return

            sigm = Agent.HungerReproduceSigmoid(self.GSM, self.hunger)
            rnd = round(random.random(), 2)
            mult = round(self.GSM.Base_reproduce_chance * sigm, 2)

            ConsoleLog.ReproduceChance(self, self.GSM.Base_reproduce_chance, sigm, mult, rnd, self.GSM.Console_log_reproduce_chance)
            if rnd <= mult:

                UpdatedAnimalSum = len(self.GSM.Tigers_list) + len(self.GSM.Dandelion_list) + len(self.GSM.Cows_list) + len(self.GSM.Wolf_list) + len(self.GSM.Rabbits_list) + len(self.GSM.Appletree_list) + len(self.GSM.Fox_list) #need to update this when adding more animals

                if pow(self.GSM.World_size, 2) < (round(UpdatedAnimalSum * self.GSM.World_size_spawn_tolerance, 1)):

                    ConsoleLog.WorldTooSmallTooBreed(self.GSM.Console_log_worldtoosmalltobreed)
                    return

                elif "Tiger" in self.name:
                    if len(self.GSM.Tigers_list) > self.GSM.Personal_animal_limit:
                        ConsoleLog.PersonalPopulationLimit("Tiger", self.GSM.Console_log_personalpopulationlimit)
                        return
                    babyname = int(re.search(r"(\d+)$", self.name).group(1)) #use regular expression to extract the generation of parent
                    babyname = "Tiger_" + str(babyname+1) #make name with new generation number
                    newborn = SpawnTiger(self.GSM, name=babyname, perception=self.perception, speed=self.speed, hunger=self.hunger)
                elif "Cow" in self.name:
                    if len(self.GSM.Cows_list) > self.GSM.Personal_animal_limit:
                        ConsoleLog.PersonalPopulationLimit("Cow", self.GSM.Console_log_personalpopulationlimit)
                        return
                    babyname = int(re.search(r"(\d+)$", self.name).group(1))
                    babyname = "Cow_" + str(babyname+1)
                    newborn = SpawnCow(self.GSM, name=babyname, perception=self.perception, speed=self.speed, hunger=self.hunger)
                elif "Rabbit" in self.name:
                    if len(self.GSM.Rabbits_list) > self.GSM.Personal_animal_limit:
                        ConsoleLog.PersonalPopulationLimit("Rabbit", self.GSM.Console_log_personalpopulationlimit)
                        return
                    babyname = int(re.search(r"(\d+)$", self.name).group(1))
                    babyname = "Rabbit_" + str(babyname+1)
                    newborn = SpawnRabbit(self.GSM, name=babyname, perception=self.perception, speed=self.speed, hunger=self.hunger)
                elif "Wolf" in self.name:
                    if len(self.GSM.Wolf_list) > self.GSM.Personal_animal_limit:
                        ConsoleLog.PersonalPopulationLimit("Wolf", self.GSM.Console_log_personalpopulationlimit)
                        return
                    babyname = int(re.search(r"(\d+)$", self.name).group(1)) #use regular expression to extract the generation of parent
                    babyname = "Wolf_" + str(babyname+1) #make name with new generation number
                    newborn = SpawnWolf(self.GSM, name=babyname, perception=self.perception, speed=self.speed, hunger=self.hunger)
                elif "Fox" in self.name:
                    if len(self.GSM.Fox_list) > self.GSM.Personal_animal_limit:
                        ConsoleLog.PersonalPopulationLimit("Fox", self.GSM.Console_log_personalpopulationlimit)
                        return
                    babyname = int(re.search(r"(\d+)$", self.name).group(1)) #use regular expression to extract the generation of parent
                    babyname = "Fox_" + str(babyname+1) #make name with new generation number
                    newborn = SpawnFox(self.GSM, name=babyname, perception=self.perception, speed=self.speed, hunger=self.hunger)
                ConsoleLog.Born(newborn, self.GSM.Console_log_born)


            #todo: gene evo mutate func



#Function to spawn agents
def SpawnDandelion(GSM, name="Dandelion_1", type="Plant", perception=0, speed=0, size="Small", hunger=20): # input default name, type, perception, speed, size, and starting hunger, unless overwritten by parent
    Dandelion = Agent(GSM, name, type, perception, speed, size, hunger)
    GSM.Dandelion_list.append(Dandelion)
    return Dandelion
def SpawnAppletree(GSM, name="Appletree_1", type="Plant", perception=0, speed=0, size="Large", hunger=20): # input default name, type, perception, speed, size, and starting hunger, unless overwritten by parent
    Appletree = Agent(GSM, name, type, perception, speed, size, hunger)
    GSM.Appletree_list.append(Appletree)
    return Appletree
def SpawnCow(GSM, name="Cow_1", type="Herbivore", perception=1, speed=1, size="Large", hunger=25):
    Cow = Agent(GSM, name, type, perception, speed, size, hunger)
    GSM.Cows_list.append(Cow)
    return Cow
def SpawnRabbit(GSM, name="Rabbit_1", type="Herbivore", perception=1, speed=1, size="Small", hunger=25):
    Rabbit = Agent(GSM, name, type, perception, speed, size, hunger)
    GSM.Rabbits_list.append(Rabbit)
    return Rabbit
def SpawnTiger(GSM, name="Tiger_1", type="Carnivore", perception=1, speed=1, size="Large", hunger=25):
    Tiger = Agent(GSM, name, type, perception, speed, size, hunger)
    GSM.Tigers_list.append(Tiger)
    return Tiger
def SpawnWolf(GSM, name="Wolf_1", type="Carnivore", perception=1, speed=1, size="Medium", hunger=25):
    Wolf = Agent(GSM, name, type, perception, speed, size, hunger)
    GSM.Wolf_list.append(Wolf)
    return Wolf
def SpawnFox(GSM, name="Fox_1", type="Carnivore", perception=1, speed=1, size="Small", hunger=25):
    Fox = Agent(GSM, name, type, perception, speed, size, hunger)
    GSM.Fox_list.append(Fox)
    return Fox