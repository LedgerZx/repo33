import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from dataclasses import dataclass
from typing import List, Tuple
import colorsys

@dataclass
class Creature:
    x: float
    y: float
    energy: float
    speed: float
    size: float
    vision_range: float
    color: Tuple[float, float, float]
    generation: int = 0
    age: int = 0
    food_eaten: int = 0
    
    def move(self, width: int, height: int, food_positions: List[Tuple[float, float]]):
        """Move creature towards nearest food or randomly wander"""
        if food_positions:
            # Find nearest food
            distances = [np.sqrt((self.x - fx)**2 + (self.y - fy)**2) 
                        for fx, fy in food_positions]
            min_idx = np.argmin(distances)
            target_x, target_y = food_positions[min_idx]
            
            # Move towards food if within vision range
            if distances[min_idx] < self.vision_range:
                dx = target_x - self.x
                dy = target_y - self.y
                norm = np.sqrt(dx**2 + dy**2)
                if norm > 0:
                    self.x += (dx / norm) * self.speed
                    self.y += (dy / norm) * self.speed
            else:
                # Random walk
                angle = random.uniform(0, 2 * np.pi)
                self.x += np.cos(angle) * self.speed
                self.y += np.sin(angle) * self.speed
        else:
            # Random walk
            angle = random.uniform(0, 2 * np.pi)
            self.x += np.cos(angle) * self.speed
            self.y += np.sin(angle) * self.speed
        
        # Keep within bounds
        self.x = max(self.size, min(width - self.size, self.x))
        self.y = max(self.size, min(height - self.size, self.y))
        
        # Energy cost for movement
        self.energy -= 0.01 * self.speed
        
    def reproduce(self) -> 'Creature':
        """Create offspring with mutated traits"""
        mutation_rate = 0.2
        child = Creature(
            x=self.x + random.uniform(-10, 10),
            y=self.y + random.uniform(-10, 10),
            energy=50,
            speed=max(0.1, self.speed + random.uniform(-mutation_rate, mutation_rate)),
            size=max(1, self.size + random.uniform(-mutation_rate, mutation_rate)),
            vision_range=max(5, self.vision_range + random.uniform(-mutation_rate*5, mutation_rate*5)),
            color=self.mutate_color(self.color),
            generation=self.generation + 1
        )
        self.energy -= 30  # Reproduction cost
        return child
    
    def mutate_color(self, parent_color: Tuple[float, float, float]) -> Tuple[float, float, float]:
        """Slightly mutate the creature's color"""
        h, s, v = colorsys.rgb_to_hsv(*parent_color)
        h = (h + random.uniform(-0.05, 0.05)) % 1.0
        s = max(0, min(1, s + random.uniform(-0.1, 0.1)))
        v = max(0.3, min(1, v + random.uniform(-0.1, 0.1)))
        return colorsys.hsv_to_rgb(h, s, v)

class Ecosystem:
    def __init__(self, width: int = 800, height: int = 600, initial_creatures: int = 20):
        self.width = width
        self.height = height
        self.creatures: List[Creature] = []
        self.food_positions: List[Tuple[float, float]] = []
        self.max_food = 50
        self.generation = 0
        
        # Initialize creatures with random traits
        for _ in range(initial_creatures):
            self.creatures.append(Creature(
                x=random.uniform(0, width),
                y=random.uniform(0, height),
                energy=random.uniform(40, 80),
                speed=random.uniform(0.5, 2.0),
                size=random.uniform(2, 5),
                vision_range=random.uniform(20, 60),
                color=(random.random(), random.random(), random.random())
            ))
        
        # Initialize food
        self.spawn_food()
    
    def spawn_food(self):
        """Spawn food at random locations"""
        while len(self.food_positions) < self.max_food:
            self.food_positions.append((
                random.uniform(10, self.width - 10),
                random.uniform(10, self.height - 10)
            ))
    
    def update(self):
        """Update ecosystem state"""
        # Move creatures
        for creature in self.creatures:
            creature.move(self.width, self.height, self.food_positions)
            creature.age += 1
            
            # Check for food consumption
            for food_pos in self.food_positions[:]:
                distance = np.sqrt((creature.x - food_pos[0])**2 + 
                                 (creature.y - food_pos[1])**2)
                if distance < creature.size + 3:
                    creature.energy += 20
                    creature.food_eaten += 1
                    self.food_positions.remove(food_pos)
            
            # Reproduction
            if creature.energy > 70 and len(self.creatures) < 100:
                self.creatures.append(creature.reproduce())
        
        # Remove dead creatures
        self.creatures = [c for c in self.creatures if c.energy > 0 and c.age < 1000]
        
        # Spawn new food
        self.spawn_food()
        
        # Track generation
        if self.creatures:
            self.generation = max(c.generation for c in self.creatures)
    
    def get_stats(self) -> dict:
        """Get ecosystem statistics"""
        if not self.creatures:
            return {}
        
        return {
            'population': len(self.creatures),
            'avg_speed': np.mean([c.speed for c in self.creatures]),
            'avg_size': np.mean([c.size for c in self.creatures]),
            'avg_vision': np.mean([c.vision_range for c in self.creatures]),
            'generation': self.generation,
            'avg_energy': np.mean([c.energy for c in self.creatures])
        }

