
class GlobalsManager:
    # TODO: add stone or water or impassable terrain
    # TODO: add world editor
    # TODO: make predators able to see fleeing prey
    # TODO: create loadable settings presets
    # TODO: Make animals able to pass thru flowers: Rabbits get stuck easily
    # TODO: Add individual flower limit (single ratio)
    # TODO: Add consoleLog when running from predator
    # TODO: Add visualiser graph for genes
    if True:       #debug/test mode
        World_size = 20     #how big (box) do you want the world to be1
        Simulation_Length = 60     #how many turns in simulation

        Num_dandelion = [0];
        Num_berrybush = [0];
        Num_appletree = [0];
        Num_rabbit    = [0];
        Num_goat      = [20];
        Num_cow       = [0];
        Num_fox       = [0];
        Num_wolf      = [20];
        Num_tiger     = [0];

        Max_flowers               = 40       #how many flowers can be
        Dandelion_growth_per_turn = 0     #how many Dandelions spawn per turn
        Berrybush_growth_per_turn = 10
        Appletree_growth_per_turn = 0
    else:
        World_size = 40     # how big (box) do you want the world to be1
        Simulation_Length = 600     # how many turns in simulation

        # how many of each agents do you want to start with, stores their numbers each turn
        Num_dandelion = [25];
        Num_berrybush = [25];
        Num_appletree = [25];
        Num_rabbit    = [50];
        Num_goat      = [25];
        Num_cow       = [25];
        Num_fox       = [50];
        Num_wolf      = [50];
        Num_tiger     = [50];

        Max_flowers               = 250       #how many flowers can be
        Dandelion_growth_per_turn = 20     #how many Dandelions spawn per turn
        Berrybush_growth_per_turn = 13
        Appletree_growth_per_turn = 7

    Flower_spawn_cube         = 6  # Cube, including diagonal, how far flowers spawn from each other, (2, 6, None) None disables this
    Minimum_flower_number_for_cube_spawn = 8        #Minimum amount of unique flowers for that plant to spawn in clusters, bigger number means more clusters
    Mutation_chance           = 0.15        #Chance for baby to change genes
    Mutateable_genes          = ["perception", "speed"]  # which genes are permitted to mutate (empty list disables mutations)
    Max_mutation_points       = 6       #how many mutation points can animals use
    Maximum_hunger            = 50     #maximum hunger a creature can have in its belly
    Reproduce_age             = 5   #minimum age before can breed
    Max_hunger_to_reproduce   = 40    #at which hunger value is highest chance to breed
    Base_reproduce_chance     = 0.75     #maximum reproduce chance (at max hunger)
    DeathAge                  = 50       #at how old do animals 100% die (sigmoid)
    Predator_bigger_prey_fight_chance   = 0.4     #for prey 1 size larger, chance to fight it. This is 1/5 worth for 2 size larger
    Predator_bigger_prey_win_chance     = 0.25       #for prey 1 size larger, chance for predator to kill it, else it dies. This is 1/5 worth for 2 size larger
    Well_fed_buff             = 0.3        #at maximum hunger, preys base chance for victory is multiplied by this much
    Animal_breed_cooldown     = 3
    Animal_spawn_cube         = 1       #Cube, including diagonal, how far can animal breed spawn (1 or 2)

    Window_width = 900
    Window_height = 900

    Console_log_start_position          = False
    Console_log_mutated                 = False
    Console_log_avg_perception          = True
    Console_log_avg_speed               = True
    Console_log_check_for_food          = False
    Console_log_found_food              = True
    Console_log_was_eaten               = True
    Console_log_death_starvation        = False
    Console_log_death_oldage            = False
    Console_log_death_battle            = False
    Console_log_born                    = False
    Console_log_random_move             = False
    Console_log_reproduce_chance        = False
    Console_log_fight_big               = False
    Console_log_worldtoosmalltobreed    = False
    Console_log_personalpopulationlimit = False
    Console_log_worldtoosmalltogrow     = False

    Graph_population_toggle = False
    Graph_hunger_toggle = False
    Graph_perception_toggle = True
    Graph_speed_toggle = True
    Visualise_simulation_toggle = True

    Sim_delay = 1    #delay in seconds between each turn

    Grid_color = (0, 0, 0)
    Fill_color = (0, 200, 0)
    Tiger_color = (255, 0, 0)
    Fox_color = (224, 156, 18)
    Rabbit_color = (255, 255, 255)
    Goat_color = (52, 192, 235)
    Dandelion_color = (235, 235, 26)
    Wolf_color = (137, 12, 166)
    Cow_color = (0, 0, 0)
    Berrybush_color = (181, 45, 0)
    Appletree_color = (242, 87, 44)



    'Variables for the program to define and operate on'
    World_agent_list_x_y = []

    World_size_spawn_tolerance = 1.05      #tolerance to world size to prevent overpopulation
    Personal_animal_limit = pow(World_size, 2) * 0.7       #how much % of the world can a single population have before its forbidden from spawning

    Cows_list = []  # initialise lists to store agents
    Rabbits_list = []
    Goats_list = []
    Dandelion_list = []
    Berrybush_list = []
    Appletree_list = []
    Tigers_list = []
    Wolf_list = []
    Fox_list = []

    Cows_hunger = []  # stores average hunger values every turn
    Rabbits_hunger = []
    Goats_hunger = []
    Tigers_hunger = []
    Wolf_hunger = []
    Fox_hunger = []

    Cows_perception = []  # stores average genes values every turn
    Rabbits_perception = []
    Goats_perception = []
    Tigers_perception = []
    Wolf_perception = []
    Fox_perception = []
    Cows_speed = []
    Rabbits_speed = []
    Goats_speed = []
    Tigers_speed = []
    Wolf_speed = []
    Fox_speed = []

    Is_paused = False
    Last_update_time = 0
    SumAllAgents = 0
    Gridsize = 0
    Visualise_window = 0
    Start_x = 0
    Start_y = 0
    Generation_text_font = 0
    Axis_text_font = 0  #Fonts are defined in VisualiseSimulationInit cause it needs stuff before
    GUI_text_font = 0
    Cell_positions = 0
    Distancebtwrow = 0
    Animal_drawing_offset = 0.00

    #placeholder variables for sprites
    background_sprite = 0
    Berrybush_sprite = 0
    Appletree_sprite = 0
    Rabbit_sprite = 0
    Goat_sprite = 0
    Cow_sprite = 0
    Dandelion_sprite = 0
    Fox_sprite = 0
    Wolf_sprite = 0
    Tiger_sprite = 0