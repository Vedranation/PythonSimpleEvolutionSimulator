#handles visualisation and graphing
import plotly.graph_objects as go
import pygame
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
    Visualise_window = pygame.display.set_mode((width, height))
    gridsize = round(min((width, height)) * 0.8) #use 80% of the smaller dimension
    Visualise_window.fill((0, 200, 0))

    # Calculate starting points to center the grid
    start_x = (width - gridsize) // 2
    start_y = (height - gridsize) // 2
    grid_color = (0, 0, 0)

    #draw the grid
    distancebtwrow = gridsize // worldsize
    cell_positions = []  # Initialize list to hold cell positions

    #calculates left top of each cell
    for i in range(worldsize):
        row = []  # Initialize list to hold cell positions for this row
        for j in range(worldsize):
            # Calculate top-left corner of each cell
            cell_x = start_x + j * distancebtwrow
            cell_y = start_y + i * distancebtwrow
            row.append((cell_x, cell_y))

        cell_positions.append(row)

    print(cell_positions)

    for i in range(worldsize + 1):  # +1 to draw the boundary of the grid
        # Vertical line (need to adjust both start and end points)
        pygame.draw.line(Visualise_window, grid_color,
                         (start_x + i * distancebtwrow, start_y),
                         (start_x + i * distancebtwrow, start_y + gridsize))
        # Horizontal line (need to adjust both start and end points)
        pygame.draw.line(Visualise_window, grid_color,
                         (start_x, start_y + i * distancebtwrow),
                         (start_x + gridsize, start_y + i * distancebtwrow))


    global TigerIcon
    TigerIcon = pygame.Rect((start_x, start_y, 30, 30))




def VisualiseSimulationDraw():
    pygame.draw.rect(Visualise_window, (255, 0, 0), TigerIcon)
    pygame.display.update()
def VisualiseSimulationQuit():
    pygame.quit()