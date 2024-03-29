#handles visualisation and graphing
import plotly.graph_objects as go   #5.18.0
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame #2.5.2
import re #2.2.1
import sys
import time

def GraphPopulation(GSM):

    if GSM.Graph_population_toggle == True:
        turns_list = [i for i in range(1, GSM.Simulation_Length + 1)]
        # Create traces
        fig = go.Figure()
        #TODO: Refactor this to use singuar GSM color variable to share with square color instead of handpicking here
        fig.add_trace(go.Scatter(x=turns_list, y=GSM.Num_cow, mode='lines', name='Cows', line=dict(color='black')))
        fig.add_trace(go.Scatter(x=turns_list, y=GSM.Num_tiger, mode='lines', name='Tigers', line=dict(color='red')))
        fig.add_trace(go.Scatter(x=turns_list, y=GSM.Num_dandelion, mode='lines', name='Dandelions', line=dict(color='yellow', dash='dash')))
        fig.add_trace(go.Scatter(x=turns_list, y=GSM.Num_wolf, mode='lines', name='Wolves', line=dict(color='purple')))
        fig.add_trace(go.Scatter(x=turns_list, y=GSM.Num_rabbit, mode='lines', name='Rabbits', line=dict(color='white')))
        fig.add_trace(go.Scatter(x=turns_list, y=GSM.Num_appletree, mode='lines', name='Apple trees', line=dict(color='rgb(242, 87, 44)', dash='dash')))
        fig.add_trace(go.Scatter(x=turns_list, y=GSM.Num_berrybush, mode='lines', name='Berry bushes', line=dict(color='rgb(181, 45, 0)', dash='dash')))
        fig.add_trace(go.Scatter(x=turns_list, y=GSM.Num_fox, mode='lines', name='Foxes', line=dict(color='orange')))
        fig.add_trace(go.Scatter(x=turns_list, y=GSM.Num_goat, mode='lines', name='Goats', line=dict(color='rgb(52, 192, 235)')))

        # Add titles and labels
        fig.update_layout(title='Animal Population Over Time',
                          xaxis_title='Turn',
                          yaxis_title='Number of Animals')

        # Show the plot
        fig.show()
    return

def GraphHunger(GSM):

    if GSM.Graph_hunger_toggle == True:
        # Turns list for X-axis
        turns_list = [i for i in range(1, GSM.Simulation_Length + 1)]
        # Create the plot for average hunger
        fig_hunger = go.Figure()
        fig_hunger.add_trace(go.Scatter(x=turns_list, y=GSM.Cows_hunger, mode='lines', name='Cows', line=dict(color='black')))
        fig_hunger.add_trace(go.Scatter(x=turns_list, y=GSM.Rabbits_hunger, mode='lines', name='Rabbits', line=dict(color='white')))
        fig_hunger.add_trace(go.Scatter(x=turns_list, y=GSM.Goats_hunger, mode='lines', name='Goats', line=dict(color='rgb(52, 192, 235)')))
        fig_hunger.add_trace(go.Scatter(x=turns_list, y=GSM.Tigers_hunger, mode='lines', name='Tigers', line=dict(color='red')))
        fig_hunger.add_trace(go.Scatter(x=turns_list, y=GSM.Wolf_hunger, mode='lines', name='Wolves', line=dict(color='purple')))
        fig_hunger.add_trace(go.Scatter(x=turns_list, y=GSM.Fox_hunger, mode='lines', name='Foxes', line=dict(color='orange')))

        # Add titles and labels
        fig_hunger.update_layout(title='Average Animal Hunger Over Time',
                                 xaxis_title='Turn',
                                 yaxis_title='Average Hunger')
        # Show the plot
        fig_hunger.show()
    return
