import pygame
import random
import math
import time

# --- Configuration & Constants ---
WIDTH, HEIGHT = 1000, 700
FPS = 60
BACKGROUND_COLOR = (10, 10, 15)
FOOD_COUNT = 150
MAX_ORGANISMS = 150

# Colors
COLOR_RED = (255, 80, 80)
COLOR_BLUE = (80, 150, 255)
COLOR_FOOD = (50, 200, 100)

# --- Helper Functions ---
def distance(a, b):
    return math.hypot(a.x - b.x, a.y - b.y)

# --- Classes ---

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Food:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.size = 3
        self.energy_value = 15

    def draw(self, screen):
        pygame.draw.circle(screen, COLOR_FOOD, (self.x, self.y), self.size)

class Organism:
    def __init__(self, x, y, dna=None):
        self.x = x
        self.y = y
        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-1, 1)
        
        # Genetics (if no DNA provided, randomize)
        if dna is None:
            self.dna = {
                'speed': random.uniform(2, 6),
                'sense_radius': random.uniform(50, 150),
                'size': random.uniform(4, 10),
                'aggression': random.uniform(0, 1), # 0 = peaceful, 1 = hunter
                'metabolism': random.uniform(0.1, 0.3) # Energy burn rate
            }
        else:
            self.dna = dna
            # Mutate slightly
            for key in self.dna:
                self.dna[key] *= random.uniform(0.9, 1.1)

        self.energy = 100
        self.age = 0
        self.alive = True
        self.color = (0, 0, 0) # Set
