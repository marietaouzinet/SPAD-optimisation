import customtkinter as ctk
from plot_layers import draw_layers
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from simulate import Pbd, QE, simulate_pde

# Global appearance configuration
ctk.set_appearance_mode("light")  # Modes: "dark", "light", "system"
ctk.set_default_color_theme("blue")  # Themes: "blue", "green", "dark-blue"
ctk.set_widget_scaling(1.0)

# Create the main window
root = ctk.CTk()
root.title("Layer Parameters")
root.geometry("800x600")

# Create the container for buttons and inputs (button_container)
button_container = ctk.CTkFrame(root)
button_container.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

# Create the container for the graph (graph_container)
graph_container = ctk.CTkFrame(root)
graph_container.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

# Lists of values for dropdown menus
thicknesses = [f"{i/10:.1f} µm" for i in range(1, 41)]
concentrations = [f"10^{i}" for i in range(15, 19)]

# Adding widgets to the button container
thickness_label = ctk.CTkLabel(button_container, text="Thickness values for each layer:")
thickness_label.grid(row=0, column=0, padx=5, pady=5)

thickness_1 = ctk.CTkComboBox(button_container, values=thicknesses)
thickness_1.set("z1")
thickness_1.grid(row=1, column=0, padx=5, pady=5)

thickness_2 = ctk.CTkComboBox(button_container, values=thicknesses)
thickness_2.set("1 µm")
thickness_2.grid(row=2, column=0, padx=5, pady=5)

thickness_3 = ctk.CTkComboBox(button_container, values=thicknesses)
thickness_3.set("1 µm")
thickness_3.grid(row=3, column=0, padx=5, pady=5)

thickness_4 = ctk.CTkComboBox(button_container, values=thicknesses)
thickness_4.set("W")
thickness_4.grid(row=4, column=0, padx=5, pady=5)

concentration_label = ctk.CTkLabel(button_container, text="Doping concentrations for each layer:")
concentration_label.grid(row=0, column=1, padx=5, pady=5)

concentration_1 = ctk.CTkComboBox(button_container, values=concentrations)
concentration_1.set("10^15")
concentration_1.grid(row=1, column=1, padx=5, pady=5)

concentration_2 = ctk.CTkComboBox(button_container, values=concentrations)
concentration_2.set("10^15")
concentration_2.grid(row=2, column=1, padx=5, pady=5)

concentration_3 = ctk.CTkComboBox(button_container, values=concentrations)
concentration_3.set("10^15")
concentration_3.grid(row=3, column=1, padx=5, pady=5)

concentration_4 = ctk.CTkComboBox(button_container, values=concentrations)
concentration_4.set("10^15")
concentration_4.grid(row=4, column=1, padx=5, pady=5)

method_label = ctk.CTkLabel(button_container, text="Coefficient depending on material:")
method_label.grid(row=0, column=2, padx=5, pady=5)

a_entry = ctk.CTkEntry(button_container)
a_entry.insert(0, "0.3")
a_entry.grid(row=1, column=2, padx=5, pady=5)

b_entry = ctk.CTkEntry(button_container)
b_entry.insert(0, "8e5")
b_entry.grid(row=2, column=2, padx=5, pady=5)

c_entry = ctk.CTkEntry(button_container)
c_entry.insert(0, "6.5e-4")
c_entry.grid(row=3, column=2, padx=5, pady=5)

d_entry = ctk.CTkEntry(button_container)
d_entry.insert(0, "6.0e-4")
d_entry.grid(row=4, column=2, padx=5, pady=5)

E_label = ctk.CTkLabel(button_container, text="Electric field (V/cm):")
E_label.grid(row=0, column=3, padx=5, pady=5)
E = ctk.CTkEntry(button_container)
E.insert(0, "6.5e5")  # Using scientific notation
E.grid(row=1, column=3, padx=5, pady=5)

# Function to update the graph
def update_plot():
    z1 = float(thickness_1.get().replace(" µm", "")) * 1e-4
    u = float(thickness_2.get().replace(" µm", "")) * 1e-4
    v = float(thickness_3.get().replace(" µm", "")) * 1e-4
    W = float(thickness_4.get().replace(" µm", "")) * 1e-4

    fig.clf()  
    ax = fig.add_subplot(111)
    draw_layers(ax, z1, u, v, W)
    canvas.draw()

# Function to perform the calculations
def calculate_fonction():
    z1 = float(thickness_1.get().replace(" µm", "")) * 1e-4
    u = float(thickness_2.get().replace(" µm", "")) * 1e-4
    v = float(thickness_3.get().replace(" µm", "")) * 1e-4
    W = float(thickness_4.get().replace(" µm", "")) * 1e-4
    

    try:
        E_value = float(E.get())
    except ValueError:
        resultat_label.configure(text="Invalid electric field value")
        return
    
    try:
        a = float(a_entry.get())
        b = float(b_entry.get())
        c = float(c_entry.get())
        d = float(d_entry.get())
        C = [a,b,c,d]
        P_bd = Pbd(W, T=300, E=E_value,method='Okuto',C=C)
        QE_value = QE(z1)
        thicknesses_value = [z1, u, v, W]
        PDE = simulate_pde(thicknesses_value, 'Okuto',C)
    except Exception as e:
        resultat_label.configure(text=f"Error in calculation: {e}")
        return
    
    # Call update_plot to refresh the graph with the new values
    update_plot()

    resultat_label.configure(text=f"Avalanche triggering probability = {P_bd * 100:.2f} %\nQuantum Efficiency = {QE_value * 100:.2f} %\nPhoto detection efficiency = {PDE * 100:.2f} %")

# Button to perform the calculation
calculate_button = ctk.CTkButton(button_container, text="Calculate", command=calculate_fonction)
calculate_button.grid(row=5, column=0, padx=5, pady=20, columnspan=4)

# Label to display the result of the calculation
resultat_label = ctk.CTkLabel(button_container, text="")
resultat_label.grid(row=6, column=0, padx=5, pady=10, columnspan=4)

# Create the Matplotlib figure
fig = plt.figure(figsize=(10, 5))
ax = fig.add_subplot(111)
draw_layers(ax, 1e-4, 1e-4, 1e-4, 1e-4)

# Integrate the Matplotlib figure into Tkinter
canvas = FigureCanvasTkAgg(fig, master=graph_container)
canvas.get_tk_widget().pack(fill=ctk.BOTH, expand=True)

# Configure the rows and columns to expand correctly
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=2)
root.grid_columnconfigure(0, weight=1)

# Start the main loop
root.mainloop()
