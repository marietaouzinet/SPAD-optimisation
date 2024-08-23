import numpy as np
import matplotlib.pyplot as plt
from best_values import best_values

# Use of a constant electric field within the multiplication layer
E = 6.5 * 1e5 # V/cm

# Temperature
T = 300 #K

# InP/InGaAs SPAD 
coeff = [0.3,8e5,6.5e-4,6e-4]
alpha = 7500

# Optimisation of W and z1 
best_values(T,E,"Okuto",coeff,alpha)





