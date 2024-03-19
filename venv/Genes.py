import ConsoleLog
import random
def Mutation(agent, GSM):
    if random.random() <= agent.GSM.Mutation_chance:
        gene_1 = random.choice(agent.GSM.Mutateable_genes)
        if gene_1 == "speed":
            gene_nerf_2 = "perception"
            ex_gene_buff = agent.speed
            ex_gene_nerf = agent.perception
            if agent.speed != 5 or agent.perception != 1:
                agent.speed = agent.speed + 1
                agent.perception = agent.perception - 1
            else:
                return
        elif gene_1 == "perception":
            gene_nerf_2 = "speed"
            ex_gene_buff = agent.perception
            ex_gene_nerf = agent.speed
            if agent.perception != 5 or agent.speed != 1:
                agent.perception = agent.perception + 1
                agent.speed = agent.speed - 1
            else:
                return
        ConsoleLog.Mutated(agent, gene_1, gene_nerf_2, ex_gene_buff, ex_gene_nerf, agent.GSM.Console_log_mutated)