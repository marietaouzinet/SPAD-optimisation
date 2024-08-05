# Calcule the PDE and DCR parameters

import numpy as np
import matplotlib.pyplot as plt
from numerical_methods import runge_kutta_4, find_threshold
from Ionisation_rate_model import lackner, Okuto

# Use of a constant electric field within the multiplication layer
E = 6.5 * 1e5 # V/cm

# Temperature
T = 300 #K

alpha = 7500 # arborption coefficient in 1/cm

def Pbd(W,method):
    """
    Return the avalanche triggering (or breakdown) probability as a function of
    thickness, temperature, electric field values and the method used to calculate 
    the ionisation rates.
    """
    # W : thickness of the multiplication region in cm
    # This value is coded in cm but in reality it is in micrometres
    
    # Define ionisation parameters
    if method == 'Okuto':
        alpha_e = Okuto(T,E) # 1/cm 
        alpha_h = Okuto(T,E)
    if method == 'Lackner':
        alpha_e = lackner('Mean free',E)[0] # 1/cm
        alpha_h = lackner('Mean free',E)[1]

    # Define the system of differential equations
    def system(z, y):
        Pe, Ph = y
        dPe_dz = alpha_e * (Pe + Ph) - alpha_e * Pe**2 - 2 * alpha_e * Pe * Ph + alpha_e * Ph * Pe**2
        dPh_dz = -alpha_h * (Pe + Ph) + alpha_h * Ph**2 + 2 * alpha_h * Pe * Ph - alpha_e * Pe * Ph**2
        return np.array([dPe_dz, dPh_dz])
    
    # Initial conditions for Pe
    Pe0 = 0
    
    # Resolution interval
    z0 = 0
    h = 1e-6
    
    # Finding the threshold
    Ph0_initial = find_threshold(system, z0, W, h, Pe0)
    print(f"Initial value of Ph found by dichotomy : {Ph0_initial}")

    # System resolution
    y0 = np.array([Pe0, Ph0_initial])
    z_values, y_values = runge_kutta_4(system, y0, z0, W, h)

    # Extracting results
    Pe_values = y_values[:, 0]
    Ph_values = y_values[:, 1]
    Pbd_values = Pe_values + Ph_values - Pe_values * Ph_values

    # Calculating the Pbd or avalanche triggering probability
    Pbd = Pbd_values[-1]
    return Pbd
    
def QE(z1):
    """
    Return the photon absorption probability or quantum efficiency as a function of the 
    thickness of the absorption layer z1.
    """
    # z1 : thickness of the absorption region in cm
    z0 = 0 * 1e-4 # first coordinate of the absorption layer
    QE = np.exp(-alpha * z0) - np.exp(-alpha * z1) # quantum efficiency
    return QE

def simulate_pde(thicknesses,method):
    """
    Return the Photo detection efficiency of the SPAD thanks to QE and Pbd.
    """
    z1,u,v,W = thicknesses # thickness of the layers (we just need z1 and W here)
    PDE = QE(z1) * Pbd(W, method) # photo detection efficiency
    return PDE

def simulate_dcr(thicknesses, concentrations):
    # Simulation du DCR en fonction des épaisseurs et des concentrations de dopage
    # Remplacer par votre propre modèle
    return sum(thicknesses) + sum(concentrations)