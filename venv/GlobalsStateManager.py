
class GlobalsManager:
    World_size = 30     #how big (box) do you want the world to be1
    Simulation_Length = 600     #how many turns in simulation

    #how many of each agents do you want to start with, stores their numbers each turn

    #TODO: add Num_berrybush = [30];

    #TODO: add Num_goat = [30];
    #TODO: add stone or impassable terrain
    #TODO: make animals babies spawn near parents
    #TODO: make predators able to see fleeing prey
    Num_dandelion = [100];
    Num_cow = [20];
    Num_rabbit = [100];
    Num_tiger = [20];
    Num_wolf = [60];
    Num_appletree = [30];
    Num_fox = [10];

    Max_flowers = 200       #how many flowers can be
    Dandelion_growth_per_turn = 30     #how many Dandelions spawn per turn
    Berrybush_growth_per_turn = 7
    Appletree_growth_per_turn = 3
    Maximum_hunger = 50     #maximum hunger a creature can have in its belly
    Reproduce_age = 5   #minimum age before can breed
    Max_hunger_to_reproduce = 40    #at which hunger value is highest chance to breed
    Base_reproduce_chance = 0.75     #maximum reproduce chance (at max hunger)
    DeathAge = 50       #at how old do animals 100% die (sigmoid)
    World_size_spawn_tolerance = 1.05      #tolerance to world size to prevent overpopulation
    Personal_animal_limit = pow(World_size, 2) * 0.7       #how much % of the world can a single population have before its forbidden from spawning
    Predator_bigger_prey_fight_chance = 0.5     #for prey 1 size larger, chance to fight it. This is 1/5 worth for 2 size larger
    Predator_bigger_prey_win_chance = 0.6       #for prey 1 size larger, chance for predator to kill it, else it dies. This is 1/5 worth for 2 size larger
    Well_fed_buff = 0.2        #at maximum hunger, preys base chance for victory is multiplied by this much
    Animal_breed_cooldown = 2

    Window_width = 900
    Window_height = 900

    Console_log_start_position = False
    Console_log_check_for_food = False
    Console_log_found_food = False
    Console_log_was_eaten = False
    Console_log_death_starvation = False
    Console_log_death_oldage = False
    Console_log_death_battle = False
    Console_log_born = False
    Console_log_random_move = False
    Console_log_reproduce_chance = False
    Console_log_fight_big = True
    Console_log_worldtoosmalltobreed = False
    Console_log_personalpopulationlimit = False
    Console_log_worldtoosmalltogrow = False

    Visualise_population_toggle = True
    Visualise_hunger_toggle = True
    Visualise_simulation_toggle = True

    Sim_delay = 0.25    #delay in seconds between each turn