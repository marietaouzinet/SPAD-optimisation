# To show the dependance of the avalanche triggering probability

import numpy as np
import matplotlib.pyplot as plt
from numerical_methods import runge_kutta_4, find_threshold
from Ionisation_rate_model import Okuto

# Constants
T_values = [300, 280, 240, 200]  # Temperatures in K
E_values = np.linspace(4e5, 8e5, 100)  # Electric field in V/cm
d = 1e-4  # Distance in cm (example value)
Pbd_results = {}

for T in T_values:
    Pbd_list = []
    for E in E_values:
        V = E * d  # Convert electric field to voltage
        # Define parameters
        alpha_e = Okuto(T, E)
        alpha_h = Okuto(T, E)
        
        # Define the system of differential equations
        def system(z, y):
            Pe, Ph = y
            dPe_dz = alpha_e * (Pe + Ph) - alpha_e * Pe**2 - 2 * alpha_e * Pe * Ph + alpha_e * Ph * Pe**2
            dPh_dz = -alpha_h * (Pe + Ph) + alpha_h * Ph**2 + 2 * alpha_h * Pe * Ph - alpha_e * Pe * Ph**2
            return np.array([dPe_dz, dPh_dz])
        
        # Initial condition for Pe
        Pe0 = 0
        # Interval for solving
        W = 0.5 * 1e-4
        h = 1e-6
        
        # Find the threshold
        Ph0_initial = find_threshold(system, 0, W, h, Pe0)
        
        # Solve the system
        y0 = np.array([Pe0, Ph0_initial])
        z_values, y_values = runge_kutta_4(system, y0, 0, W, h)
        
        # Extract results
        Pe_values = y_values[:, 0]
        Ph_values = y_values[:, 1]
        Pbd = Pe_values + Ph_values - Pe_values * Ph_values
        Pbd_list.append(Pbd[-1])
    
    Pbd_results[T] = (E_values * d * 1e2, Pbd_list)  # Convert cm to µm for plotting

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
