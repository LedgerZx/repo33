import numpy as np
import random
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from dataclasses import dataclass
from typing import List, Tuple

# Neural Network for AI agent
class NeuralNetwork:
    def __init__(self, input_size=8, hidden_size=16, output_size=4):
        self.weights1 = np.random.randn(input_size, hidden_size) * 0.5
        self.weights2 = np.random.randn(hidden_size, output_size) * 0.5
        self.bias1 = np.random.randn(hidden_size) * 0.5
        self.bias2 = np.random.randn(output_size) * 0.5
    
    def forward(self, x):
        self.z1 = np.dot(x, self.weights1) + self.bias1
        self.a1 = np.tanh(self.z1)
        self.z2 = np.dot(self.a1, self.weights2) + self.bias2
        return np.tanh(self.z2)
    
    def mutate(self, rate=0.1):
        if random.random() < rate:
            self.weights1 += np.random.randn(*self.weights1.shape) * 0.2
            self.weights2 += np.random.randn(*self.weights2.shape) * 0.2
            self.bias1 += np.random.randn(*self.bias1.shape) * 0.2
            self.bias2 += np.random.randn(*self.bias2.shape) * 0.2
    
    def crossover(self, other):
        child = NeuralNetwork()
        mask1 = np.random.random(self.weights1.shape) > 0.5
        mask2 = np.random.random(self.weights2.shape) > 0.5
        
        child.weights1 = np.where(mask1, self.weights1, other.weights1)
        child.weights2 = np.where(mask2, self.weights2, other.weights2)
        child.bias1 = np.where(random.random() > 0.5, self.bias1, other.bias1)
        child.bias2 = np.where(random.random() > 0.5, self.bias2, other.bias2)
        
        return child

@dataclass
class Agent:
    position: np.ndarray
    brain: NeuralNetwork
    energy: int = 100
    score: int = 0
    alive: bool = True
    
    def get_inputs(self, food_pos, world_size):
        # Distance and angle to nearest food
        to_food = food_pos - self.position
        distance = np.linalg.norm(to_food)
        angle = np.arctan2(to_food[1], to_food[0])
        
        # Position and velocity
        inputs = [
            self.position[0] / world_size[0],
            self.position[1] / world_size[1],
            distance / (world_size[0] * 1.5),
            np.cos(angle),
            np.sin(angle),
            self.energy / 100,
            self.score / 10,
            random.random()  # Random exploration factor
        ]
        
        return np.array(inputs)
    
    def move(self, action, world_size):
        speed = 2.0
        dx = action[0] * speed
        dy = action[1] * speed
        
        self.position[0] = np.clip(self.position[0] + dx, 0, world_size[0])
        self.position[1] = np.clip(self.position[1] + dy, 0, world_size[1])
        
        self.energy -= 1
        if self.energy <= 0:
            self.alive = False

class Simulation:
    def __init__(self, population_size=50, world_size=(100, 100), num_food=10):
        self.population_size = population_size
        self.world_size = world_size
        self.num_food = num_food
        self.generation = 0
        self.best_score = 0
        self.agents = []
        self.food_positions = []
        self.history = []
        
    def initialize_population(self):
        self.agents = []
        for _ in range(self.population_size):
            pos = np.array([
                random.uniform(10, self.world_size[0] - 10),
                random.uniform(10, self.world_size[1] - 10)
            ])
            brain = NeuralNetwork()
            self.agents.append(Agent(pos, brain))
    
    def place_food(self):
        self.food_positions = []
        for _ in range(self.num_food):
            pos = np.array([
                random.uniform(5, self.world_size[0] - 5),
                random.uniform(5, self.world_size[1] - 5)
            ])
            self.food_positions.append(pos)
    
    def find_nearest_food(self, agent):
        if not self.food_positions:
            return np.array([50, 50])
        
        distances = [np.linalg.norm(food - agent.position) for food in self.food_positions]
        nearest_idx = np.argmin(distances)
        return self.food_positions[nearest_idx]
    
    def check_food_collision(self, agent):
        for i, food in enumerate(self.food_positions):
            if np.linalg.norm(agent.position - food) < 3:
                self.food_positions[i] = np.array([
                    random.uniform(5, self.world_size[0] - 5),
                    random.uniform(5, self.world_size[1] - 5)
                ])
                agent.score += 1
                agent.energy = min(100, agent.energy + 20)
                return True
        return False
    
    def evolve_population(self):
        # Sort agents by fitness (score + energy)
        sorted_agents = sorted(self.agents, key=lambda a: a.score + a.energy/10, reverse=True)
        
        # Keep top performers
        elite_size = self.population_size // 5
        new_agents = [Agent(
            np.array([random.uniform(10, self.world_size[0] - 10),
                     random.uniform(10, self.world_size[1] - 10)]),
            sorted_agents[i].brain,
            100, 0, True
        ) for i in range(elite_size)]
        
        # Create offspring through crossover and mutation
        while len(new_agents) < self.population_size:
            parent1 = random.choice(sorted_agents[:self.population_size//2])
            parent2 = random.choice(sorted_agents[:self.population_size//2])
            
            child_brain = parent1.brain.crossover(parent2.brain)
            child_brain.mutate(0.1)
            
            new_agents.append(Agent(
                np.array([random.uniform(10, self.world_size[0] - 10),
                         random.uniform(10, self.world_size[1] - 10)]),
                child_brain,
                100, 0, True
            ))
        
        self.agents = new_agents
        self.generation += 1
    
    def run_generation(self, max_steps=500):
        self.place_food()
        
        for step in range(max_steps):
            alive_agents = [a for a in self.agents if a.alive]
            if not alive_agents:
                break
            
            for agent in alive_agents:
                nearest_food = self.find_nearest_food(agent)
                inputs = agent.get_inputs(nearest_food, self.world_size)
                actions = agent.brain.forward(inputs)
                agent.move(actions[:2], self.world_size)
                self.check_food_collision(agent)
        
        # Record statistics
        avg_score = np.mean([a.score for a in self.agents])
        max_score = max([a.score for a in self.agents])
        self.history.append({
            'generation': self.generation,
            'avg_score': avg_score,
            'max_score': max_score
        })
        
        if max_score > self.best_score:
            self.best_score = max_score
        
        print(f"Generation {self.generation}: Avg Score: {avg_score:.2f}, Best Score: {max_score}")
    
    def run_simulation(self, generations=100):
        self.initialize_population()
        
        for gen in range(generations):
            self.run_generation()
            self.evolve_population()
        
        return self.history

# Visualization
def plot_evolution(history):
    generations = [h['generation'] for h in history]
    avg_scores = [h['avg_score'] for h in history]
    max_scores = [h['max_score'] for h in history]
    
    plt.figure(figsize=(12, 6))
    plt.plot(generations, avg_scores, 'b-', label='Average Score', alpha=0.7)
    plt.plot(generations, max_scores, 'r-', label='Best Score', linewidth=2)
    plt.xlabel('Generation')
    plt.ylabel('Score')
    plt.title('AI Agent Evolution Over Time')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()

# Run the simulation
if __name__ == "__main__":
    print("🧬 Starting AI Evolution Simulation...")
    print("Watch as neural network agents learn to find food!\n")
    
    sim = Simulation(population_size=30, world_size=(100, 100), num_food=8)
    history = sim.run_simulation(generations=50)
    
    print(f"\n🎯 Best score achieved: {sim.best_score}")
    print(f"📊 Final generation: {sim.generation}")
    
    plot_evolution(history)
