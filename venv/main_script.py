
import time
import ConsoleLog
import VisualiseScript
import GlobalsStateManager
import AgentScript

GSM = GlobalsStateManager.GlobalsManager #Encapsulate all globals

#how many of each agents do you want to start with, stores their numbers each turn

#TODO: add Num_berrybush = [30];

#TODO: add Num_goat = [30];
#TODO: add stone or impassable terrain
#TODO: make animals babies spawn near parents
#TODO: make predators able to see fleeing prey

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
            AgentScript.SpawnDandelion(GSM)
        for j in range(GSM.Appletree_growth_per_turn):
            AgentScript.SpawnAppletree(GSM)
    elif (current_flower_amount + total_growth_per_turn/2) <= GSM.Max_flowers: #spawns half
        for j in range(GSM.Dandelion_growth_per_turn//2):
            AgentScript.SpawnDandelion(GSM)
        for j in range(GSM.Appletree_growth_per_turn//2):
            AgentScript.SpawnAppletree(GSM)
    else:
        return


#spawn amount of agents we want
for i in range(GSM.Num_dandelion[0]):
    AgentScript.SpawnDandelion(GSM)
for i in range(GSM.Num_appletree[0]):
    AgentScript.SpawnAppletree(GSM)
for i in range(GSM.Num_cow[0]):
    AgentScript.SpawnCow(GSM)
for i in range(GSM.Num_rabbit[0]):
    AgentScript.SpawnRabbit(GSM)
for i in range(GSM.Num_tiger[0]):
    AgentScript.SpawnTiger(GSM)
for i in range(GSM.Num_wolf[0]):
    AgentScript.SpawnWolf(GSM)
for i in range(GSM.Num_fox[0]):
    AgentScript.SpawnFox(GSM)

print(f"World started with {GSM.Num_dandelion[0]} Dandelions, {GSM.Num_appletree[0]} Apple trees, {GSM.Num_cow[0]} Cows, {GSM.Num_rabbit[0]} Rabbits, {GSM.Num_fox[0]} Foxes, {GSM.Num_wolf[0]} Wolves and {GSM.Num_tiger[0]} Tigers")
ConsoleLog.StartPosition(GSM.Cows_list, GSM.Dandelion_list, GSM.Appletree_list, GSM.Tigers_list, GSM.Wolf_list, GSM.Rabbits_list, GSM.Fox_list, GSM.Console_log_start_position)

def CalculateAverageHunger(animal_list):
    average = 0
    for i in animal_list:
        average = average + i.hunger
    if len(animal_list) == 0:
        return 0
    average = average / len(animal_list)
    return round(average, 1)

#simulate GSM.Simulation_Length turns (main loop)
for i in range(GSM.Simulation_Length):
    print(GSM.Predator_bigger_prey_win_chance)
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