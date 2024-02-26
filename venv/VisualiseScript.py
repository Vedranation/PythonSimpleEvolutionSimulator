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
    pygame.init()
    global Visualise_window
    global World_size
    global Gridsize
    global Start_x
    global Start_y

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
    DrawGrid()

    #calculates left top of each cell
    for i in range(worldsize):
        row = []  # Initialize list to hold cell positions for this row
        for j in range(worldsize):
            # Calculate top-left corner of each cell
            cell_x = Start_x + j * Distancebtwrow
            cell_y = Start_y + i * Distancebtwrow
            row.append((cell_x, cell_y))
        Cell_positions.append(row)
    #print(Cell_positions)

def DrawGrid():
    global Visualise_window
    global World_size
    global Gridsize
    global Start_x
    global Start_y
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
    Visualise_window.fill(Fill_color)
    for i in range(World_size + 1):  # +1 to draw the boundary of the grid
        # Vertical line (need to adjust both start and end points)
        pygame.draw.line(Visualise_window, Grid_color,
                         (Start_x + i * Distancebtwrow, Start_y),
                         (Start_x + i * Distancebtwrow, Start_y + Gridsize))
        # Horizontal line (need to adjust both start and end points)
        pygame.draw.line(Visualise_window, Grid_color,
                         (Start_x, Start_y + i * Distancebtwrow),
                         (Start_x + Gridsize, Start_y + i * Distancebtwrow))


def VisualiseSimulationDraw(SumAllAgents, world_agent_list_x_y):
    for event in pygame.event.get():  # kill program once X is pressed
        if event.type == pygame.QUIT:
            VisualiseSimulationQuit() #FIXME: Make X button not lag if used on high speeds

    global Visualise_window
    global TigerIcon
    global Cell_positions
    DrawGrid()
    pygame.event.pump()

    for x_row_list in world_agent_list_x_y:
        for y_cell in x_row_list:
            if y_cell is None: #empty cell
                #print("None")
                continue

            animalname = re.match(r"(\D+)_\d+", y_cell.name) #what animal is this
            animalname = animalname.group(1) #scrape the generation number
            if animalname == "Tiger":
                # print(f"{animalname}, ({y_cell.x}, {y_cell.y}") #this is in COORDINATE SYSTEM XY
                # print(Cell_positions[y_cell.x][y_cell.y]) #this is in PIXEL CELL LOCATION TOP LEFT CORNER OF THE CELL
                cell_position_x, cell_position_y = Cell_positions[y_cell.x][y_cell.y]
                pygame.draw.rect(Visualise_window, Tiger_color, pygame.Rect((cell_position_x + Distancebtwrow*0.06, cell_position_y + Distancebtwrow*0.06, Distancebtwrow*0.9, Distancebtwrow*0.9))) #window, color, what (start x, start y, sizex , sizey)
            elif animalname == "Rabbit":
                cell_position_x, cell_position_y = Cell_positions[y_cell.x][y_cell.y]
                pygame.draw.rect(Visualise_window, Rabbit_color, pygame.Rect((cell_position_x + Distancebtwrow*0.06, cell_position_y + Distancebtwrow*0.06, Distancebtwrow*0.9, Distancebtwrow*0.9)))
            elif animalname == "Wolf":
                cell_position_x, cell_position_y = Cell_positions[y_cell.x][y_cell.y]
                pygame.draw.rect(Visualise_window, Wolf_color, pygame.Rect((cell_position_x + Distancebtwrow*0.06, cell_position_y + Distancebtwrow*0.06, Distancebtwrow*0.9, Distancebtwrow*0.9)))
            elif animalname == "Dandelion":
                cell_position_x, cell_position_y = Cell_positions[y_cell.x][y_cell.y]
                pygame.draw.rect(Visualise_window, Dandelion_color, pygame.Rect((cell_position_x + Distancebtwrow*0.06, cell_position_y + Distancebtwrow*0.06, Distancebtwrow*0.9, Distancebtwrow*0.9)))
            elif animalname == "Cow":
                cell_position_x, cell_position_y = Cell_positions[y_cell.x][y_cell.y]
                pygame.draw.rect(Visualise_window, Cow_color, pygame.Rect((cell_position_x + Distancebtwrow*0.06, cell_position_y + Distancebtwrow*0.06, Distancebtwrow*0.9, Distancebtwrow*0.9)))
            elif animalname == "Berrybush":
                cell_position_x, cell_position_y = Cell_positions[y_cell.x][y_cell.y]
                pygame.draw.rect(Visualise_window, Berrybush_color, pygame.Rect((cell_position_x + Distancebtwrow*0.06, cell_position_y + Distancebtwrow*0.06, Distancebtwrow*0.9, Distancebtwrow*0.9)))



    pygame.display.update()
def VisualiseSimulationQuit():
    pygame.display.quit()
    pygame.quit()
    sys.exit()