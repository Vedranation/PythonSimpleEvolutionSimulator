import matplotlib.pyplot as plt
import math

# Constants
Max_hunger_to_reproduce = 60  # Y almost 100%
sigmoid_slope = 15.0  # the bigger the steeper

# Function to calculate reproduction chance
def HungerReproduceSigmoid(hunger):
    hunger_factor = hunger / Max_hunger_to_reproduce  # Normalizes hunger between 0 and 1
    return round(1 / (1 + math.exp(-sigmoid_slope * (hunger_factor - 0.5))), 2)  # more well fed, more chance to breed


hunger_values = range(0, Max_hunger_to_reproduce + 1)
reproduction_chances = [HungerReproduceSigmoid(hunger) for hunger in hunger_values]
# Plot the reproduction chance function
plt.plot(hunger_values, reproduction_chances)
plt.title('Reproduction Chance vs. Hunger')
plt.xlabel('Hunger')
plt.ylabel('Reproduction Chance')
plt.grid(True)
plt.show()



#used in main
Max_hunger_to_reproduce = 40

print(HungerReproduceSigmoid(10))