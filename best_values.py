# To find the best value for thickness of absorption and multiplication regions
import numpy as np
import matplotlib.pyplot as plt
from simulate import Pbd, QE, simulate_pde

def best_values(T,E,method):
    """
    Plot two graphs which allow to find the best thicknesses of the multiplication and absorption layers
    """
    z1_values = np.linspace(0.5e-4,4e-4,35)  # thickness of the absorption region
    W_values = np.linspace(0.2e-4, 1.5e-4,10) # thickness of the multiplication region

    # Find the best z1
    QE_list = []
    for z1 in z1_values:
        qe = QE(z1)
        QE_list.append(qe)
    QE_results = (z1_values * 1e4, QE_list)  # Convert cm to µm for plotting

    # Find the best W
    Pbd_list = []
    for W in W_values:
        pbd = Pbd(W,T,E,method)
        Pbd_list.append(pbd)
    Pbd_results = (W_values * 1e4, Pbd_list)

    # Display results
    fig1, (ax1,ax2) = plt.subplots(2, 1, figsize=(6, 9))

    ax1.plot(QE_results[0], QE_results[1], label='QE', color='orange')
    ax1.set_xlabel('Thickness of the absorption layer')
    ax1.set_ylabel('QE')
    ax1.legend()
    ax1.set_title('Photon absorption probability QE as a function of the thickness of the absorption layer')

    ax2.plot(Pbd_results[0], Pbd_results[1], label='Pbd', color='red')
    ax2.set_xlabel('Thickness of the multiplication layer')
    ax2.set_ylabel('Pbd')
    ax2.legend()
    ax2.set_title('Avalanche triggering probability Pbd as a function of the thickness of the multiplication layer')

    plt.tight_layout()
    plt.show()