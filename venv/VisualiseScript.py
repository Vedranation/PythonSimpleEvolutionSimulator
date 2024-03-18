#handles visualisation and graphing
import plotly.graph_objects as go   #2.2.1
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame #5.18.0
import re #2.5.2
import sys


def VisualisePopulation(GSM):

    if GSM.Visualise_population_toggle == True:
        turns_list = [i for i in range(1, GSM.Simulation_Length + 1)]
        # Create traces
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=turns_list, y=GSM.Num_cow, mode='lines', name='Cows', line=dict(color='black')))
        fig.add_trace(go.Scatter(x=turns_list, y=GSM.Num_tiger, mode='lines', name='Tigers', line=dict(color='red')))
        fig.add_trace(go.Scatter(x=turns_list, y=GSM.Num_dandelion, mode='lines', name='Dandelions', line=dict(color='yellow', dash='dash')))
        fig.add_trace(go.Scatter(x=turns_list, y=GSM.Num_wolf, mode='lines', name='Wolves', line=dict(color='purple')))
        fig.add_trace(go.Scatter(x=turns_list, y=GSM.Num_rabbit, mode='lines', name='Rabbits', line=dict(color='white')))
        fig.add_trace(go.Scatter(x=turns_list, y=GSM.Num_appletree, mode='lines', name='Apple trees', line=dict(color='rgb(242, 87, 44)', dash='dash')))
        fig.add_trace(go.Scatter(x=turns_list, y=GSM.Num_fox, mode='lines', name='Foxes', line=dict(color='orange')))


        # Add titles and labels
        fig.update_layout(title='Animal Population Over Time',
                          xaxis_title='Turn',
                          yaxis_title='Number of Animals')

        # Show the plot
        fig.show()
    return

def VisualiseHunger(GSM):

    if GSM.Visualise_hunger_toggle == True:
        # Turns list for X-axis
        turns_list = [i for i in range(1, GSM.Simulation_Length + 1)]

        # Create the plot for average hunger
        fig_hunger = go.Figure()
        fig_hunger.add_trace(go.Scatter(x=turns_list, y=GSM.Cows_hunger, mode='lines', name='Cows', line=dict(color='black')))
        fig_hunger.add_trace(go.Scatter(x=turns_list, y=GSM.Rabbits_hunger, mode='lines', name='Rabbits', line=dict(color='white')))
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

