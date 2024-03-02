#handles visualisation and graphing
import plotly.graph_objects as go
import pygame
import re
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
    global Visualise_window #TODO: Finish refactoring these guys...
    global Start_x
    global Start_y
    global Generation_text_font
    global Axis_text_font
    global GUI_text_font
    global Animal_drawing_offset

    global Grid_color
    global Fill_color
    global Tiger_color
    global Rabbit_color
    global Dandelion_color
    global Wolf_color
    global Cow_color
    global Fox_color
    global Berrybush_color
    global Appletree_color

    global Cell_positions
    global Distancebtwrow

    Grid_color = (0, 0, 0)
    Fill_color = (0, 200, 0)
    Tiger_color = (255, 0, 0)
    Fox_color = (224, 156, 18)
    Rabbit_color = (255, 255, 255)
    Dandelion_color = (235, 235, 26)
    Wolf_color = (137, 12, 166)
    Cow_color = (0, 0, 0)
    Berrybush_color = (181, 45, 0)
    Appletree_color = (242, 87, 44)

    Visualise_window = pygame.display.set_mode((GSM.width, GSM.height))
    GSM.Gridsize = round(min((GSM.width, GSM.height)) * 0.8) #use 80% of the smaller dimension
    Cell_positions = []  # Initialize list to hold cell positions
    World_size = worldsize #this is very bad practise I know but this script doesnt have access to main_script globals and its 5am and oh well
    # Calculate starting points to center the grid
    Start_x = (GSM.width - GSM.Gridsize) // 2
    Start_y = (GSM.height - GSM.Gridsize) // 2
    #draw the grid
    Distancebtwrow = GSM.Gridsize // worldsize

    'more variables'
    Visualise_window.fill((0, 200, 0))  # background color
    Animal_drawing_offset = 0.06
    Generation_text_font = pygame.font.SysFont("Arial", Distancebtwrow // 3)  # font and size for agent generation number
    Axis_text_font = pygame.font.SysFont("Arial", Distancebtwrow // 2)  # font and size for grid axis
    GUI_text_font = pygame.font.SysFont("Arial", int(GSM.Gridsize // 15))

    DrawGrid(GSM.width, GSM.height, 0, 0)

    #calculates left top of each cell
    for i in range(worldsize):
        row = []  # Initialize list to hold cell positions for this row
        for j in range(worldsize):
            # Calculate top-left corner of each cell
            cell_x = Start_x + j * Distancebtwrow
            cell_y = Start_y + i * Distancebtwrow
            row.append((cell_x, cell_y))
        Cell_positions.append(row)

def DrawText(text, font, color, x, y):
    'function for drawing text in pygame'
    global Visualise_window
    text = str(text)
    text_image = font.render(text, True, color)
    Visualise_window.blit(text_image, (x, y))


def DrawGrid(width, height, turnN, currentTurnDelay):
    global Visualise_window

    Visualise_window.fill(Fill_color)
    DrawText("Turn " + str(turnN), GUI_text_font, (0, 0, 0), 5, 5)
    DrawText("Speed: " + str(currentTurnDelay), GUI_text_font, (0, 0, 0), width - 230, 5)

    for i in range(World_size + 1):  # +1 to draw the boundary of the grid
        # Vertical line (need to adjust both start and end points)
        if i == 0 or i == World_size:
            pygame.draw.line(Visualise_window, Grid_color,
                             (Start_x + i * Distancebtwrow, Start_y),
                             (Start_x + i * Distancebtwrow, Start_y + Gridsize), width=3)
            # Horizontal line (need to adjust both start and end points)
            pygame.draw.line(Visualise_window, Grid_color,
                             (Start_x, Start_y + i * Distancebtwrow),
                             (Start_x + Gridsize, Start_y + i * Distancebtwrow), width=3)
        else:
            pygame.draw.line(Visualise_window, Grid_color,
                             (Start_x + i * Distancebtwrow, Start_y),
                             (Start_x + i * Distancebtwrow, Start_y + Gridsize))
            # Horizontal line (need to adjust both start and end points)
            pygame.draw.line(Visualise_window, Grid_color,
                             (Start_x, Start_y + i * Distancebtwrow),
                             (Start_x + Gridsize, Start_y + i * Distancebtwrow))
        if i != World_size: #Draw axis numbers
            DrawText(str(i), Axis_text_font, (0, 0, 0), (Start_x + i * Distancebtwrow + Distancebtwrow*0.5), (height - Start_y)) #FIXME: Change this to its own font (X AXIS)
            DrawText(str(World_size - i -1), Axis_text_font, (0, 0, 0), (Start_x - Distancebtwrow/2), (Start_y + i * Distancebtwrow + Distancebtwrow*0.25)) #(Y AXIS)

def EventHandler(currentTurnDelay):
    'this is called separately from VisualiseSimulationDraw so that variable can be returned to main loop'
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # kill program once X is pressed
            VisualiseSimulationQuit() #FIXME: Make X button not lag if used on high speeds

        elif event.type == pygame.KEYDOWN: # For switching sim speed
            if event.key == pygame.K_LEFT:
                if currentTurnDelay > 1:
                    return currentTurnDelay - 0.5
                elif currentTurnDelay == 0.25:
                    return 0.12
                elif currentTurnDelay < 0.25 and currentTurnDelay != 0.03:
                    return currentTurnDelay / 2
                elif currentTurnDelay == 0.03:
                    return 0
                else:
                    return currentTurnDelay - 0.25
            elif event.key == pygame.K_RIGHT:
                if currentTurnDelay >= 1:
                    return currentTurnDelay + 0.5
                elif currentTurnDelay == 0.12:
                    return 0.25
                elif currentTurnDelay == 0:
                    currentTurnDelay = 0.03
                elif currentTurnDelay < 0.12:
                    return currentTurnDelay * 2
                else:
                    return currentTurnDelay + 0.25
    return currentTurnDelay #if no events are detected
def VisualiseSimulationDraw(SumAllAgents, world_agent_list_x_y, turnN, width, height, currentTurnDelay):
    'this is called every main loop iteration'

    global Visualise_window
    global Cell_positions

    DrawGrid(width, height, turnN, currentTurnDelay)


    for x_row_list in world_agent_list_x_y:
        for y_cell in x_row_list:
            if y_cell is None: #empty cell
                continue

            animalname = re.match(r"(\D+)_\d+", y_cell.name) #what animal is this
            animalname = animalname.group(1) #scrape the generation number
            cell_position_x, cell_position_y = Cell_positions[y_cell.y][y_cell.x]   #fixes orientation of coordinate system from top left to bottom left
            cell_position_y = abs(height - cell_position_y - Distancebtwrow)


            if animalname == "Tiger":
                #fixme: On not square resolutions things offset incorrectly - also on world size 25 for some reason?
                pygame.draw.rect(Visualise_window, Tiger_color, pygame.Rect((cell_position_x + Distancebtwrow*Animal_drawing_offset, cell_position_y + Distancebtwrow*Animal_drawing_offset, Distancebtwrow*0.9, Distancebtwrow*0.9))) #window, color, what (start x, start y, sizex , sizey)
            elif animalname == "Rabbit":
                pygame.draw.rect(Visualise_window, Rabbit_color, pygame.Rect((cell_position_x + Distancebtwrow*Animal_drawing_offset, cell_position_y + Distancebtwrow*Animal_drawing_offset, Distancebtwrow*0.9, Distancebtwrow*0.9)))
            elif animalname == "Wolf":
                pygame.draw.rect(Visualise_window, Wolf_color, pygame.Rect((cell_position_x + Distancebtwrow*Animal_drawing_offset, cell_position_y + Distancebtwrow*Animal_drawing_offset, Distancebtwrow*0.9, Distancebtwrow*0.9)))
            elif animalname == "Fox":
                pygame.draw.rect(Visualise_window, Fox_color, pygame.Rect((cell_position_x + Distancebtwrow*Animal_drawing_offset, cell_position_y + Distancebtwrow*Animal_drawing_offset, Distancebtwrow*0.9, Distancebtwrow*0.9)))
            elif animalname == "Dandelion":
                pygame.draw.rect(Visualise_window, Dandelion_color, pygame.Rect((cell_position_x + Distancebtwrow*Animal_drawing_offset, cell_position_y + Distancebtwrow*Animal_drawing_offset, Distancebtwrow*0.9, Distancebtwrow*0.9)))
            elif animalname == "Cow":
                pygame.draw.rect(Visualise_window, Cow_color, pygame.Rect((cell_position_x + Distancebtwrow*Animal_drawing_offset, cell_position_y + Distancebtwrow*Animal_drawing_offset, Distancebtwrow*0.9, Distancebtwrow*0.9)))
            elif animalname == "Berrybush":
                pygame.draw.rect(Visualise_window, Berrybush_color, pygame.Rect((cell_position_x + Distancebtwrow*Animal_drawing_offset, cell_position_y + Distancebtwrow*Animal_drawing_offset, Distancebtwrow*0.9, Distancebtwrow*0.9)))
            elif animalname == "Appletree":
                pygame.draw.rect(Visualise_window, Appletree_color, pygame.Rect((cell_position_x + Distancebtwrow*Animal_drawing_offset, cell_position_y + Distancebtwrow*Animal_drawing_offset, Distancebtwrow*0.9, Distancebtwrow*0.9)))

            if y_cell.type != "Plant": #display animal generation number

                match = re.search(r"\d+$", y_cell.name)
                generation_number = int(match.group())  # Convert the matched string to an integer

                DrawText(generation_number, Generation_text_font, (0, 0, 0), cell_position_x + Distancebtwrow*0.06, cell_position_y + Distancebtwrow*0.06)



    pygame.display.update()
def VisualiseSimulationQuit():
    pygame.display.quit()
    pygame.quit()
    sys.exit()