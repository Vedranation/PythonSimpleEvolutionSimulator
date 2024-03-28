#function to easily toggle logging to console
#Was coded before GSM was created so it doesnt use it. Instead relies on passing values in manually
#Not exactly clever but I'm too lazy to refactor it for no reason

def StartPosition(Cows_list, Dandelion_list, Appletree_list, Tigers_list, Wolf_list, Rabbits_list, Fox_list, Berrybush_list, Goats_list, logbool):
    '''Logs agents starting positions, input Cows_list, Dandelion_list, Tigers_list, Wolf_list, Rabbits_list'''
    if logbool == True:
        for i in Dandelion_list:
            print(f"Dandelions are at: [{i.x}, {i.y}]")
        for i in Berrybush_list:
            print(f"Berry bushes are at: [{i.x}, {i.y}]")
        for i in Appletree_list:
            print(f"Apple trees are at: [{i.x}, {i.y}]")
        for i in Rabbits_list:
            print(f"Rabbits are at: [{i.x}, {i.y}]")
        for i in Goats_list:
            print(f"Goats are at: [{i.x}, {i.y}]")
        for i in Cows_list:
            print(f"Cows are at: [{i.x}, {i.y}]")
        for i in Fox_list:
            print(f"Foxes are at: [{i.x}, {i.y}]")
        for i in Wolf_list:
            print(f"Wolves are at: [{i.x}, {i.y}]")
        for i in Tigers_list:
            print(f"Tigers are at: [{i.x}, {i.y}]")
    return

def CheckForFood(agent, directionX, directionY, isNone, World_agent_list_x_y, logbool):
    '''Logs when agents check squares, input agent instance, directionX, directionY, if checked square isNone, World_agent_list_x_y'''

    if logbool == True:
        if isNone == True:
            print(f"{agent.name} [{agent.x},{agent.y}]  |  check: [{directionX},{directionY}]  |  found: None")
        else:
            print(f"{agent.name} [{agent.x},{agent.y}]  |  check: [{directionX},{directionY}]  |  found: {World_agent_list_x_y[directionX][directionY].name}")
    return

def Mutated(agent, gene_name, ex_value, new_value, logbool):
    if logbool:
        if new_value > ex_value:    #Spent a point to upgrade
            print(f"{agent.name} mutated {gene_name}: ({ex_value} -> {new_value})  |  Gene points: {agent.free_mutation_points+1} -> {agent.free_mutation_points}")
        else:   #Gained a point to downgrade
            print(f"{agent.name} mutated {gene_name}: ({ex_value} -> {new_value})  |  Gene points: {agent.free_mutation_points-1} -> {agent.free_mutation_points}")


def FoundFood(agent, directionX, directionY, World_agent_list_x_y, worth, logbool):
    '''Logs when agents find food, input agent instance, directionX, directionY, World_agent_list_x_y'''
    if logbool == True:
        print(f"{agent.name} found food! Food is: {World_agent_list_x_y[directionX][directionY].name}, Hunger: {agent.hunger} -> {agent.hunger + worth}")  # Find specific instance to eat
    return

def DeathStarvation(agent, logbool):
    if logbool == True:
        print(f"{agent.name} died of starvation at [{agent.x}, {agent.y}]")
    return

def Born(newborn_agent, logbool):
    if logbool == True:
        print(f"{newborn_agent.name} was born with:  perception {newborn_agent.perception}, speed {newborn_agent.speed},  hunger {newborn_agent.hunger}, at [{newborn_agent.x}, {newborn_agent.y}]")
        if newborn_agent.hunger <= 0:
            print("WARNING - ZERO OR NEGATIVE HUNGER BREEDING DETECTED");
    return

def AgentWasEaten(agent, directionX, directionY, World_agent_list_x_y, worth, logbool):
    if logbool == True:
        print(f"{agent.name} just ate a {World_agent_list_x_y[directionX][directionY].name}, at [{agent.x}, {agent.y}], Hunger: {agent.hunger} -> {agent.hunger + worth}")
    return

def RandomMove(agent, directionX, directionY, logbool):
    if logbool == True:
        print(f"{agent.name} roamed [{agent.x},{agent.y}] -> [{directionX},{directionY}], Hunger: {agent.hunger}")
    return

def DeathOldAge(agent, logbool):
    if logbool == True:
        print(f"{agent.name} died of old age at [{agent.x}, {agent.y}]")
    return

def ReproduceChance(agent, Base_reproduce_chance, sigm, mult, rnd, logbool):
    if logbool == True:
        print(
            f"Base: {Base_reproduce_chance},  |   Sigm: {sigm},  |   Mult: {mult},  |   Rnd: {rnd},  |   Rnd small? {rnd <= round(Base_reproduce_chance * sigm, 2)}")
    return

def DiedInBattle(agent, prey, logbool):
    if logbool == True:
        print(f"{agent.name} ({agent.hunger}) died in battle fighting {prey}")
    return

def PersonalPopulationLimit(animal, logbool):
    if logbool:
        print(f"{animal} has reached population limit")
    return

def WorldTooSmallTooGrow(logbool):
    if logbool:
        print("World too small to grow!")
    return

def FightBig(agent, prey_agent, win_chance, prey_power, logbool):
    if logbool == True:
        win_chance = round(win_chance, 2)
        if prey_agent.size == "Large" and agent.size == "Small":

            print(f"DAMM! {agent.name} ({agent.size}) just killed HUGE game! {prey_agent.name} ({prey_agent.size}) Prey Power: {prey_power*100}%, Total win chance was: {win_chance*100}%")
        else:
            print(f"{agent.name} ({agent.size}) just killed a bigger prey! {prey_agent.name} ({prey_agent.size}) Prey Power: {prey_power*100}%, Total win chance was: {win_chance*100}%")
    return

def WorldTooSmallTooBreed(logbool):
    if logbool:
        print(f"World too small to breed!")

def AverageSpeed(cows_speed, tigers_speed, rabbits_speed, goats_speed, wolf_speed, fox_speed, logbool):
    if logbool:
        print(f"Average speed for:        cows: {cows_speed} | tigers: {tigers_speed} | rabbits: {rabbits_speed} | goats: {goats_speed} | wolves: {wolf_speed} | foxes: {fox_speed}")
def AveragePerception(cows_perception, tigers_perception, rabbits_perception, goats_perception, wolf_perception, fox_perception, logbool):
    if logbool:
        print(f"Average perception for:   cows: {cows_perception} | tigers: {tigers_perception} | rabbits: {rabbits_perception} | goats: {goats_perception} | wolves: {wolf_perception} | foxes: {fox_perception}")