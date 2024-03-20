import ConsoleLog
import random
def Mutation(agent):
    if random.random() <= agent.GSM.Mutation_chance:
        gene_1 = random.choice(agent.GSM.Mutateable_genes) #TODO: Make preffered_food mutateable gene
        if gene_1 == "speed":
            gene_nerf_2 = "perception"
            ex_gene_buff = agent.speed
            ex_gene_nerf = agent.perception
            if agent.speed != 5 and agent.perception != 1:
                agent.speed = agent.speed + 1
                agent.perception = agent.perception - 1
            else:
                return
        elif gene_1 == "perception":
            gene_nerf_2 = "speed"
            ex_gene_buff = agent.perception
            ex_gene_nerf = agent.speed
            if agent.perception != 5 and agent.speed != 1:
                agent.perception = agent.perception + 1
                agent.speed = agent.speed - 1
            else:
                return
        ConsoleLog.Mutated(agent, gene_1, gene_nerf_2, ex_gene_buff, ex_gene_nerf, agent.GSM.Console_log_mutated)
def PerceptionCheck(agent):
    'Scans area around depending on agents perception. Agents will prioritise moving toward the closest preferable food'
    #Yes thats a D&D reference
    directions_x_y = []
    if agent.perception >= 1:  # lowest perception, only sees up down left right
        directions_x_y_tier1 = []
        directions_x_y_tier1.append([agent.x + 1, agent.y])  # right
        directions_x_y_tier1.append([agent.x - 1, agent.y])  # left
        directions_x_y_tier1.append([agent.x, agent.y + 1])  # up
        directions_x_y_tier1.append([agent.x, agent.y - 1])  # down
        random.shuffle(directions_x_y_tier1)
        directions_x_y.append(directions_x_y_tier1)
    if agent.perception >= 2:  # second perception, sees up-left, up-right, down-left, down-right
        directions_x_y_tier2 = []
        directions_x_y_tier2.append([agent.x - 1, agent.y + 1])  # up-left
        directions_x_y_tier2.append([agent.x + 1, agent.y + 1])  # up-right
        directions_x_y_tier2.append([agent.x - 1, agent.y - 1])  # down-left
        directions_x_y_tier2.append([agent.x + 1, agent.y - 1])  # down-right
        random.shuffle(directions_x_y_tier2)
        directions_x_y.append(directions_x_y_tier2)
    if agent.perception >= 3:  # this guy sees 2 tiles away
        directions_x_y_tier3 = []
        directions_x_y_tier3.append([agent.x + 2, agent.y])  # right 2
        directions_x_y_tier3.append([agent.x - 2, agent.y])  # left 2
        directions_x_y_tier3.append([agent.x, agent.y + 2])  # up 2
        directions_x_y_tier3.append([agent.x, agent.y - 2])  # down 2
        random.shuffle(directions_x_y_tier3)
        directions_x_y.append(directions_x_y_tier3)
    if agent.perception >= 4:  # corners of corners
        directions_x_y_tier4 = []
        directions_x_y_tier4.append([agent.x - 1, agent.y + 2])  # up 2 - left 1
        directions_x_y_tier4.append([agent.x + 1, agent.y + 2])  # up 2 - right 1
        directions_x_y_tier4.append([agent.x - 1, agent.y - 2])  # down 2 - left 1
        directions_x_y_tier4.append([agent.x + 1, agent.y - 2])  # down 2 - right 1
        directions_x_y_tier4.append([agent.x - 2, agent.y + 1])  # up 1 - left 2
        directions_x_y_tier4.append([agent.x + 2, agent.y + 1])  # up 1 - right 2
        directions_x_y_tier4.append([agent.x - 2, agent.y - 1])  # down 1 - left 2
        directions_x_y_tier4.append([agent.x + 2, agent.y - 1])  # down 1 - right 2
        random.shuffle(directions_x_y_tier4)
        directions_x_y.append(directions_x_y_tier4)
    if agent.perception >= 5:  # Bro sees america from here
        directions_x_y_tier5 = []
        directions_x_y_tier5.append([agent.x + 3, agent.y])  # right 3
        directions_x_y_tier5.append([agent.x - 3, agent.y])  # left 3
        directions_x_y_tier5.append([agent.x, agent.y + 3])  # up 3
        directions_x_y_tier5.append([agent.x, agent.y - 3])  # down 3
        random.shuffle(directions_x_y_tier5)
        directions_x_y.append(directions_x_y_tier5)
    # Flatten the list of lists using list comprehension
    directions_x_y = [item for sublist in directions_x_y for item in sublist]
    scan_memory = {}
    for direction in directions_x_y:
        if direction[0] >= agent.GSM.World_size or direction[1] >= agent.GSM.World_size or direction[0] < 0 or direction[1] < 0:  # prevents checking beyond edge of world
            continue
        if agent.GSM.World_agent_list_x_y[direction[0]][direction[1]] is None:  #empty
            ConsoleLog.CheckForFood(agent, direction[0], direction[1], True, agent.GSM.World_agent_list_x_y,
                                    agent.GSM.Console_log_check_for_food)
            continue
        else:   #found something
            ConsoleLog.CheckForFood(agent, direction[0], direction[1], False, agent.GSM.World_agent_list_x_y,
                                    agent.GSM.Console_log_check_for_food)
            # if we found food, eat it and go there:
            if agent.GSM.World_agent_list_x_y[direction[0]][direction[1]].type == agent.food:
                if agent.GSM.World_agent_list_x_y[direction[0]][direction[1]].size == agent.preferred_food:
                    if "nearest_preferred_food" not in scan_memory:
                        scan_memory["nearest_preferred_food"] = direction
                else:
                    if "nearest_other_food" not in scan_memory:
                        if agent.HerbivoreNoEatBig(agent.GSM.World_agent_list_x_y[direction[0]][direction[1]]) == True:
                            scan_memory["nearest_other_food"] = direction   #Only add to memory food a herbivore can't eat (not size bigger)
            elif agent.type == "Herbivore" and agent.GSM.World_agent_list_x_y[direction[0]][direction[1]].type == "Carnivore":
                if "nearest_predator" not in scan_memory:
                    if agent.size == "Large" and agent.GSM.World_agent_list_x_y[direction[0]][direction[1]].size == "Small":
                        continue    #cows dont fear foxes
                    else:
                        scan_memory["nearest_predator"] = direction
    return scan_memory  #return dictionary of what was found