import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Button, Slider, RadioButtons
import random

class CellularAutomaton:
    def __init__(self, width=100, height=100, pattern='game_of_life'):
        self.width = width
        self.height = height
        self.grid = np.zeros((height, width), dtype=int)
        self.pattern = pattern
        self.generation = 0
        self.history = []
        self.max_history = 50
        
        # Pattern rules: (birth_min, birth_max, survive_min, survive_max)
        self.rules = {
            'game_of_life': (3, 3, 2, 3),
            'highlife': (3, 6, 2, 3),
            'seeds': (2, 2, 0, 0),
            'day_night': (3, 3, 3, 6),
            'maze': (3, 3, 1, 5),
            'coral': (3, 3, 4, 8),
            'amoeba': (3, 3, 5, 8),
            'coagulations': (3, 3, 2, 2)
        }
        
        # Initialize with random cells
        self.randomize()
    
    def randomize(self, density=0.3):
        """Randomly initialize the grid with a given density of live cells"""
        self.grid = np.random.choice([0, 1], size=(self.height, self.width), 
                                    p=[1-density, density])
        self.generation = 0
        self.history = []
    
    def add_pattern(self, pattern_name, x, y):
        """Add a specific pattern at the given position"""
        patterns = {
            'glider': np.array([[0, 1, 0], [0, 0, 1], [1, 1, 1]]),
            'blinker': np.array([[1, 1, 1]]),
            'toad': np.array([[0, 1, 1, 1], [1, 1, 1, 0]]),
            'beacon': np.array([[1, 1, 0, 0], [1, 1, 0, 0], 
                               [0, 0, 1, 1], [0, 0, 1, 1]]),
            'pulsar': np.array([
                [0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
                [0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0],
                [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0]
            ]),
            'spaceship': np.array([
                [0, 1, 0, 0, 1],
                [1, 0, 0, 0, 0],
                [1, 0, 0, 0, 1],
                [1, 1, 1, 1, 0]
            ]),
            'pentomino': np.array([
                [0, 1, 1],
                [1, 1, 0],
                [0, 1, 0]
            ])
        }
        
        if pattern_name in patterns:
            pattern = patterns[pattern_name]
            ph, pw = pattern.shape
            
            # Place pattern at the specified position
            for i in range(ph):
                for j in range(pw):
                    if 0 <= y+i < self.height and 0 <= x+j < self.width:
                        self.grid[y+i, x+j] = pattern[i, j]
    
    def count_neighbors(self, y, x):
        """Count the number of live neighbors for a cell"""
        count = 0
        # Check all 8 neighbors
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue  # Skip the cell itself
                
                ny, nx = (y + i) % self.height, (x + j) % self.width
                count += self.grid[ny, nx]
        
        return count
    
    def update(self):
        """Update the grid according to the rules of the cellular automaton"""
        new_grid = np.zeros_like(self.grid)
        birth_min, birth_max, survive_min, survive_max = self.rules[self.pattern]
        
        for y in range(self.height):
            for x in range(self.width):
                neighbors = self.count_neighbors(y, x)
                
                if self.grid[y, x] == 1:  # Cell is alive
                    if survive_min <= neighbors <= survive_max:
                        new_grid[y, x] = 1  # Cell survives
                else:  # Cell is dead
                    if birth_min <= neighbors <= birth_max:
                        new_grid[y, x] = 1  # Cell is born
        
        self.grid = new_grid
        self.generation += 1
        
        # Store history for density plot
        self.history.append(np.sum(self.grid))
        if len(self.history) > self.max_history:
            self.history.pop(0)
        
        return self.grid
    
    def get_density(self):
        """Calculate the density of live cells"""
        return np.sum(self.grid) / (self.width * self.height)
    
    def toggle_cell(self, y, x):
        """Toggle a cell between alive and dead"""
        if 0 <= y < self.height and 0 <= x < self.width:
            self.grid[y, x] = 1 - self.grid[y, x]
    
    def clear(self):
        """Clear the grid"""
        self.grid = np.zeros((self.height, self.width), dtype=int)
        self.generation = 0
        self.history = []

class CellularAutomatonGUI:
    def __init__(self, width=100, height=100):
        self.ca = CellularAutomaton(width, height)
        self.fig = plt.figure(figsize=(14, 8))
        self.fig.suptitle('Cellular Automaton Simulator', fontsize=16)
        
        # Create grid for main display
        self.ax_grid = plt.subplot2grid((3, 3), (0, 0), colspan=2, rowspan=3)
        self.im = self.ax_grid.imshow(self.ca.grid, cmap='binary', interpolation='nearest')
        self.ax_grid.set_title(f'Generation: {self.ca.generation}')
        
        # Create density plot
        self.ax_density = plt.subplot2grid((3, 3), (0, 2))
        self.density_line, = self.ax_density.plot([], [], 'r-')
        self.ax_density.set_xlim(0, self.ca.max_history)
        self.ax_density.set_ylim(0, 1)
        self.ax_density.set_title('Cell Density')
        self.ax_density.set_xlabel('Generation')
        self.ax_density.set_ylabel('Density')
        
        # Add controls
        self.add_controls()
        
        # Animation control
        self.animation = None
        self.is_running = False
        
        # Mouse interaction
        self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        self.dragging = False
        self.fig.canvas.mpl_connect('button_release_event', self.on_release)
        self.fig.canvas.mpl_connect('motion_notify_event', self.on_motion)
        
        plt.tight_layout()
    
    def add_controls(self):
        """Add UI controls to the figure"""
        # Play/Pause button
        ax_button = plt.axes([0.7, 0.25, 0.1, 0.04])
        self.btn_play = Button(ax_button, 'Play')
        self.btn_play.on_clicked(self.toggle_animation)
        
        # Step button
        ax_step = plt.axes([0.7, 0.2, 0.1, 0.04])
        self.btn_step = Button(ax_step, 'Step')
        self.btn_step.on_clicked(self.step_simulation)
        
        # Clear button
        ax_clear = plt.axes([0.7, 0.15, 0.1, 0.04])
        self.btn_clear = Button(ax_clear, 'Clear')
        self.btn_clear.on_clicked(self.clear_grid)
        
        # Randomize button
        ax_random = plt.axes([0.7, 0.1, 0.1, 0.04])
        self.btn_random = Button(ax_random, 'Randomize')
        self.btn_random.on_clicked(self.randomize_grid)
        
        # Speed slider
        ax_speed = plt.axes([0.7, 0.05, 0.2, 0.03])
        self.speed_slider = Slider(ax_speed, 'Speed', 1, 60, valinit=10, valstep=1)
        
        # Pattern selector
        ax_pattern = plt.axes([0.85, 0.05, 0.12, 0.2])
        self.pattern_selector = RadioButtons(ax_pattern, list(self.ca.rules.keys()))
        self.pattern_selector.on_clicked(self.change_pattern)
        
        # Pattern buttons
        ax_glider = plt.axes([0.7, 0.35, 0.05, 0.04])
        self.btn_glider = Button(ax_glider, 'Glider')
        self.btn_glider.on_clicked(lambda x: self.add_pattern('glider'))
        
        ax_pulsar = plt.axes([0.75, 0.35, 0.05, 0.04])
        self.btn_pulsar = Button(ax_pulsar, 'Pulsar')
        self.btn_pulsar.on_clicked(lambda x: self.add_pattern('pulsar'))
        
        ax_spaceship = plt.axes([0.7, 0.3, 0.05, 0.04])
        self.btn_spaceship = Button(ax_spaceship, 'Ship')
        self.btn_spaceship.on_clicked(lambda x: self.add_pattern('spaceship'))
        
        ax_pento = plt.axes([0.75, 0.3, 0.05, 0.04])
        self.btn_pento = Button(ax_pento, 'Pento')
        self.btn_pento.on_clicked(lambda x: self.add_pattern('pentomino'))
    
    def update_plot(self, frame=None):
        """Update the plot for animation"""
        if self.is_running:
            self.ca.update()
            self.im.set_data(self.ca.grid)
            self.ax_grid.set_title(f'Generation: {self.ca.generation}')
            
            # Update density plot
            if self.ca.history:
                self.density_line.set_data(range(len(self.ca.history)), 
                                         [h / (self.ca.width * self.ca.height) for h in self.ca.history])
        
        return [self.im, self.density_line]
    
    def toggle_animation(self, event=None):
        """Toggle between play and pause"""
        self.is_running = not self.is_running
        
        if self.is_running:
            self.btn_play.label.set_text('Pause')
            if self.animation is None:
                self.animation = animation.FuncAnimation(
                    self.fig, self.update_plot, 
                    interval=1000//int(self.speed_slider.val),
                    blit=True
                )
            else:
                self.animation.resume()
        else:
            self.btn_play.label.set_text('Play')
            if self.animation:
                self.animation.pause()
        
        plt.draw()
    
    def step_simulation(self, event=None):
        """Step the simulation forward by one generation"""
        self.ca.update()
        self.im.set_data(self.ca.grid)
        self.ax_grid.set_title(f'Generation: {self.ca.generation}')
        
        # Update density plot
        if self.ca.history:
            self.density_line.set_data(range(len(self.ca.history)), 
                                     [h / (self.ca.width * self.ca.height) for h in self.ca.history])
        
        plt.draw()
    
    def clear_grid(self, event=None):
        """Clear the grid"""
        self.ca.clear()
        self.im.set_data(self.ca.grid)
        self.ax_grid.set_title(f'Generation: {self.ca.generation}')
        self.density_line.set_data([], [])
        plt.draw()
    
    def randomize_grid(self, event=None):
        """Randomize the grid"""
        self.ca.randomize()
        self.im.set_data(self.ca.grid)
        self.ax_grid.set_title(f'Generation: {self.ca.generation}')
        self.density_line.set_data([], [])
        plt.draw()
    
    def change_pattern(self, label):
        """Change the cellular automaton pattern"""
        self.ca.pattern = label
        self.ax_grid.set_title(f'Generation: {self.ca.generation} - {label.replace("_", " ").title()}')
        plt.draw()
    
    def add_pattern(self, pattern_name):
        """Add a pattern at a random position"""
        x = random.randint(10, self.ca.width - 20)
        y = random.randint(10, self.ca.height - 20)
        self.ca.add_pattern(pattern_name, x, y)
        self.im.set_data(self.ca.grid)
        plt.draw()
    
    def on_click(self, event):
        """Handle mouse click events"""
        if event.inaxes == self.ax_grid:
            self.dragging = True
            x, y = int(event.xdata), int(event.ydata)
            self.ca.toggle_cell(y, x)
            self.im.set_data(self.ca.grid)
            plt.draw()
    
    def on_release(self, event):
        """Handle mouse release events"""
        self.dragging = False
    
    def on_motion(self, event):
        """Handle mouse motion events"""
        if self.dragging and event.inaxes == self.ax_grid:
            x, y = int(event.xdata), int(event.ydata)
            self.ca.toggle_cell(y, x)
            self.im.set_data(self.ca.grid)
            plt.draw()
    
    def show(self):
        """Display the GUI"""
        plt.show()

if __name__ == "__main__":
    # Create and run the cellular automaton GUI
    gui = CellularAutomatonGUI(width=100, height=100)
    gui.show()
