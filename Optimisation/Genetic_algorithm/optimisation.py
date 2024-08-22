import random
from deap import base, creator, tools, algorithms
from simulate import simulate_pde, simulate_dcr

# Use of a constant electric field within the multiplication layer
E = 6.5 * 1e5 # V/cm

# Temperature
T = 300 #K

#  Search limits for the thicknesses and doping concentrations.
z_min, z_max = 0.1, 4.0  # Thickness of layers
c_min, c_max = 1e15, 1e18  # Doping concentrations

# Define the structure of individuals and population
creator.create("FitnessMulti", base.Fitness, weights=(1.0, -1.0))  # Maximise PDE (1.0) and minimise DCR (-1.0)
creator.create("Individual", list, fitness=creator.FitnessMulti)

toolbox = base.Toolbox()
toolbox.register("attr_float", random.uniform, z_min, z_max)  # Bornes pour les épaisseurs
toolbox.register("attr_conc", random.uniform, c_min, c_max)  # Bornes pour les concentrations

# Define an individual (4 thicknesses + 4 concentrations)
toolbox.register("individual", tools.initCycle, creator.Individual, 
                 (toolbox.attr_float, toolbox.attr_float, toolbox.attr_float, toolbox.attr_float, 
                  toolbox.attr_conc, toolbox.attr_conc, toolbox.attr_conc, toolbox.attr_conc), n=1)

# Define the population
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# Define the evaluation function
def evaluate(individual):
    """The evaluation function calculates the PDE and DCR values for a given individual 
    (a specific combination of thicknesses and spiking concentrations) and returns these 
    values as a tuple."""
    thicknesses = individual[:4] #  extraction of the first four values 
    concentrations = individual[4:] # the last four values
    pde = simulate_pde(thicknesses)
    dcr = simulate_dcr(thicknesses, concentrations)
    return pde, dcr

toolbox.register("evaluate", evaluate) # Save the evaluation function

# Register genetic operators
toolbox.register("mate", tools.cxBlend, alpha=0.5)
toolbox.register("mutate", tools.mutPolynomialBounded, low=[z_min]*4+[c_min]*4, up=[z_max]*4+[c_max]*4, eta=0.1, indpb=0.2)
toolbox.register("select", tools.selNSGA2)

# Algorithm parameters: initial population size, number of generations, and crossover 
# and mutation probabilities.
population = toolbox.population(n=100) 
ngen = 50
cxpb = 0.9
mutpb = 0.1

# Perform optimization
algorithms.eaMuPlusLambda(population, toolbox, mu=100, lambda_=200, cxpb=cxpb, mutpb=mutpb, ngen=ngen, 
                          stats=None, halloffame=None, verbose=True)

# Extract the solutions of Pareto
pareto_front = tools.sortNondominated(population, len(population), first_front_only=True)[0]

# Display the results
for ind in pareto_front:
    print(f"Épaisseurs: {ind[:4]}, Concentrations: {ind[4:]}, PDE: {ind.fitness.values[0]}, DCR: {ind.fitness.values[1]}")

