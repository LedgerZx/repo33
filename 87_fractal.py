import time
import random
import math
import os
import sys
from datetime import datetime

class FractalTree:
    def __init__(self, width=80, height=40):
        self.width = width
        self.height = height
        self.frame = [[' ' for _ in range(width)] for _ in range(height)]
        self.wind_force = 0
        self.wind_phase = 0
        self.season = 0  # 0: spring, 1: summer, 2: autumn, 3: winter
        self.season_colors = {
            0: ['🌸', '🌺', '🌼'],  # Spring - flowers
            1: ['🍃', '🌿', '🍀'],  # Summer - green leaves
            2: ['🍂', '🍁', '🍄'],  # Autumn - falling leaves
            3: ['❄️', '🌨️', '⛄']   # Winter - snow
        }
        
    def clear_frame(self):
        self.frame = [[' ' for _ in range(self.width)] for _ in range(self.height)]
    
    def draw_branch(self, x, y, length, angle, depth, max_depth):
        if depth > max_depth or length < 1:
            # Draw leaves/snow/flowers at the end of branches
            if depth == max_depth and random.random() > 0.3:
                leaf = random.choice(self.season_colors[self.season])
                self.draw_char(x, y, leaf)
            return
        
        # Calculate wind effect
        wind_effect = math.sin(self.wind_phase + depth * 0.5) * self.wind_force * (depth / max_depth)
        adjusted_angle = angle + wind_effect
        
        # Calculate end point
        end_x = int(x + length * math.cos(adjusted_angle))
        end_y = int(y + length * math.sin(adjusted_angle))
        
        # Draw branch
        self.draw_line(x, y, end_x, end_y, '█' if depth < 3 else '▓')
        
        # Create sub-branches
        if length > 2:
            # Recursive branching with some randomness
            branch_angle = math.pi / 6 + random.uniform(-0.2, 0.2)
            length_reduction = 0.7 + random.uniform(-0.1, 0.1)
            
            # Left branch
            self.draw_branch(
                end_x, end_y,
                length * length_reduction,
                adjusted_angle - branch_angle,
                depth + 1,
                max_depth
            )
            
            # Right branch
            self.draw_branch(
                end_x, end_y,
                length * length_reduction,
                adjusted_angle + branch_angle,
                depth + 1,
                max_depth
            )
            
            # Occasional middle branch
            if random.random() > 0.7:
                self.draw_branch(
                    end_x, end_y,
                    length * length_reduction * 0.8,
                    adjusted_angle + random.uniform(-0.3, 0.3),
                    depth + 1,
                    max_depth
                )
    
    def draw_line(self, x1, y1, x2, y2, char):
        """Draw a line using Bresenham's algorithm"""
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy
        
        while True:
            if 0 <= x1 < self.width and 0 <= y1 < self.height:
                self.frame[y1][x1] = char
            
            if x1 == x2 and y1 == y2:
                break
                
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy
    
    def draw_char(self, x, y, char):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.frame[y][x] = char
    
    def update_wind(self):
        self.wind_phase += 0.1
        self.wind_force = math.sin(self.wind_phase * 0.3) * 0.3 + \
                         math.sin(self.wind_phase * 0.7) * 0.2
    
    def change_season(self):
        self.season = (self.season + 1) % 4
    
    def render(self):
        # Clear screen
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Draw ground
        ground_chars = ['▒', '░', '▓']
        for x in range(self.width):
            ground_char = random.choice(ground_chars)
            self.frame[self.height - 1][x] = ground_char
            if random.random() > 0.8:
                self.frame[self.height - 2][x] = ground_char
        
        # Draw sun/moon
        celestial_body = '☀️' if self.season in [0, 1] else '🌙'
        self.draw_char(self.width - 10, 3, celestial_body)
        
        # Draw clouds
        for i in range(3):
            cloud_x = 10 + i * 25 + int(math.sin(self.wind_phase + i) * 5)
            cloud_y = 5 + i * 3
            for dx in range(-2, 3):
                for dy in range(-1, 2):
                    if random.random() > 0.3:
                        self.draw_char(cloud_x + dx, cloud_y + dy, '☁')
        
        # Print frame
        for row in self.frame:
            print(''.join(row))
        
        # Print info
        season_names = ['Spring', 'Summer', 'Autumn', 'Winter']
        print(f"\nSeason: {season_names[self.season]} | Wind: {abs(self.wind_force):.2f}")
        print("Press SPACE to change season, ESC to exit")
    
    def animate(self):
        try:
            while True:
                self.clear_frame()
                
                # Draw main tree
                self.draw_branch(
                    self.width // 2,
                    self.height - 3,
                    self.height // 3,
                    -math.pi / 2,
                    0,
                    8
                )
                
                self.update_wind()
                self.render()
                time.sleep(0.1)
                
                # Check for keypress
                if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                    key = sys.stdin.read(1)
                    if key == ' ':
                        self.change_season()
                    elif key == '\x1b':  # ESC key
                        break
                        
        except KeyboardInterrupt:
            pass

# Main execution
if __name__ == "__main__":
    import select
    
    print("🌳 Fractal Tree Animation 🌳")
    print("Controls: SPACE = Change Season | ESC = Exit")
    print("Starting animation...")
    time.sleep(2)
    
    tree = FractalTree()
    tree.animate()
    
    print("\nThanks for watching! 🌲")
