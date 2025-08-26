import random

# Define constants
POPULATION_SIZE = 100
INFLUENCE_PROBABILITY = 0.2
MAX_STEPS = 50

# Define a class for individuals
class Individual:
    def __init__(self, adopts_new_behavior=False):
        self.adopts_new_behavior = adopts_new_behavior

    def influence(self, others):
        if self.adopts_new_behavior:
            for other in others:
                if not other.adopts_new_behavior and random.random() < INFLUENCE_PROBABILITY:
                    other.adopts_new_behavior = True

    def __repr__(self):
        return "Adopter" if self.adopts_new_behavior else "Non-adopter"

# Create a population
population = [Individual(random.choice([True, False])) for _ in range(POPULATION_SIZE)]

# Simulate the spread of a new behavior
for step in range(MAX_STEPS):
    print(f"Step {step}:")
    for individual in population:
        print(individual, end=' ')
    print()

    # Each individual tries to influence others
    for individual in population:
        others = [other for other in population if other is not individual]
        individual.influence(others)

# Final state of the population
print("\nFinal State:")
for individual in population:
    print(individual, end=' ')
print()
