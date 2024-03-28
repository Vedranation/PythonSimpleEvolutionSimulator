import time
import ConsoleLog
import VisualiseScript
import GlobalsStateManager
import AgentScript

GSM = GlobalsStateManager.GlobalsManager #Encapsulate all globals

#how many of each agents do you want to start with, stores their numbers each turn

#TODO: Make it possible to pass thru plants
#TODO: add stone or impassable terrain
#TODO: make animals babies spawn near parents
#TODO: make predators able to see fleeing prey

#---------------------------------------------------------------------------

if GSM.Visualise_simulation_toggle == True:
    VisualiseScript.VisualiseSimulationInit(GSM)
    GSM.Last_update_time = time.time()

DiedInBattle = False
#Check if world is big enough for all agents
GSM.SumAllAgents = [GSM.Num_cow[-1]+GSM.Num_dandelion[-1]+GSM.Num_tiger[-1]+
                    GSM.Num_wolf[-1]+GSM.Num_rabbit[-1]+GSM.Num_appletree[-1]+
                    GSM.Num_berrybush[-1]+GSM.Num_fox[-1]+GSM.Num_goat[-1]]
if pow(GSM.World_size, 2) < GSM.SumAllAgents[-1]:
    raise Exception("World can't be smaller than amount of objects to spawn")

#Generate the world X in Y, filled with None to show empty cells, starts from XY = 0, ends at at GSM.World_size - 1
GSM.World_agent_list_x_y = [[None for _ in range(GSM.World_size)] for _ in range(GSM.World_size)] #stores all agent instances


