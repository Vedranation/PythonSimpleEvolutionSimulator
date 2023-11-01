import matplotlib.pyplot as plt
import math

# Constants
MAX_HUNGER_VALUE = 40  # Y almost 100%
sigmoid_slope = 7.0  # the bigger the steeper

# Function to calculate reproduction chance
def reproduction_chance(hunger):
    max_hunger = MAX_HUNGER_VALUE
    hunger_factor = hunger / max_hunger  # Normalize hunger to [0, 1]
    return 1 / (1 + math.exp(-sigmoid_slope * (hunger_factor - 0.5)))

# Generate hunger values and corresponding reproduction chances
hunger_values = range(0, MAX_HUNGER_VALUE + 1)
reproduction_chances = [reproduction_chance(hunger) for hunger in hunger_values]

# Plot the reproduction chance function
plt.plot(hunger_values, reproduction_chances)
plt.title('Reproduction Chance vs. Hunger')
plt.xlabel('Hunger')
plt.ylabel('Reproduction Chance')
plt.grid(True)
#plt.show()



#used in main
Max_hunger_to_reproduce = 40
def HungerReproduceSigmoid(hunger):
    hunger_factor = hunger / Max_hunger_to_reproduce #Normalizes hunger between 0 and 1
    return round(1 / (1 + math.exp(-sigmoid_slope * (hunger_factor - 0.5))), 2)

print(HungerReproduceSigmoid(20))