def animate_ecosystem():
    """Run the ecosystem simulation with visualization"""
    ecosystem = Ecosystem()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Main visualization
    ax1.set_xlim(0, ecosystem.width)
    ax1.set_ylim(0, ecosystem.height)
    ax1.set_aspect('equal')
    ax1.set_title('Digital Ecosystem Simulation')
    ax1.set_facecolor('#0a0a0a')
    
    # Statistics plot
    ax2.set_xlim(0, 100)
    ax2.set_ylim(0, 5)
    ax2.set_title('Population Statistics')
    ax2.set_xlabel('Time')
    ax2.set_ylabel('Value')
    
    # Data storage for plotting
    time_data = []
    pop_data = []
    speed_data = []
    size_data = []
    vision_data = []
    
    def update(frame):
        ecosystem.update()
        stats = ecosystem.get_stats()
        
        # Clear axes
        ax1.clear()
        ax2.clear()
        
        # Redraw ecosystem
        ax1.set_xlim(0, ecosystem.width)
        ax1.set_ylim(0, ecosystem.height)
        ax1.set_aspect('equal')
        ax1.set_facecolor('#0a0a0a')
        
        # Draw food
        if ecosystem.food_positions:
            food_x = [f[0] for f in ecosystem.food_positions]
            food_y = [f[1] for f in ecosystem.food_positions]
            ax1.scatter(food_x, food_y, c='green', s=20, alpha=0.6, marker='*')
        
        # Draw creatures
        for creature in ecosystem.creatures:
            circle = plt.Circle((creature.x, creature.y), creature.size, 
                              color=creature.color, alpha=0.7)
            ax1.add_patch(circle)
            
            # Draw vision range for high-energy creatures
            if creature.energy > 50:
                vision_circle = plt.Circle((creature.x, creature.y), 
                                         creature.vision_range, 
                                         fill=False, edgecolor=creature.color, 
                                         alpha=0.2, linewidth=0.5)
                ax1.add_patch(vision_circle)
        
        # Update statistics
        if stats:
            time_data.append(frame)
            pop_data.append(stats['population'])
            speed_data.append(stats['avg_speed'])
            size_data.append(stats['avg_size'])
            vision_data.append(stats['avg_vision'] / 20)  # Normalize for display
            
            # Keep only last 100 points
            if len(time_data) > 100:
                time_data.pop(0)
                pop_data.pop(0)
                speed_data.pop(0)
                size_data.pop(0)
                vision_data.pop(0)
            
            # Plot statistics
            ax2.plot(time_data, pop_data, 'b-', label='Population')
            ax2.plot(time_data, speed_data, 'r-', label='Avg Speed')
            ax2.plot(time_data, size_data, 'g-', label='Avg Size')
            ax2.plot(time_data, vision_data, 'y-', label='Avg Vision/20')
            ax2.legend(loc='upper right')
            ax2.set_title(f'Generation: {stats["generation"]}')
            ax2.grid(True, alpha=0.3)
        
        # Add info text
        info_text = f"Creatures: {len(ecosystem.creatures)}\n"
        info_text += f"Food: {len(ecosystem.food_positions)}\n"
        if stats:
            info_text += f"Avg Energy: {stats['avg_energy']:.1f}"
        ax1.text(10, ecosystem.height - 30, info_text, color='white', 
                fontsize=10, verticalalignment='top')
        
        return ax1, ax2
    
    anim = animation.FuncAnimation(fig, update, interval=50, blit=False)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    print("Starting Digital Ecosystem Simulation...")
    print("Watch as creatures evolve over time!")
    print("\nFeatures:")
    print("- Creatures with genetic traits (speed, size, vision)")
    print("- Natural selection and reproduction")
    print("- Real-time evolution visualization")
    print("- Population dynamics tracking")
    print("\nClose the window to exit.")
    
    animate_ecosystem()
