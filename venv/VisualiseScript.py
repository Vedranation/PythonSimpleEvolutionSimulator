#handles visualisation and graphing
import plotly.graph_objects as go

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