def GraphPerception(GSM):

    if GSM.Graph_perception_toggle == True:
        turns_list = [i for i in range(1, GSM.Simulation_Length + 1)]
        # Create traces
        fig = go.Figure()

        # Refactor this to use singular GSM color variable to share with square color instead of handpicking here
        fig.add_trace(go.Scatter(x=turns_list, y=GSM.Cows_perception, name='Cows', marker_color='black'))
        fig.add_trace(go.Scatter(x=turns_list, y=GSM.Tigers_perception, name='Tigers', marker_color='red'))

        fig.add_trace(go.Scatter(x=turns_list, y=GSM.Wolf_perception, name='Wolves', marker_color='purple'))
        fig.add_trace(go.Scatter(x=turns_list, y=GSM.Rabbits_perception, name='Rabbits', marker_color='white'))

        fig.add_trace(go.Scatter(x=turns_list, y=GSM.Fox_perception, name='Foxes', marker_color='orange'))
        fig.add_trace(go.Scatter(x=turns_list, y=GSM.Goats_perception, name='Goats', marker_color='rgb(52, 192, 235)'))

        # Add titles and labels
        fig.update_layout(title='Animal Perception',
                          xaxis_title='Turn',
                          yaxis_title='Perception tier')
        # Show the plot
        fig.show()
    return

#Todo: Graphs deserve their own script at this point
def GraphSpeed(GSM):

    if GSM.Graph_speed_toggle == True:
        turns_list = [i for i in range(1, GSM.Simulation_Length + 1)]
        # Create traces
        fig = go.Figure()

        # Refactor this to use singular GSM color variable to share with square color instead of handpicking here
        fig.add_trace(go.Scatter(x=turns_list, y=GSM.Cows_speed, name='Cows', marker_color='black'))
        fig.add_trace(go.Scatter(x=turns_list, y=GSM.Tigers_speed, name='Tigers', marker_color='red'))

        fig.add_trace(go.Scatter(x=turns_list, y=GSM.Wolf_speed, name='Wolves', marker_color='purple'))
        fig.add_trace(go.Scatter(x=turns_list, y=GSM.Rabbits_speed, name='Rabbits', marker_color='white'))

        fig.add_trace(go.Scatter(x=turns_list, y=GSM.Fox_speed, name='Foxes', marker_color='orange'))
        fig.add_trace(go.Scatter(x=turns_list, y=GSM.Goats_speed, name='Goats', marker_color='rgb(52, 192, 235)'))

        # Add titles and labels
        fig.update_layout(title='Animal Speed',
                          xaxis_title='Turn',
                          yaxis_title='Speed tier')
        # Show the plot
        fig.show()
    return

