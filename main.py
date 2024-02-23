"""
Replication of Artificial Intelligence, Algorithmic Pricing, and Collusion
    by: Calvano, Calzolari, Denicolò (2020) in Python
    at: https://www.aeaweb.org/articles?id=10.1257/aer.20190623

Original code for duopoly model:
    author: Matteo Courthoud
    date: 07/05/2021
    git: https://github.com/matteocourthoud, https://matteocourthoud.github.io/

Code additions and modifications:
Oligopoly model, plots, and minor code adjustments
    author: Teele Rossi
    date: 21/10/2023
    git: https://github.com/teeross/algo-collusion-with-duopoly-and-oligopoly
"""

#the following code is made for the duopoly model, please switch the following .py files to an equivalent of an oligopoly model if desired
from input.init import model #alternatively change this to init_oligopoly
from input.qlearning import simulate_game
import matplotlib.pyplot as plt
import numpy as np

# Number of simulations
num_simulations = 1 #possible to edit the number of simulations as desired

# List to store results of each simulation
results = []

# Init algorithm and run simulations
for _ in range(num_simulations):
    game = model()
    _, game_instance, _ = simulate_game(game)  # Breaking apart the tuple
    results.append(game_instance)  # Assuming game_instance contains the Q-values

# Plotting the results
for idx, game_instance in enumerate(results):
    plt.plot(game_instance.Q[0, 0, 0, :], label=f'Simulation {idx + 1}')  # Adjust as needed

plt.legend()
plt.title("Q-values across Simulations")
plt.xlabel("Actions")
plt.ylabel("Q-value")
plt.show()
