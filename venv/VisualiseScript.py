#handles visualisation and graphing
import plotly.graph_objects as go
import pygame
import re
import sys
def VisualisePopulation(Simulation_Length, Num_cow, Num_tiger, Num_dandelion, Num_wolf, Num_rabbit, logbool):

    if logbool == True:
        turns_list = [i for i in range(1, Simulation_Length + 1)]
        # Create traces
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=turns_list, y=Num_cow, mode='lines', name='Cows', line=dict(color='black')))
        fig.add_trace(go.Scatter(x=turns_list, y=Num_tiger, mode='lines', name='Tigers', line=dict(color='red')))
        fig.add_trace(go.Scatter(x=turns_list, y=Num_dandelion, mode='lines', name='Dandelions', line=dict(color='green')))
        fig.add_trace(go.Scatter(x=turns_list, y=Num_wolf, mode='lines', name='Wolves', line=dict(color='purple')))
        fig.add_trace(go.Scatter(x=turns_list, y=Num_rabbit, mode='lines', name='Rabbits', line=dict(color='orange')))

        # Add titles and labels
        fig.update_layout(title='Animal Population Over Time',
                          xaxis_title='Turn',
                          yaxis_title='Number of Animals')

        # Show the plot
        fig.show()
    return

def VisualiseHunger(Simulation_Length, Cows_hunger, Rabbits_hunger, Tigers_hunger, Wolf_hunger, logbool):

    if logbool == True:
        # Turns list for X-axis
        turns_list = [i for i in range(1, Simulation_Length + 1)]

        # Create the plot for average hunger
        fig_hunger = go.Figure()
        fig_hunger.add_trace(go.Scatter(x=turns_list, y=Cows_hunger, mode='lines', name='Cows', line=dict(color='black')))
        fig_hunger.add_trace(go.Scatter(x=turns_list, y=Rabbits_hunger, mode='lines', name='Rabbits', line=dict(color='orange')))
        fig_hunger.add_trace(go.Scatter(x=turns_list, y=Tigers_hunger, mode='lines', name='Tigers', line=dict(color='red')))
        fig_hunger.add_trace(go.Scatter(x=turns_list, y=Wolf_hunger, mode='lines', name='Wolves', line=dict(color='purple')))

        # Add titles and labels
        fig_hunger.update_layout(title='Average Animal Hunger Over Time',
                                 xaxis_title='Turn',
                                 yaxis_title='Average Hunger')

        # Show the plot
        fig_hunger.show()
    return

def VisualiseSimulationInit(worldsize, width=800, height=800):
    'Initialises visualisation, and sets variables like font, color etc'
    pygame.init()
    global Visualise_window
    global World_size
    global Gridsize
    global Start_x
    global Start_y
    global Generation_text_font

    global Grid_color
    global Fill_color
    global Tiger_color
    global Rabbit_color
    global Dandelion_color
    global Wolf_color
    global Cow_color
    global Berrybush_color

    global Cell_positions
    global Distancebtwrow

    Generation_text_font = pygame.font.SysFont("Arial", 30)     #font and size for agent generation number

    Grid_color = (0, 0, 0)
    Fill_color = (0, 200, 0)
    Tiger_color = (255, 0, 0)
    Rabbit_color = (224, 156, 18)
    Dandelion_color = (235, 235, 26)
    Wolf_color = (137, 12, 166)
    Cow_color = (0, 0, 0)
    Berrybush_color = (181, 45, 0)

    Cell_positions = []  # Initialize list to hold cell positions
    World_size = worldsize #this is very bad practise I know but this script doesnt have access to main_script globals and its 5am and oh well

    Visualise_window = pygame.display.set_mode((width, height))
    Gridsize = round(min((width, height)) * 0.8) #use 80% of the smaller dimension
    Visualise_window.fill((0, 200, 0))
    # Calculate starting points to center the grid
    Start_x = (width - Gridsize) // 2
    Start_y = (height - Gridsize) // 2
    #draw the grid
    Distancebtwrow = Gridsize // worldsize
    DrawGrid(0)

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


def DrawGrid(turnN):
    global Visualise_window

    Visualise_window.fill(Fill_color)
    DrawText("Turn " + str(turnN), Generation_text_font, (0, 0, 0), 0, 0)

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


def VisualiseSimulationDraw(SumAllAgents, world_agent_list_x_y, turnN, height):
    for event in pygame.event.get():  # kill program once X is pressed
        if event.type == pygame.QUIT:
            VisualiseSimulationQuit() #FIXME: Make X button not lag if used on high speeds

    global Visualise_window
    global Cell_positions
    DrawGrid(turnN)
    pygame.event.pump()

    for x_row_list in world_agent_list_x_y:
        for y_cell in x_row_list:
            if y_cell is None: #empty cell
                continue

            animalname = re.match(r"(\D+)_\d+", y_cell.name) #what animal is this
            animalname = animalname.group(1) #scrape the generation number
            cell_position_x, cell_position_y = Cell_positions[y_cell.y][y_cell.x]   #fixes orientation of coordinate system from top left to bottom left


            cell_position_y = abs(height - cell_position_y)
            print(cell_position_y)


            if animalname == "Tiger":
                # print(f"{animalname}, ({y_cell.x}, {y_cell.y}") #this is in COORDINATE SYSTEM XY
                # print(Cell_positions[y_cell.x][y_cell.y]) #this is in PIXEL CELL LOCATION TOP LEFT CORNER OF THE CELL
                pygame.draw.rect(Visualise_window, Tiger_color, pygame.Rect((cell_position_x + Distancebtwrow*0.06, cell_position_y + Distancebtwrow*0.06, Distancebtwrow*0.9, Distancebtwrow*0.9))) #window, color, what (start x, start y, sizex , sizey)
            elif animalname == "Rabbit":
                pygame.draw.rect(Visualise_window, Rabbit_color, pygame.Rect((cell_position_x + Distancebtwrow*0.06, cell_position_y + Distancebtwrow*0.06, Distancebtwrow*0.9, Distancebtwrow*0.9)))
            elif animalname == "Wolf":
                pygame.draw.rect(Visualise_window, Wolf_color, pygame.Rect((cell_position_x + Distancebtwrow*0.06, cell_position_y + Distancebtwrow*0.06, Distancebtwrow*0.9, Distancebtwrow*0.9)))
            elif animalname == "Dandelion":
                pygame.draw.rect(Visualise_window, Dandelion_color, pygame.Rect((cell_position_x + Distancebtwrow*0.06, cell_position_y + Distancebtwrow*0.06, Distancebtwrow*0.9, Distancebtwrow*0.9)))
            elif animalname == "Cow":
                pygame.draw.rect(Visualise_window, Cow_color, pygame.Rect((cell_position_x + Distancebtwrow*0.06, cell_position_x + Distancebtwrow*0.06, Distancebtwrow*0.9, Distancebtwrow*0.9)))
            elif animalname == "Berrybush":
                pygame.draw.rect(Visualise_window, Berrybush_color, pygame.Rect((cell_position_x + Distancebtwrow*0.06, cell_position_y + Distancebtwrow*0.06, Distancebtwrow*0.9, Distancebtwrow*0.9)))

            if y_cell.type != "Plant": #display animal generation number

                match = re.search(r"\d+$", y_cell.name)
                generation_number = int(match.group())  # Convert the matched string to an integer

                DrawText(generation_number, Generation_text_font, (0, 0, 0), cell_position_x + Distancebtwrow*0.06, cell_position_y + Distancebtwrow*0.06)



    pygame.display.update()
def VisualiseSimulationQuit():
    pygame.display.quit()
    pygame.quit()
    sys.exit()