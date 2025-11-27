#!/usr/bin/env python3
import random
import numpy as np
import curses
from collections import defaultdict
import math
import time

class Creature:
    def __init__(self, x, y, dna=None):
        self.x = x
        self.y = y
        self.age = 0
        self.energy = 50
        self.generation = 0
        
        if dna is None:
            # Random DNA traits (0-255 values)
            self.dna = {
                'speed': random.randint(1, 10),
                'vision': random.randint(2, 8),
                'efficiency': random.randint(1, 10),
                'reproduction_threshold': random.randint(70, 120),
                'metabolism': random.randint(1, 5),
                'aggression': random.randint(0, 10),
                'cooperation': random.randint(0, 10),
                'color_r': random.randint(50, 255),
                'color_g': random.randint(50, 255),
                'color_b': random.randint(50, 255)
            }
        else:
            self.dna = self.mutate_dna(dna)
            self.generation = dna.get('generation', 0) + 1
    
    def mutate_dna(self, parent_dna):
        mutated = parent_dna.copy()
        for key in mutated:
            if key != 'generation':
                if random.random() < 0.1:  # 10% mutation chance
                    mutation = random.randint(-5, 5)
                    mutated[key] = max(0, min(255, mutated[key] + mutation))
        return mutated
    
    def move(self, world_width, world_height, creatures, food):
        # Calculate movement based on DNA traits
        speed = self.dna['speed']
        vision = self.dna['vision']
        
        # Find nearest food or creature
        nearest_target = None
        min_distance = float('inf')
        
        # Look for food
        for f in food:
            dist = abs(self.x - f[0]) + abs(self.y - f[1])
            if dist < vision and dist < min_distance:
                min_distance = dist
                nearest_target = f
        
        # Look for creatures (aggression/cooperation behavior)
        for other in creatures:
            if other != self:
                dist = abs(self.x - other.x) + abs(self.y - other.y)
                if dist < vision and dist < min_distance:
                    min_distance = dist
                    nearest_target = other
        
        # Move towards target or randomly
        if nearest_target:
            dx = np.sign(nearest_target[0] - self.x) if hasattr(nearest_target, '__len__') else np.sign(nearest_target.x - self.x)
            dy = np.sign(nearest_target[1] - self.y) if hasattr(nearest_target, '__len__') else np.sign(nearest_target.y - self.y)
        else:
            dx = random.randint(-1, 1)
            dy = random.randint(-1, 1)
        
        # Apply speed
        self.x = max(0, min(world_width - 1, self.x + dx * speed))
        self.y = max(0, min(world_height - 1, self.y + dy * speed))
    
    def update(self):
        self.age += 1
        self.energy -= self.dna['metabolism']
        
        # Energy efficiency bonus
        if self.dna['efficiency'] > 5:
            self.energy += 1
        
        return self.energy > 0
    
    def can_reproduce(self):
        return self.energy > self.dna['reproduction_threshold']

class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.creatures = []
        self.food = []
        self.generation = 0
        self.stats = defaultdict(int)
        self.time_step = 0
        
        # Initialize creatures
        for _ in range(20):
            x = random.randint(0, width - 1)
            y = random.randint(0, height - 1)
            self.creatures.append(Creature(x, y))
        
        # Initialize food
        self.spawn_food(50)
    
    def spawn_food(self, count):
        for _ in range(count):
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            self.food.append((x, y))
    
    def update(self):
        self.time_step += 1
        
        # Spawn food periodically
        if self.time_step % 10 == 0:
            self.spawn_food(5)
        
        # Update creatures
        new_creatures = []
        dead_creatures = []
        
        for creature in self.creatures:
            creature.move(self.width, self.height, self.creatures, self.food)
            
            # Eat food
            for i, (fx, fy) in enumerate(self.food):
                if creature.x == fx and creature.y == fy:
                    creature.energy += 20
                    self.food.pop(i)
                    break
            
            # Update creature
            if not creature.update():
                dead_creatures.append(creature)
            
            # Reproduction
            elif creature.can_reproduce() and len(self.creatures) < 100:
                creature.energy /= 2
                offspring = Creature(creature.x, creature.y, creature.dna)
                new_creatures.append(offspring)
        
        # Remove dead creatures
        for dead in dead_creatures:
            self.creatures.remove(dead)
            # Dead creature becomes food
            self.food.append((dead.x, dead.y))
        
        # Add new creatures
        self.creatures.extend(new_creatures)
        
        # Update statistics
        self.update_stats()
    
    def update_stats(self):
        self.stats = defaultdict(int)
        for creature in self.creatures:
            self.stats['total'] += 1
            self.stats['avg_speed'] += creature.dna['speed']
            self.stats['avg_vision'] += creature.dna['vision']
            self.stats['avg_efficiency'] += creature.dna['efficiency']
            self.stats['avg_generation'] += creature.generation
        
        if self.stats['total'] > 0:
            for key in ['avg_speed', 'avg_vision', 'avg_efficiency', 'avg_generation']:
                self.stats[key] /= self.stats['total']

class Simulation:
    def __init__(self):
        self.screen = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.screen.keypad(True)
        curses.curs_set(0)
        curses.start_color()
        
        # Initialize colors
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_CYAN, curses.COLOR_BLACK)
        
        self.height, self.width = self.screen.getmaxyx()
        self.world = World(self.width
