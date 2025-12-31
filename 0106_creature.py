import random
import math
import os
import time

class Creature:
    def __init__(self, x, y, dna=None):
        self.x = x
        self.y = y
        self.energy = 100
        self.age = 0
        self.generation = 0
        
        # DNA determines creature traits
        if dna is None:
            # Random DNA for first generation
            self.dna = {
                'speed': random.uniform(0.5, 2.0),
                'size': random.uniform(3, 8),
                'vision_range': random.uniform(20, 60),
                'metabolism': random.uniform(0.5, 2.0),
                'reproduction_threshold': random.uniform(150, 250),
                'color_r': random.randint(50, 255),
                'color_g': random.randint(50, 255),
                'color_b': random.randint(50, 255)
            }
        else:
            # Inherit DNA with mutations
            self.dna = {}
            for trait, value in dna.items():
                if isinstance(value, (int, float)):
                    mutation = random.gauss(0, 0.1)
                    if isinstance(value, int):
                        new_value = max(0, min(255, int(value + value * mutation)))
                    else:
                        new_value = max(0.1, value + value * mutation)
                    self.dna[trait] = new_value
                else:
                    self.dna[trait] = value
        
        self.direction = random.uniform(0, 2 * math.pi)
        self.alive = True
    
    def move(self, width, height):
        if not self.alive:
            return
        
        # Random walk with momentum
        self.direction += random.gauss(0, 0.3)
        
        # Move based on speed from DNA
        dx = math.cos(self.direction) * self.dna['speed']
        dy = math.sin(self.direction) * self.dna['speed']
        
        self.x = (self.x + dx) % width
        self.y = (self.y + dy) % height
        
        # Bounce off walls (alternative to wrapping)
        if self.x < 0 or self.x > width:
            self.direction = math.pi - self.direction
        if self.y < 0 or self.y > height:
            self.direction = -self.direction
    
    def update(self):
        if not self.alive:
            return
        
        # Age and consume energy based on metabolism
        self.age += 1
        self.energy -= self.dna['metabolism']
        
        # Die if no energy or too old
        if self.energy <= 0 or self.age > 1000:
            self.alive = False
    
    def can_reproduce(self):
        return self.alive and self.energy > self.dna['reproduction_threshold']
    
    def reproduce(self):
        if self.can_reproduce():
            # Create offspring with mutated DNA
            offspring = Creature(
                self.x + random.uniform(-10, 10),
                self.y + random.uniform(-10, 10),
                self.dna
            )
            offspring.generation = self.generation + 1
            self.energy /= 2  # Reproduction costs energy
            return offspring
        return None
    
    def eat_food(self, food_amount):
        self.energy = min(self.energy + food_amount, 300)

class Food:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.energy = random.uniform(20, 40)

class Ecosystem:
    def __init__(self, width=100, height=40):
        self.width = width
        self.height = height
        self.creatures = []
        self.food = []
        self.generation = 0
        self.time_step = 0
        
        # Initialize with random creatures
        for _ in range(20):
            self.creatures.append(
                Creature(
                    random.uniform(0, width),
                    random.uniform(0, height)
                )
            )
        
        # Initialize with food
        for _ in range(50):
            self.food.append(
                Food(
                    random.uniform(0, width),
                    random.uniform(0, height)
                )
            )
    
    def update(self):
        self.time_step += 1
        
        # Move and update creatures
        new_creatures = []
        for creature in self.creatures:
            creature.move(self.width, self.height)
            creature.update()
            
            # Check for food
            for food in self.food[:]:
                distance = math.sqrt((creature.x - food.x)**2 + (creature.y - food.y)**2)
                if distance < creature.dna['vision_range']:
                    # Move towards food
                    angle_to_food = math.atan2(food.y - creature.y, food.x - creature.x)
                    creature.direction = angle_to_food
                    
                    # Eat if close enough
                    if distance < creature.dna['size']:
                        creature.eat_food(food.energy)
                        self.food.remove(food)
            
            # Reproduction
            if creature.can_reproduce():
                offspring = creature.reproduce()
                if offspring:
                    new_creatures.append(offspring)
        
        # Add new creatures from reproduction
        self.creatures.extend(new_creatures)
        
        # Remove dead creatures
        self.creatures = [c for c in self.creatures if c.alive]
        
        # Add new food periodically
        if random.random() < 0.3:
            self.food.append(
                Food(
                    random.uniform(0, self.width),
                    random.uniform(0, self.height)
                )
            )
        
        # Track generations
        if self.creatures:
            self.generation = max(c.generation for c in self.creatures)
    
    def get_stats(self):
        if not self.creatures:
            return {
                'population': 0,
                'avg_energy': 0,
                'avg_speed': 0,
                'avg_size': 0,
                'avg_vision': 0,
                'generation': 0
            }
        
        return {
            'population': len(self.creatures),
            'avg_energy': sum(c.energy for c in self.creatures) / len(self.creatures),
            'avg_speed': sum(c.dna['speed'] for c in self.creatures) / len(self.creatures),
            'avg_size': sum(c.dna['size'] for c in self.creatures) / len(self.creatures),
            'avg_vision': sum(c.dna['vision_range'] for c in self.creatures) / len(self.creatures),
            'generation': self.generation
        }
    
    def render(self):
        os.system('clear' if os.name == 'posix' else 'cls')
        
        # Create grid
        grid = [['.' for _ in range(self.width)] for _ in range(self.height)]
        
        # Place food
        for food in self.food:
            x, y = int(food.x), int(food.y)
            if 0 <= x < self.width and 0 <= y < self.height:
                grid[y][x] = '+'
        
        # Place creatures
        for creature in self.creatures:
            x, y = int(creature.x), int(creature.y)
            if 0 <= x < self.width and 0 <= y < self.height:
                # Different symbols based on energy
                if creature.energy > 150:
                    grid[y][x] = '@'
                elif creature.energy > 100:
                    grid[y][x] = 'o'
                else:
                    grid[y][x] = '.'
        
        # Print grid
        for row in grid:
            print(''.join(row))
        
        # Print stats
        stats = self.get_stats()
        print(f"\nTime: {self.time_step} | Generation: {stats['generation']} | Population: {stats['population']}")
        print(f"Avg Energy: {stats['avg_energy']:.1f} | Avg Speed: {stats['avg_speed']:.2f}")
        print(f"Avg Size: {stats['avg_size']:.2f} | Avg Vision: {stats['avg_vision']:.1f}")
        print(f"Food available: {len(self.food)}")

def main():
    ecosystem = Ecosystem()
    
    try:
        while True:
            ecosystem.update()
            ecosystem.render()
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nSimulation ended. Final stats:")
        stats = ecosystem.get_stats()
        for key, value in stats.items():
            print(f"{key}: {value}")

if __name__ == "__main__":
    main()
