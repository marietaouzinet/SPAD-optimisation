import customtkinter as ctk
from plot_layers import draw_layers
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from simulate import Pbd, QE, simulate_pde

# Configuration de l'apparence globale
ctk.set_appearance_mode("light")  # Modes: "dark", "light", "system"
ctk.set_default_color_theme("blue")  # Thèmes: "blue", "green", "dark-blue"

# Création de la fenêtre principale
root = ctk.CTk()
root.title("Paramètres des couches")
root.geometry("400x300")

# Listes des valeurs pour les menus déroulants
thicknesses = [f"{i/10:.1f} µm" for i in range(1, 41)]
concentrations = [f"10^{i}" for i in range(15, 19)]
ionisation_model = ['Okuto','Lackner']


# Création des menus déroulants pour les épaisseurs
thickness_label = ctk.CTkLabel(root, text="Thickness values for each layer:")
thickness_label.pack(pady=5)

thickness_1 = ctk.CTkComboBox(root, values=thicknesses)
thickness_1.set("0.1 µm")
thickness_1.pack(pady=5)

thickness_2 = ctk.CTkComboBox(root, values=thicknesses)
thickness_2.set("0.1 µm")
thickness_2.pack(pady=5)

thickness_3 = ctk.CTkComboBox(root, values=thicknesses)
thickness_3.set("0.1 µm")
thickness_3.pack(pady=5)

thickness_4 = ctk.CTkComboBox(root, values=thicknesses)
thickness_4.set("0.1 µm")
thickness_4.pack(pady=5)

# Création des menus déroulants pour les concentrations
concentration_label = ctk.CTkLabel(root, text="Doping concentrations values for each layer:")
concentration_label.pack(pady=5)

concentration_1 = ctk.CTkComboBox(root, values=concentrations)
concentration_1.set("10^15")
concentration_1.pack(pady=5)

concentration_2 = ctk.CTkComboBox(root, values=concentrations)
concentration_2.set("10^15")
concentration_2.pack(pady=5)

concentration_3 = ctk.CTkComboBox(root, values=concentrations)
concentration_3.set("10^15")
concentration_3.pack(pady=5)

concentration_4 = ctk.CTkComboBox(root, values=concentrations)
concentration_4.set("10^15")
concentration_4.pack(pady=5)

# Choisir sa méthode de calcul du taux d'ionisation
method = ctk.CTkLabel(root, text="Ionisation model used:")
method.pack(pady=5)
method = ctk.CTkComboBox(root, values=ionisation_model)
method.set("Okuto")
method.pack(pady=5)

# Choisir le champ électrique au sein de la région de multiplication
E_label = ctk.CTkLabel(root, text="Electric field (V/cm):")
E_label.pack(pady=5)
E = ctk.CTkEntry(root)
E.insert(0, "6.5 x10^5")
E.pack(pady=5)

# Fonction pour mettre à jour le schéma
def update_plot():
    z1 = float(thickness_1.get().replace(" µm", "")) * 1e-6
    u = float(thickness_2.get().replace(" µm", "")) * 1e-6
    v = float(thickness_3.get().replace(" µm", "")) * 1e-6
    W = float(thickness_4.get().replace(" µm", "")) * 1e-6

    # Clear the figure
    fig.clf()  
    
    # Créer un nouvel axe et dessiner les couches avec les nouvelles valeurs
    ax = fig.add_subplot(111)
    draw_layers(ax, z1, u, v, W)
    
    # Mettre à jour le canvas pour refléter les changements
    canvas.draw()

def calculer_fonction():
    # Récupérer les valeurs des menus déroulants et les convertir en cm
    z1 = float(thickness_1.get().replace(" µm", "")) * 1e-4
    u = float(thickness_2.get().replace(" µm", "")) * 1e-4
    v = float(thickness_3.get().replace(" µm", "")) * 1e-4
    W = float(thickness_4.get().replace(" µm", "")) * 1e-4
    method_selected = method.get()

    # Récupérer la valeur du champ électrique
    E_value = float(E.get().replace(" x10^5", "")) 
    
    # Effectuer les calculs du Pbd, QE et PDE
    #P_bd = Pbd(W,T=300,E=E_value,method=method_selected)
    #QE = QE(z1)
    thicknesses_value = [z1,u,v,W]
    #PDE = simulate_pde(thicknesses_value, method_selected)

    # Afficher le résultat du calcul
    #resultat_label.config(text=f"Avalanche triggering probability = {P_bd:.2f} %")

# Création de la figure matplotlib
fig = plt.figure(figsize=(10, 5))
ax = fig.add_subplot(111)
draw_layers(ax, 0.1e-6, 0.1e-6, 0.1e-6, 0.1e-6)

# Bouton pour effectuer le calcul
calculer_button = ctk.CTkButton(root, text="Calculer", command=calculer_fonction)
calculer_button.pack(pady=20)

# Label pour afficher le résultat du calcul
resultat_label = ctk.CTkLabel(root, text="")
resultat_label.pack(pady=10)

# Intégration de la figure matplotlib dans Tkinter
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True)

# Lancement de la boucle principale
root.mainloop()