def RespawnVegetation():
    # respawn plants every turn
    UpdatedAnimalSum = len(GSM.Tigers_list) + len(GSM.Dandelion_list) + len(GSM.Cows_list) + len(GSM.Wolf_list)\
                       + len(GSM.Rabbits_list) + len(GSM.Appletree_list) + len(GSM.Fox_list) + \
                       len(GSM.Berrybush_list) + len(GSM.Goats_list)# need to update this when adding more animals
    max_tiles = pow(GSM.World_size, 2)
    current_flower_amount = GSM.Num_dandelion[-1] + GSM.Num_appletree[-1] + GSM.Num_berrybush[-1]
    total_growth_per_turn = GSM.Dandelion_growth_per_turn + GSM.Appletree_growth_per_turn + GSM.Berrybush_growth_per_turn

    if max_tiles <= (round((UpdatedAnimalSum + total_growth_per_turn) * GSM.World_size_spawn_tolerance)):
        ConsoleLog.WorldTooSmallTooGrow(GSM.Console_log_worldtoosmalltogrow)
        return
    if current_flower_amount + total_growth_per_turn <= GSM.Max_flowers:
        for j in range(GSM.Dandelion_growth_per_turn):
            AgentScript.SpawnDandelion(GSM)
        for j in range(GSM.Appletree_growth_per_turn):
            AgentScript.SpawnAppletree(GSM)
        for j in range(GSM.Berrybush_growth_per_turn):
            AgentScript.SpawnBerrybush(GSM)
    elif (current_flower_amount + total_growth_per_turn/2) <= GSM.Max_flowers: #spawns half
        for j in range(GSM.Dandelion_growth_per_turn//2):
            AgentScript.SpawnDandelion(GSM)
        for j in range(GSM.Appletree_growth_per_turn//2):
            AgentScript.SpawnAppletree(GSM)
        for j in range(GSM.Berrybush_growth_per_turn//2):
            AgentScript.SpawnBerrybush(GSM)
    else:
        return


#spawn amount of agents we want
for i in range(GSM.Num_dandelion[0]):
    AgentScript.SpawnDandelion(GSM)
for i in range(GSM.Num_berrybush[0]):
    AgentScript.SpawnBerrybush(GSM)
for i in range(GSM.Num_appletree[0]):
    AgentScript.SpawnAppletree(GSM)
for i in range(GSM.Num_cow[0]):
    AgentScript.SpawnCow(GSM)
for i in range(GSM.Num_rabbit[0]):
    AgentScript.SpawnRabbit(GSM)
for i in range(GSM.Num_goat[0]):
    AgentScript.SpawnGoat(GSM)
for i in range(GSM.Num_tiger[0]):
    AgentScript.SpawnTiger(GSM)
for i in range(GSM.Num_wolf[0]):
    AgentScript.SpawnWolf(GSM)
for i in range(GSM.Num_fox[0]):
    AgentScript.SpawnFox(GSM)

print(f"World started with {GSM.Num_dandelion[0]} Dandelions, {GSM.Num_berrybush[0]} berry bushes, {GSM.Num_appletree[0]} Apple trees, {GSM.Num_rabbit[0]} Rabbits, "
      f"{GSM.Num_goat[0]} Goats, {GSM.Num_cow} Cows, {GSM.Num_fox[0]} Foxes, {GSM.Num_wolf[0]} Wolves and {GSM.Num_tiger[0]} Tigers")
ConsoleLog.StartPosition(GSM.Cows_list, GSM.Dandelion_list, GSM.Appletree_list, GSM.Tigers_list, GSM.Wolf_list, GSM.Rabbits_list, GSM.Fox_list, GSM.Berrybush_list, GSM.Goats_list, GSM.Console_log_start_position)

def CalculateAverageStat(animal_list, stat):
    average = 0
    for agent in animal_list:
        average = average + getattr(agent, stat)    #This lets me pass in str and get agent.thing back
    if len(animal_list) == 0:
        return 0
    average = average / len(animal_list)
    return round(average, 1)

#simulate GSM.Simulation_Length turns (main loop)
for i in range(GSM.Simulation_Length):

    RespawnVegetation()

    print(f"\n\n----------Turn {i+1}----------")
    print(f"There are: {len(GSM.Dandelion_list)} Dandelions, {len(GSM.Berrybush_list)} Berry bushes, {len(GSM.Appletree_list)} Apple trees, "
          f"{len(GSM.Rabbits_list)} Rabbits, \n{len(GSM.Goats_list)} Goats, {len(GSM.Cows_list)} Cows, "
          f"{len(GSM.Fox_list)} Foxes, {len(GSM.Wolf_list)} Wolves, and {len(GSM.Tigers_list)} Tigers, Total: {GSM.SumAllAgents[-1]}\n\n")
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
    for goats in GSM.Goats_list[:]:
        goats.SearchForFood()
        goats.Reproduce()
        goats.Starvation_Age_Battle_Death()
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
    GSM.Num_berrybush.append(len(GSM.Berrybush_list))
    GSM.Num_appletree.append(len(GSM.Appletree_list))
    GSM.Num_tiger.append(len(GSM.Tigers_list))
    GSM.Num_wolf.append(len(GSM.Wolf_list))
    GSM.Num_fox.append(len(GSM.Fox_list))
    GSM.Num_rabbit.append(len(GSM.Rabbits_list))
    GSM.Num_goat.append(len(GSM.Goats_list))
    GSM.SumAllAgents.append(GSM.Num_dandelion[-1] + GSM.Num_cow[-1] + GSM.Num_tiger[-1] + GSM.Num_wolf[-1] + GSM.Num_rabbit[-1] + GSM.Num_appletree[-1] + GSM.Num_fox[-1] + GSM.Num_berrybush[-1] + GSM.Num_goat[-1])

    GSM.Cows_hunger.append(CalculateAverageStat(GSM.Cows_list, "hunger"))
    GSM.Tigers_hunger.append(CalculateAverageStat(GSM.Tigers_list, "hunger"))
    GSM.Rabbits_hunger.append(CalculateAverageStat(GSM.Rabbits_list, "hunger"))
    GSM.Goats_hunger.append(CalculateAverageStat(GSM.Goats_list, "hunger"))
    GSM.Wolf_hunger.append(CalculateAverageStat(GSM.Wolf_list, "hunger"))
    GSM.Fox_hunger.append(CalculateAverageStat(GSM.Fox_list, "hunger"))

    GSM.Cows_perception.append(CalculateAverageStat(GSM.Cows_list, "perception"))
    GSM.Tigers_perception.append(CalculateAverageStat(GSM.Tigers_list, "perception"))
    GSM.Rabbits_perception.append(CalculateAverageStat(GSM.Rabbits_list, "perception"))
    GSM.Goats_perception.append(CalculateAverageStat(GSM.Goats_list, "perception"))
    GSM.Wolf_perception.append(CalculateAverageStat(GSM.Wolf_list, "perception"))
    GSM.Fox_perception.append(CalculateAverageStat(GSM.Fox_list, "perception"))

    GSM.Cows_speed.append(CalculateAverageStat(GSM.Cows_list, "speed"))
    GSM.Tigers_speed.append(CalculateAverageStat(GSM.Tigers_list, "speed"))
    GSM.Rabbits_speed.append(CalculateAverageStat(GSM.Rabbits_list, "speed"))
    GSM.Goats_speed.append(CalculateAverageStat(GSM.Goats_list, "speed"))
    GSM.Wolf_speed.append(CalculateAverageStat(GSM.Wolf_list, "speed"))
    GSM.Fox_speed.append(CalculateAverageStat(GSM.Fox_list, "speed"))

    if GSM.Visualise_simulation_toggle:
        #TODO: Change displayed speed from being "time between turns" into "turns per second" so "0.06 delay" instead becomes "16.6 turns per second"
        while True:
            #loop to trap the program
            current_time = time.time()
            elapsed_time = current_time - GSM.Last_update_time
            VisualiseScript.EventHandler(GSM)
            if GSM.Visualise_simulation_toggle == False:
                break
            if GSM.Is_paused:
                time.sleep(0.05) #to prevent it eating 25% CPU
                VisualiseScript.VisualiseSimulationDraw(GSM, i+1)  # draw the display window
                continue
            if elapsed_time >= GSM.Sim_delay:
                GSM.Last_update_time = current_time
                VisualiseScript.VisualiseSimulationDraw(GSM, i+1)  # draw the display window
                break
            VisualiseScript.VisualiseSimulationDraw(GSM, i+1)  # draw the display window
            if GSM.Sim_delay > 0.05:
                time.sleep(0.01) #to prevent it eating 25% CPU




#report results
print("\n\n----------SIMULATION END----------")
print(f"World started with {GSM.Num_dandelion[0]} Dandelions, {GSM.Num_berrybush[0]} Berry bushes, {GSM.Num_appletree[0]} Apple trees,"
      f" {GSM.Num_rabbit[0]} Rabbits, {GSM.Num_goat[0]} Goats, {GSM.Num_cow[0]} Cows, {GSM.Num_fox[0]} Foxes, {GSM.Num_wolf[0]} Wolves, and {GSM.Num_tiger[0]} Tigers, Total: {(GSM.SumAllAgents[0])}")
print(f"World ended at turn {GSM.Simulation_Length} with {GSM.Num_dandelion[-1]} Dandelions, {GSM.Num_berrybush[-1]} Berry bushes, "
      f"{GSM.Num_appletree[-1]} Apple trees, {GSM.Num_rabbit[-1]} Rabbits, {GSM.Num_goat[-1]} Goats, {GSM.Num_cow[-1]} Cows, {GSM.Num_fox[-1]} Foxes, "
      f"{GSM.Num_wolf[-1]} Wolves, and {GSM.Num_tiger[-1]} Tigers, Total: {GSM.SumAllAgents[-1]}/{round(pow(GSM.World_size, 2) / GSM.World_size_spawn_tolerance)}")

VisualiseScript.GraphPopulation(GSM)
VisualiseScript.GraphHunger(GSM)
VisualiseScript.GraphPerception(GSM)
VisualiseScript.GraphSpeed(GSM)

VisualiseScript.VisualiseSimulationQuit()