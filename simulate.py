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

# Defining coefficients
alpha_e = Okuto(T,E)
alpha_h = Okuto(T,E)
# alpha_e = lackner('Mean free',E)[0] # 1/cm 
# alpha_h = lackner('Mean free',E)[1] # 1/cm
alpha = 7500 # 1/cm 

# Define the system of differential equations
def system(z, y):
    Pe, Ph = y
    dPe_dz = alpha_e * (Pe + Ph) - alpha_e * Pe**2 - 2 * alpha_e * Pe * Ph + alpha_e * Ph * Pe**2
    dPh_dz = -alpha_h * (Pe + Ph) + alpha_h * Ph**2 + 2 * alpha_h * Pe * Ph - alpha_e * Pe * Ph**2
    return np.array([dPe_dz, dPh_dz])


Pe0 = 0 # Initial conditions for Pe
h = 1e-6 # number for numerical resolution
z0 = 0 * 1e-4 # coded in cm but in reality it is a micrometre
#z3 = z1 + 1 * 1e-4 # Coordinates of the multiplication zone

def simulate_pde(thicknesses):
    z1, W = thicknesses # thickness of the absorption and multiplication layers
    
    # Finding the threshold
    Ph0_initial = find_threshold(system, z0, W, h, Pe0)
    print(f"Initial value of Ph found by dichotomy: {Ph0_initial}")

    # System resolution
    y0 = np.array([Pe0, Ph0_initial])
    z_values, y_values = runge_kutta_4(system, y0, z0, W, h)

    # Extracting results
    Pe_values = y_values[:, 0]
    Ph_values = y_values[:, 1]
    Pbd_values = Pe_values + Ph_values - Pe_values * Ph_values

    # Calculating the PDE
    QE = np.exp(-alpha * z0) - np.exp(-alpha * z1) # absorption proba
    Pbd = Pbd_values[-1] # avalanche triggering proba
    PDE = QE * Pbd
    #print(f"PDE(z1={z1},W={W}) = {PDE:.3f}")
    
    # Creating subplots
    #fig1, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 10))

    # Plotting the Pbd graph if wanted
    #ax1.plot(z_values, Pe_values, label='Pe', color='blue')
    #ax1.plot(z_values, Ph_values, label='Ph', color='green')
    #ax1.plot(z_values, Pbd_values, label='Pbd', color='red')
    #ax1.set_xlabel('z')
    #ax1.set_ylabel('Values')
    #ax1.legend()
    #ax1.set_title('Solutions of Pe, Ph and Pbd as a function of z')

    # Add the PDE value annotation
    #ax1.text(0.1, 0.6, f'Pbd: {Pbd:.3f}', transform=ax1.transAxes, fontsize=14, bbox=dict(facecolor='white', alpha=0.8))
    #ax1.text(0.1, 0.5, f'QE: {QE:.3f}', transform=ax1.transAxes, fontsize=14, bbox=dict(facecolor='white', alpha=0.8))
    #ax1.text(0.1, 0.4, f'PDE: {PDE:.3f}', transform=ax1.transAxes, fontsize=14, bbox=dict(facecolor='white', alpha=0.8))

    # Drawing of the SPAD diagram
    #draw_layers(ax2, z0, z1, z3, W)

    # Display Pbd and the SPAD diagram
    #plt.tight_layout()
    #plt.show()
    return PDE

def simulate_dcr(thicknesses, concentrations):
    # Simulation du DCR en fonction des épaisseurs et des concentrations de dopage
    # Remplacer par votre propre modèle
    return sum(thicknesses) + sum(concentrations)