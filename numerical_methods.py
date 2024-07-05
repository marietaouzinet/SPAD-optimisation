import numpy as np

def runge_kutta_4(system, y0, z0, W, h):
    z_values = np.arange(z0, W + h, h)
    y_values = np.zeros((len(z_values), len(y0)))
    y_values[0] = y0
    
    for i in range(1, len(z_values)):
        z = z_values[i - 1]
        y = y_values[i - 1]
        k1 = h * system(z, y)
        k2 = h * system(z + h/2, y + k1/2)
        k3 = h * system(z + h/2, y + k2/2)
        k4 = h * system(z + h, y + k3)
        y_next = y + (k1 + 2*k2 + 2*k3 + k4) / 6
        y_values[i] = np.clip(y_next, 0, 1)
    
    return z_values, y_values

def shooting_function(system, Ph0_initial, z0, W, h, Pe0):
    y0 = np.array([Pe0, Ph0_initial])
    z_values, y_values = runge_kutta_4(system, y0, z0, W, h)
    Ph_final = y_values[-1, 1]
    return Ph_final

def find_threshold(system, z0, W, h, Pe0, tol=1e-6):
    low = 0.0
    high = 1.0
    mid = (low + high) / 2.0
    
    while high - low > tol:
        mid = (low + high) / 2.0
        Ph_final = shooting_function(system, mid, z0, W, h, Pe0)
        
        if Ph_final == 0:
            low = mid
        else:
            high = mid
            
    return mid