def VisualiseSimulationInit(GSM):
    'Initialises visualisation, and sets variables like font, color etc'
    pygame.init()
    pygame.display.set_caption("Vedran's Animal Sim")


    GSM.Visualise_window = pygame.display.set_mode((GSM.Window_width, GSM.Window_height))
    pygame.display.set_icon(pygame.image.load("AnimalSimImages/tiger.png").convert_alpha())
    GSM.Gridsize = round(min((GSM.Window_width, GSM.Window_height)) * 0.8) #use 80% of the smaller dimension
    GSM.Cell_positions = []  # Initialize list to hold cell positions

    # Calculate starting points to center the grid
    GSM.Start_x = (GSM.Window_width - GSM.Gridsize) // 2
    GSM.Start_y = (GSM.Window_height - GSM.Gridsize) // 2
    #draw the grid
    GSM.Distancebtwrow = GSM.Gridsize // GSM.World_size

    'Load image sprites'
    GSM.background_sprite = pygame.image.load("AnimalSimImages/grass.png").convert_alpha()
    GSM.Dandelion_sprite = pygame.image.load("AnimalSimImages/dandelion.png").convert_alpha()
    GSM.Berrybush_sprite = pygame.image.load("AnimalSimImages/berrybush.png").convert_alpha()
    GSM.Appletree_sprite = pygame.image.load("AnimalSimImages/appletree.png").convert_alpha()
    GSM.Rabbit_sprite = pygame.image.load("AnimalSimImages/rabbit.png").convert_alpha()
    GSM.Goat_sprite = pygame.image.load("AnimalSimImages/goat.png").convert_alpha()
    GSM.Cow_sprite = pygame.image.load("AnimalSimImages/cow.png").convert_alpha()
    GSM.Fox_sprite = pygame.image.load("AnimalSimImages/fox.png").convert_alpha()
    GSM.Wolf_sprite = pygame.image.load("AnimalSimImages/wolf.png").convert_alpha()
    GSM.Tiger_sprite = pygame.image.load("AnimalSimImages/tiger.png").convert_alpha()

    'load fonts'
    GSM.Visualise_window.fill(GSM.Fill_color)  # background color
    GSM.Generation_text_font = pygame.font.SysFont("Arial", GSM.Distancebtwrow // 2)  # font and size for agent generation number
    GSM.Axis_text_font = pygame.font.SysFont("Roboto", GSM.Distancebtwrow // 1)  # font and size for grid axis
    GSM.GUI_text_font = pygame.font.SysFont("Arial", int(GSM.Gridsize // 15))
    GSM.Token_num_text_font = pygame.font.SysFont("Roboto", int(GSM.Gridsize // 15))
    GSM.Token_num_text_font.set_bold(False)

    DrawGrid(GSM, 0)

    #calculates left top of each cell
    for i in range(GSM.World_size):
        row = []  # Initialize list to hold cell positions for this row
        for j in range(GSM.World_size):
            # Calculate top-left corner of each cell
            cell_x = GSM.Start_x + j * GSM.Distancebtwrow
            cell_y = GSM.Start_y + i * GSM.Distancebtwrow
            row.append((cell_x, cell_y))
        GSM.Cell_positions.append(row)

def DrawText(GSM, text, font, color, x, y):
    'function for drawing text in pygame'
    text = str(text)
    text_image = font.render(text, True, color)
    GSM.Visualise_window.blit(text_image, (x, y))

def DrawHUD(GSM, turnN):
    # Draw HUD
    DrawText(GSM, "Turn " + str(turnN), GSM.GUI_text_font, (0, 0, 0), 5, 5)
    DrawText(GSM, "Delay: " + str(GSM.Sim_delay), GSM.GUI_text_font, (0, 0, 0), GSM.Window_width - 230, 5)
    #Display agent numbers
    smaller_dimension = min(GSM.Window_height, GSM.Window_width)
    present_tokens = 0

    def DrawAgentIconAndNumber(animal_sprite, animal_num_list):
        nonlocal present_tokens
        if animal_num_list[0] == 0: #Don't display number of animals that were never spawned
            return
        #TODO: add greyscale when species dies out

        hud_animal = pygame.transform.scale(animal_sprite, (smaller_dimension * 0.06, smaller_dimension * 0.06))
        GSM.Visualise_window.blit(hud_animal, ((GSM.Window_width * 0.06) * present_tokens, GSM.Window_height * 0.93))

        text = str(animal_num_list[-1])
        text_width, text_height = GSM.Token_num_text_font.size(text)
        text_x = ((GSM.Window_width * 0.06) * present_tokens) + (int(smaller_dimension * 0.06) - text_width) / 2
        text_y = (GSM.Window_height * 0.93) + (int(smaller_dimension * 0.06) - text_height) / 2
        DrawText(GSM, text, GSM.Token_num_text_font, (0, 0, 0), text_x, text_y)
        present_tokens += 1

    DrawAgentIconAndNumber(GSM.Dandelion_sprite, GSM.Num_dandelion)
    DrawAgentIconAndNumber(GSM.Berrybush_sprite, GSM.Num_berrybush)
    DrawAgentIconAndNumber(GSM.Appletree_sprite, GSM.Num_appletree)

    DrawAgentIconAndNumber(GSM.Rabbit_sprite, GSM.Num_rabbit)
    DrawAgentIconAndNumber(GSM.Goat_sprite, GSM.Num_goat)
    DrawAgentIconAndNumber(GSM.Cow_sprite, GSM.Num_cow)

    DrawAgentIconAndNumber(GSM.Fox_sprite, GSM.Num_fox)
    DrawAgentIconAndNumber(GSM.Wolf_sprite, GSM.Num_wolf)
    DrawAgentIconAndNumber(GSM.Tiger_sprite, GSM.Num_tiger)

def DrawGrid(GSM, turnN):

    #Draw background
    scaled_background = pygame.transform.scale(GSM.background_sprite, (GSM.Window_width, GSM.Window_height))
    GSM.Visualise_window.blit(scaled_background, (0, 0))

    DrawHUD(GSM, turnN)

    #Draw grid
    for i in range(GSM.World_size + 1):  # +1 to draw the boundary of the grid
        # Vertical line (need to adjust both start and end points)
        if i == 0 or i == GSM.World_size:
            pygame.draw.line(GSM.Visualise_window, GSM.Grid_color,
                             (GSM.Start_x + i * GSM.Distancebtwrow, GSM.Start_y),
                             (GSM.Start_x + i * GSM.Distancebtwrow, GSM.Start_y + GSM.Gridsize), width=3)
            # Horizontal line (need to adjust both start and end points)
            pygame.draw.line(GSM.Visualise_window, GSM.Grid_color,
                             (GSM.Start_x, GSM.Start_y + i * GSM.Distancebtwrow),
                             (GSM.Start_x + GSM.Gridsize, GSM.Start_y + i * GSM.Distancebtwrow), width=3)
        else:
            pygame.draw.line(GSM.Visualise_window, GSM.Grid_color,
                             (GSM.Start_x + i * GSM.Distancebtwrow, GSM.Start_y),
                             (GSM.Start_x + i * GSM.Distancebtwrow, GSM.Start_y + GSM.Gridsize))
            # Horizontal line (need to adjust both start and end points)
            pygame.draw.line(GSM.Visualise_window, GSM.Grid_color,
                             (GSM.Start_x, GSM.Start_y + i * GSM.Distancebtwrow),
                             (GSM.Start_x + GSM.Gridsize, GSM.Start_y + i * GSM.Distancebtwrow))
        if i != GSM.World_size: #Draw axis numbers
            DrawText(GSM, str(i), GSM.Axis_text_font, (0, 0, 0), (GSM.Start_x + i * GSM.Distancebtwrow + GSM.Distancebtwrow*0.27), (GSM.Window_height - GSM.Start_y + GSM.Distancebtwrow*0.1)) #(X AXIS)
            DrawText(GSM, str(GSM.World_size - i -1), GSM.Axis_text_font, (0, 0, 0), (GSM.Start_x - GSM.Distancebtwrow*0.8), (GSM.Start_y + i * GSM.Distancebtwrow + GSM.Distancebtwrow*0.25)) #(Y AXIS)

def EventHandler(GSM):
    'this is called separately from VisualiseSimulationDraw so that variable can be returned to main loop'
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # kill program once X is pressed
            VisualiseSimulationQuit()

        elif event.type == pygame.KEYDOWN: # Checks keyboard presses
            if event.key == pygame.K_LEFT:
                if GSM.Sim_delay > 1:
                    GSM.Sim_delay = GSM.Sim_delay - 0.5
                elif GSM.Sim_delay == 0.25:
                    GSM.Sim_delay = 0.12
                elif GSM.Sim_delay < 0.25 and GSM.Sim_delay != 0.03:
                    GSM.Sim_delay = GSM.Sim_delay / 2
                elif GSM.Sim_delay == 0.03:
                    GSM.Sim_delay = 0
                else:
                    GSM.Sim_delay = GSM.Sim_delay - 0.25
            elif event.key == pygame.K_RIGHT:
                if GSM.Sim_delay >= 1:
                    GSM.Sim_delay = GSM.Sim_delay + 0.5
                elif GSM.Sim_delay == 0.12:
                    GSM.Sim_delay = 0.25
                elif GSM.Sim_delay == 0:
                    GSM.Sim_delay = 0.03
                elif GSM.Sim_delay < 0.12:
                    GSM.Sim_delay = GSM.Sim_delay * 2
                else:
                    GSM.Sim_delay = GSM.Sim_delay + 0.25
            elif event.key == pygame.K_p:
                GSM.Is_paused = not GSM.Is_paused
            elif event.key == pygame.K_ESCAPE:
                GSM.Visualise_simulation_toggle = False
                pygame.quit()
def VisualiseSimulationDraw(GSM, turnN):
    'this is called every main loop iteration'

    DrawGrid(GSM, turnN)

    for x_row_list in GSM.World_agent_list_x_y:
        for y_cell in x_row_list:
            if y_cell is None: #empty cell
                continue

            animalname = re.match(r"(\D+)_\d+", y_cell.name) #what animal is this
            animalname = animalname.group(1) #scrape the generation number
            cell_position_x, cell_position_y = GSM.Cell_positions[y_cell.y][y_cell.x]   #fixes orientation of coordinate system from top left to bottom left
            cell_position_y = abs(GSM.Window_height - cell_position_y - GSM.Distancebtwrow)

            if animalname == "Tiger":
                #fixme: On not square resolutions things offset incorrectly - also on world size 15 and 25 for some reason?
                #TODO: Make it toggleable to switch from good graphics to simple
                #TODO: Add zoom in, and pan around
                #TODO: Make it clickable on specific agent to see its stats and track it
                #TODO: Add a "walking" transition animation so its easier to tell where animal moves (especially for higher speed animals)
                #fixme: This visualise trash can be refactored into single function (dont be yandere dev with infinite IF's)

                # pygame.draw.rect(GSM.Visualise_window, GSM.Tiger_color, pygame.Rect((cell_position_x + GSM.Distancebtwrow*GSM.Animal_drawing_offset, cell_position_y + GSM.Distancebtwrow*GSM.Animal_drawing_offset, GSM.Distancebtwrow*0.9, GSM.Distancebtwrow*0.9))) #window, color, what (start x, start y, sizex , sizey)
                scaled_tiger = pygame.transform.scale(GSM.Tiger_sprite, (GSM.Distancebtwrow, GSM.Distancebtwrow))
                GSM.Visualise_window.blit(scaled_tiger, ((cell_position_x + GSM.Distancebtwrow * GSM.Animal_drawing_offset, cell_position_y + GSM.Distancebtwrow * GSM.Animal_drawing_offset)))
            elif animalname == "Rabbit":
                # pygame.draw.rect(GSM.Visualise_window, GSM.Rabbit_color, pygame.Rect((cell_position_x + GSM.Distancebtwrow*GSM.Animal_drawing_offset, cell_position_y + GSM.Distancebtwrow*GSM.Animal_drawing_offset, GSM.Distancebtwrow*0.9, GSM.Distancebtwrow*0.9)))
                scaled_rabbit = pygame.transform.scale(GSM.Rabbit_sprite, (GSM.Distancebtwrow, GSM.Distancebtwrow))
                GSM.Visualise_window.blit(scaled_rabbit, ((cell_position_x + GSM.Distancebtwrow * GSM.Animal_drawing_offset, cell_position_y + GSM.Distancebtwrow * GSM.Animal_drawing_offset)))
            elif animalname == "Goat":
                # pygame.draw.rect(GSM.Visualise_window, GSM.Goat_color, pygame.Rect((cell_position_x + GSM.Distancebtwrow*GSM.Animal_drawing_offset, cell_position_y + GSM.Distancebtwrow*GSM.Animal_drawing_offset, GSM.Distancebtwrow*0.9, GSM.Distancebtwrow*0.9)))
                scaled_goat = pygame.transform.scale(GSM.Goat_sprite, (GSM.Distancebtwrow, GSM.Distancebtwrow))
                GSM.Visualise_window.blit(scaled_goat, ((cell_position_x + GSM.Distancebtwrow * GSM.Animal_drawing_offset, cell_position_y + GSM.Distancebtwrow * GSM.Animal_drawing_offset)))
            elif animalname == "Wolf":
                # pygame.draw.rect(GSM.Visualise_window, GSM.Wolf_color, pygame.Rect((cell_position_x + GSM.Distancebtwrow*GSM.Animal_drawing_offset, cell_position_y + GSM.Distancebtwrow*GSM.Animal_drawing_offset, GSM.Distancebtwrow*0.9, GSM.Distancebtwrow*0.9)))
                scaled_wolf = pygame.transform.scale(GSM.Wolf_sprite, (GSM.Distancebtwrow, GSM.Distancebtwrow))
                GSM.Visualise_window.blit(scaled_wolf, ((cell_position_x + GSM.Distancebtwrow * GSM.Animal_drawing_offset, cell_position_y + GSM.Distancebtwrow * GSM.Animal_drawing_offset)))
            elif animalname == "Fox":
                # pygame.draw.rect(GSM.Visualise_window, GSM.Fox_color, pygame.Rect((cell_position_x + GSM.Distancebtwrow*GSM.Animal_drawing_offset, cell_position_y + GSM.Distancebtwrow*GSM.Animal_drawing_offset, GSM.Distancebtwrow*0.9, GSM.Distancebtwrow*0.9)))
                scaled_fox = pygame.transform.scale(GSM.Fox_sprite, (GSM.Distancebtwrow, GSM.Distancebtwrow))
                GSM.Visualise_window.blit(scaled_fox, ((cell_position_x + GSM.Distancebtwrow * GSM.Animal_drawing_offset, cell_position_y + GSM.Distancebtwrow * GSM.Animal_drawing_offset)))
            elif animalname == "Dandelion":
                # pygame.draw.rect(GSM.Visualise_window, GSM.Dandelion_color, pygame.Rect((cell_position_x + GSM.Distancebtwrow*GSM.Animal_drawing_offset, cell_position_y + GSM.Distancebtwrow*GSM.Animal_drawing_offset, GSM.Distancebtwrow*0.9, GSM.Distancebtwrow*0.9)))
                scaled_dandelion = pygame.transform.scale(GSM.Dandelion_sprite, (GSM.Distancebtwrow, GSM.Distancebtwrow))
                GSM.Visualise_window.blit(scaled_dandelion, ((cell_position_x + GSM.Distancebtwrow * GSM.Animal_drawing_offset, cell_position_y + GSM.Distancebtwrow * GSM.Animal_drawing_offset)))
            elif animalname == "Cow":
                # pygame.draw.rect(GSM.Visualise_window, GSM.Cow_color, pygame.Rect((cell_position_x + GSM.Distancebtwrow*GSM.Animal_drawing_offset, cell_position_y + GSM.Distancebtwrow*GSM.Animal_drawing_offset, GSM.Distancebtwrow*0.9, GSM.Distancebtwrow*0.9)))
                scaled_cow = pygame.transform.scale(GSM.Cow_sprite, (GSM.Distancebtwrow, GSM.Distancebtwrow))
                GSM.Visualise_window.blit(scaled_cow, ((cell_position_x + GSM.Distancebtwrow * GSM.Animal_drawing_offset, cell_position_y + GSM.Distancebtwrow * GSM.Animal_drawing_offset)))
            elif animalname == "Berrybush":
                # pygame.draw.rect(GSM.Visualise_window, GSM.Berrybush_color, pygame.Rect((cell_position_x + GSM.Distancebtwrow*GSM.Animal_drawing_offset, cell_position_y + GSM.Distancebtwrow*GSM.Animal_drawing_offset, GSM.Distancebtwrow*0.9, GSM.Distancebtwrow*0.9)))
                scaled_berrybush = pygame.transform.scale(GSM.Berrybush_sprite, (GSM.Distancebtwrow, GSM.Distancebtwrow))
                GSM.Visualise_window.blit(scaled_berrybush, ((cell_position_x + GSM.Distancebtwrow * GSM.Animal_drawing_offset, cell_position_y + GSM.Distancebtwrow * GSM.Animal_drawing_offset)))
            elif animalname == "Appletree":
                # pygame.draw.rect(GSM.Visualise_window, GSM.Appletree_color, pygame.Rect((cell_position_x + GSM.Distancebtwrow*GSM.Animal_drawing_offset, cell_position_y + GSM.Distancebtwrow*GSM.Animal_drawing_offset, GSM.Distancebtwrow*0.9, GSM.Distancebtwrow*0.9)))
                scaled_appletree = pygame.transform.scale(GSM.Appletree_sprite, (GSM.Distancebtwrow, GSM.Distancebtwrow))
                GSM.Visualise_window.blit(scaled_appletree, ((cell_position_x + GSM.Distancebtwrow*GSM.Animal_drawing_offset, cell_position_y + GSM.Distancebtwrow*GSM.Animal_drawing_offset)))

            if y_cell.type != "Plant": #display animal generation number

                match = re.search(r"\d+$", y_cell.name)
                generation_number = int(match.group())  # Convert the matched string to an integer

                DrawText(GSM, generation_number, GSM.Generation_text_font, (255, 255, 255), cell_position_x + GSM.Distancebtwrow*0.06, cell_position_y + GSM.Distancebtwrow*0.06)



    pygame.display.update()
def VisualiseSimulationQuit():
    pygame.display.quit()
    pygame.quit()
    sys.exit()