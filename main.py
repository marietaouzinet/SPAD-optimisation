import numpy as np
import matplotlib.pyplot as plt
from numerical_methods import runge_kutta_4, find_threshold
from plot_layers import draw_layers
from Ionisation_rate_model import lackner, Okuto
from best_values import best_values

# Use of a constant electric field within the multiplication layer
E = 6.5 * 1e5 # V/cm

#Temperature
T = 300 #K

# Optimisation of W and z1 
best_values(T,E,"Okuto")





