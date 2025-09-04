import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Constants
G = 6.67430e-11  # Gravitational constant (m^3 kg^-1 s^-2)
SUN_MASS = 1.989e30  # Mass of the Sun (kg)
AU = 1.496e11  # Astronomical Unit (m)

# Planet data (name, mass, initial position, initial velocity)
planets = [
    ("Mercury", 0.330e24, np.array([0.39, 0]), np.array([0, 47.4]) * 1e3),
    ("Venus", 4.87e24, np.array([0.72, 0]), np.array([0, 35.0]) * 1e3),
    ("Earth", 5.97e24, np.array([1.0, 0]), np.array([0, 29.8]) * 1e3),
    ("Mars", 0.642e24, np.array([1.52, 0]), np.array([0, 24.1]) * 1e3
