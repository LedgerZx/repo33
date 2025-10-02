import numpy as np
import matplotlib.pyplot as plt

# Parameters
alpha = 0.1  # Natural growth rate of prey
beta = 0.02  # Predation rate coefficient
delta = 0.1  # Natural death rate of predators
gamma = 0.01  # Efficiency of turning prey into predators

# Initial conditions
prey0 = 40
predator0 = 9

# Time parameters
t = np.linspace(0, 50, 500)

# Lotka-Volterra equations
def lotka_volterra(t, y):
    prey, predator = y
    dprey_dt = alpha * prey - beta * prey * predator
    dpredator_dt = delta * prey * predator - gamma * predator
    return [dprey_dt, dpredator_dt]

# Solve the ODEs
from scipy.integrate import odeint
y0 = [prey0, predator0]
sol = odeint(lotka_volterra, y0, t)

# Plot the results
plt.figure(figsize=(10, 6))
plt.plot(t, sol[:, 0], label='Prey')
plt.plot(t, sol[:, 1], label='Predator')
plt.xlabel('Time')
plt.ylabel('Population')
plt.title('Lotka-Volterra Predator-Prey Model')
plt.legend()
plt.grid(True)
plt.show()
