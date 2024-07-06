import numpy as np 

# Use of the Lackner model to take account of the energy that charge carriers must acquire in order to ionise other atoms


# Model

def lackner(coef,E):
    if coef == 'Van Over': #Use of the Van Overstraeten and De Man constants a and b in V/cm
        # For electrons
        a_n = 0.703 * 1e6
        b_n = 1.231 * 1e6
        # For holes
        a_p = 1.582 * 1e6
        b_p = 2.036 * 1e6
    if coef == 'Mean free': #Use of the Mean free path constants a and b in V/cm
        a_n = 1.316 * 1e6
        b_n = 1.474 * 1e6
        a_p = 1.818 * 1e6
        b_p = 2.036 * 1e6
    # Expression of the coefficient z 
    z = 1 + (b_n / E) * np.exp(-(b_n / E)) + (b_p / E) * np.exp(-(b_p / E))
    # Expressions of the ionisation rates for electrons and holes
    alpha_n = (a_n / z) * np.exp(-(b_n / E))
    alpha_p = (a_p / z) * np.exp(-(b_p / E))
    print(f"Ionisation rates : for electrons ",alpha_n, " and for holes", alpha_p)
    return alpha_n, alpha_p
