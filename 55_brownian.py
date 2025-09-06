import numpy as np
import matplotlib.pyplot as plt

# Function to simulate a single step of Brownian motion
def brownian_step(position, step_size, time_step):
    angle = np.random.uniform(0, 2 * np.pi)  # Random direction
    dx = step_size * np.cos(angle) * time_step  # Change in x
    dy = step_size * np.sin(angle) * time_step  # Change in y
    return position + np.array([dx, dy])

# Parameters
num_steps = 1000  # Number of steps to simulate
step_size = 0.1  # Size of each step
time_step = 0.1  # Time increment for each step
initial_position = np.array([0.0, 0.0])  # Starting position

# Simulate the Brownian motion
positions = [initial_position]
for _ in range(num_steps):
    current_position = positions[-1]
    new_position = brownian_step(current_position, step_size, time_step)
    positions.append(new_position)

# Convert positions to numpy array for easier plotting
positions = np.array(positions)

# Plotting the path of the particle
plt.figure(figsize=(10, 6))
plt.plot(positions[:, 0], positions[:, 1], label='Particle Path')
plt.title('Simulation of a Particle in Ocean Currents')
plt.xlabel('X Position')
plt.ylabel('Y Position')
plt.legend()
plt.grid(True)
plt.show()
