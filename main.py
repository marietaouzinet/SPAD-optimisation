import numpy as np
import matplotlib.pyplot as plt
from numerical_methods import runge_kutta_4, find_threshold
from plot_layers import draw_layers

# Définir les paramètres
alpha_e = 0.85
alpha_h = 0.55
alpha = 7500

# Coordinates of the absorption zone
z0 = 0
z1 = 3.5

# Coordonnées de la zone de multiplication
z3 = z1 + 1

# Définir le système d'équations différentielles
def system(z, y):
    Pe, Ph = y
    dPe_dz = alpha_e * (Pe + Ph) - alpha_e * Pe**2 - 2 * alpha_e * Pe * Ph + alpha_e * Ph * Pe**2
    dPh_dz = -alpha_h * (Pe + Ph) + alpha_h * Ph**2 + 2 * alpha_h * Pe * Ph - alpha_e * Pe * Ph**2
    return np.array([dPe_dz, dPh_dz])

# Conditions initiales pour Pe
Pe0 = 0

# Intervalle de résolution
z0 = 0.0
W = 2.5
h = 0.01

# Trouver le seuil
Ph0_initial = find_threshold(system, z0, W, h, Pe0)
print(f"Valeur initiale de Ph trouvée par dichotomie : {Ph0_initial}")

# Résolution du système
y0 = np.array([Pe0, Ph0_initial])
z_values, y_values = runge_kutta_4(system, y0, z0, W, h)

# Extraction des résultats
Pe_values = y_values[:, 0]
Ph_values = y_values[:, 1]
Pbd_values = Pe_values + Ph_values - Pe_values * Ph_values

# Calcul du PDE
QE = np.exp(-alpha * z0 * 1e-4) - np.exp(-alpha * z1 * 1e-4)
Pbd = Pbd_values[-1]
PDE = QE * Pbd
print("Le PDE obtenu avec les épaisseurs du schéma du SPAD est", PDE)

# Création des subplots
fig1, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 10))

# Tracé du graphique de Pbd
ax1.plot(z_values, Pe_values, label='Pe', color='blue')
ax1.plot(z_values, Ph_values, label='Ph', color='green')
ax1.plot(z_values, Pbd_values, label='Pbd', color='red')
ax1.set_xlabel('z')
ax1.set_ylabel('Values')
ax1.legend()
ax1.set_title('Solutions of Pe, Ph and Pbd as a function of z')

# Ajouter l'annotation de la valeur PDE
ax1.text(0.1, 0.6, f'Pbd: {Pbd:.3f}', transform=ax1.transAxes, fontsize=14, bbox=dict(facecolor='white', alpha=0.8))
ax1.text(0.1, 0.5, f'QE: {QE:.3f}', transform=ax1.transAxes, fontsize=14, bbox=dict(facecolor='white', alpha=0.8))
ax1.text(0.1, 0.4, f'PDE: {PDE:.3f}', transform=ax1.transAxes, fontsize=14, bbox=dict(facecolor='white', alpha=0.8))

# Tracé du graphique du SPAD
draw_layers(ax2, z0, z1, z3, W)

# Afficher Pbd et le schéma du SPAD
plt.tight_layout()
plt.show()