def VisualiseSimulationInit(GSM):
    'Initialises visualisation, and sets variables like font, color etc'
    pygame.init()


    GSM.Visualise_window = pygame.display.set_mode((GSM.Window_width, GSM.Window_height))
    GSM.Gridsize = round(min((GSM.Window_width, GSM.Window_height)) * 0.8) #use 80% of the smaller dimension
    GSM.Cell_positions = []  # Initialize list to hold cell positions

    # Calculate starting points to center the grid
    GSM.Start_x = (GSM.Window_width - GSM.Gridsize) // 2
    GSM.Start_y = (GSM.Window_height - GSM.Gridsize) // 2
    #draw the grid
    GSM.Distancebtwrow = GSM.Gridsize // GSM.World_size

    'more variables'
    GSM.Visualise_window.fill(GSM.Fill_color)  # background color
    GSM.Generation_text_font = pygame.font.SysFont("Arial", GSM.Distancebtwrow // 3)  # font and size for agent generation number
    GSM.Axis_text_font = pygame.font.SysFont("Arial", GSM.Distancebtwrow // 2)  # font and size for grid axis
    GSM.GUI_text_font = pygame.font.SysFont("Arial", int(GSM.Gridsize // 15))

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


def DrawGrid(GSM, turnN):

    GSM.Visualise_window.fill(GSM.Fill_color)
    DrawText(GSM, "Turn " + str(turnN), GSM.GUI_text_font, (0, 0, 0), 5, 5)
    DrawText(GSM, "Speed: " + str(GSM.Sim_delay), GSM.GUI_text_font, (0, 0, 0), GSM.Window_width - 230, 5)
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
            DrawText(GSM, str(i), GSM.Axis_text_font, (0, 0, 0), (GSM.Start_x + i * GSM.Distancebtwrow + GSM.Distancebtwrow*0.5), (GSM.Window_height - GSM.Start_y))
            DrawText(GSM, str(GSM.World_size - i -1), GSM.Axis_text_font, (0, 0, 0), (GSM.Start_x - GSM.Distancebtwrow/2), (GSM.Start_y + i * GSM.Distancebtwrow + GSM.Distancebtwrow*0.25)) #(Y AXIS)

def EventHandler(GSM):
    'this is called separately from VisualiseSimulationDraw so that variable can be returned to main loop'
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # kill program once X is pressed
            VisualiseSimulationQuit() #FIXME: Make X button not lag if used on high speeds

        elif event.type == pygame.KEYDOWN: # For switching sim speed
            if event.key == pygame.K_LEFT:
                if GSM.Sim_delay > 1:
                    return GSM.Sim_delay - 0.5
                elif GSM.Sim_delay == 0.25:
                    return 0.12
                elif GSM.Sim_delay < 0.25 and GSM.Sim_delay != 0.03:
                    return GSM.Sim_delay / 2
                elif GSM.Sim_delay == 0.03:
                    return 0
                else:
                    return GSM.Sim_delay - 0.25
            elif event.key == pygame.K_RIGHT:
                if GSM.Sim_delay >= 1:
                    return GSM.Sim_delay + 0.5
                elif GSM.Sim_delay == 0.12:
                    return 0.25
                elif GSM.Sim_delay == 0:
                    GSM.Sim_delay = 0.03
                elif GSM.Sim_delay < 0.12:
                    return GSM.Sim_delay * 2
                else:
                    return GSM.Sim_delay + 0.25
    return GSM.Sim_delay #if no events are detected
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
                #fixme: On not square resolutions things offset incorrectly - also on world size 25 for some reason?
                pygame.draw.rect(GSM.Visualise_window, GSM.Tiger_color, pygame.Rect((cell_position_x + GSM.Distancebtwrow*GSM.Animal_drawing_offset, cell_position_y + GSM.Distancebtwrow*GSM.Animal_drawing_offset, GSM.Distancebtwrow*0.9, GSM.Distancebtwrow*0.9))) #window, color, what (start x, start y, sizex , sizey)
            elif animalname == "Rabbit":
                pygame.draw.rect(GSM.Visualise_window, GSM.Rabbit_color, pygame.Rect((cell_position_x + GSM.Distancebtwrow*GSM.Animal_drawing_offset, cell_position_y + GSM.Distancebtwrow*GSM.Animal_drawing_offset, GSM.Distancebtwrow*0.9, GSM.Distancebtwrow*0.9)))
            elif animalname == "Wolf":
                pygame.draw.rect(GSM.Visualise_window, GSM.Wolf_color, pygame.Rect((cell_position_x + GSM.Distancebtwrow*GSM.Animal_drawing_offset, cell_position_y + GSM.Distancebtwrow*GSM.Animal_drawing_offset, GSM.Distancebtwrow*0.9, GSM.Distancebtwrow*0.9)))
            elif animalname == "Fox":
                pygame.draw.rect(GSM.Visualise_window, GSM.Fox_color, pygame.Rect((cell_position_x + GSM.Distancebtwrow*GSM.Animal_drawing_offset, cell_position_y + GSM.Distancebtwrow*GSM.Animal_drawing_offset, GSM.Distancebtwrow*0.9, GSM.Distancebtwrow*0.9)))
            elif animalname == "Dandelion":
                pygame.draw.rect(GSM.Visualise_window, GSM.Dandelion_color, pygame.Rect((cell_position_x + GSM.Distancebtwrow*GSM.Animal_drawing_offset, cell_position_y + GSM.Distancebtwrow*GSM.Animal_drawing_offset, GSM.Distancebtwrow*0.9, GSM.Distancebtwrow*0.9)))
            elif animalname == "Cow":
                pygame.draw.rect(GSM.Visualise_window, GSM.Cow_color, pygame.Rect((cell_position_x + GSM.Distancebtwrow*GSM.Animal_drawing_offset, cell_position_y + GSM.Distancebtwrow*GSM.Animal_drawing_offset, GSM.Distancebtwrow*0.9, GSM.Distancebtwrow*0.9)))
            elif animalname == "Berrybush":
                pygame.draw.rect(GSM.Visualise_window, GSM.Berrybush_color, pygame.Rect((cell_position_x + GSM.Distancebtwrow*GSM.Animal_drawing_offset, cell_position_y + GSM.Distancebtwrow*GSM.Animal_drawing_offset, GSM.Distancebtwrow*0.9, GSM.Distancebtwrow*0.9)))
            elif animalname == "Appletree":
                pygame.draw.rect(GSM.Visualise_window, GSM.Appletree_color, pygame.Rect((cell_position_x + GSM.Distancebtwrow*GSM.Animal_drawing_offset, cell_position_y + GSM.Distancebtwrow*GSM.Animal_drawing_offset, GSM.Distancebtwrow*0.9, GSM.Distancebtwrow*0.9)))

            if y_cell.type != "Plant": #display animal generation number

                match = re.search(r"\d+$", y_cell.name)
                generation_number = int(match.group())  # Convert the matched string to an integer

                DrawText(GSM, generation_number, GSM.Generation_text_font, (0, 0, 0), cell_position_x + GSM.Distancebtwrow*0.06, cell_position_y + GSM.Distancebtwrow*0.06)



    pygame.display.update()
def VisualiseSimulationQuit():
    pygame.display.quit()
    pygame.quit()
    sys.exit()