from skopt import gp_minimize
from skopt.space import Real
import matplotlib.pyplot as plt
from model import SPADModel
import torch

# Bayesian optimisation minimizes by default

model = SPADModel()

def objective(params): #fonction we want to minimize thanks to the bayesian optimisation
    thickness1, doping1, thickness2, doping2, thickness3, doping3, thickness4, doping4 = params
    model.eval() # put the model in evaluation mode (deactivate dropout, batchnorm...)
    with torch.no_grad(): # Disable backpropagation for evaluation
        X_new = torch.tensor([[thickness1, doping1, thickness2, doping2, thickness3, doping3, thickness4, doping4]], dtype=torch.float32) # Create a tensor with the new parameters
        PDE_pred, DCR_pred = model(X_new) # Predict PDE and DCR with the model
    return -PDE_pred.item() + DCR_pred.item() # Combine the two objectives (maximise PDE and minimise DCR) 

# The search space defines the limits within which Bayesian optimisation will search for optimal parameter values.
space = [
    Real(0.1, 10.0, name='thickness1'), Real(1e15, 1e18, name='doping1'),
    Real(0.1, 10.0, name='thickness2'), Real(1e15, 1e18, name='doping2'),
    Real(0.1, 10.0, name='thickness3'), Real(1e15, 1e18, name='doping3'),
    Real(0.1, 10.0, name='thickness4'), Real(1e15, 1e18, name='doping4')
]

# Bayesian optimisation
# n_calls : Number of optimisation iterations
res = gp_minimize(objective, space, n_calls=50, random_state=42)

optimal_params = res.x
print("Optimal parameters:", optimal_params)

# Visualising Convergence
plt.plot(res.func_vals) # res.func_vals contains the values of the objective function at each iteration.
plt.xlabel('Iteration')
plt.ylabel('Objective Function Value')
plt.title('Convergence Plot')
plt.show()
