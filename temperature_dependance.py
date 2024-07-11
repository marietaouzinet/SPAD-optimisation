# To show the dependance of the avalanche triggering probability

import numpy as np
import matplotlib.pyplot as plt
from numerical_methods import runge_kutta_4, find_threshold
from Ionisation_rate_model import Okuto
from pde import Pbd

# Constants
T_values = [300, 280, 240, 200]  # Temperatures in K
E_values = np.linspace(4e5, 8e5, 40)  # Electric field in V/cm
d = 1e-4  # Distance in cm (example value)
Pbd_results = {}
W = 0.5 * 1e-4 # thickness of the multi layer

for T in T_values:
    Pbd_list = []
    for E in E_values:
        V = E * d  # Convert electric field to voltage
        pbd = Pbd(W,T,E,"Okuto")
        Pbd_list.append(pbd)
    Pbd_results[T] = (E_values * d, Pbd_list)

# Plotting
plt.figure(figsize=(10, 6))

colors = ['black', 'red', 'blue', 'green']
markers = ['s', '^', 'd', '*']
labels = ['300K', '280K', '240K', '200K']

for i, T in enumerate(T_values):
    plt.plot(Pbd_results[T][0], Pbd_results[T][1], label=f'{T}K', color=colors[i], marker=markers[i])

plt.xlabel('Voltage (V)')
plt.ylabel('Probability of Avalanche $P_{bd}$')
plt.title('Probability of Avalanche Breakdown as a Function of Voltage')
plt.legend()
plt.grid(True)
plt.show()
