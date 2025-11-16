import time
import math
import os
import sys

class DNAHelix:
    def __init__(self, width=80, height=24, speed=0.1):
        self.width = width
        self.height = height
        self.speed = speed
        self.time = 0
        self.pairs = ['A-T', 'T-A', 'G-C', 'C-G']
        
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def calculate_position(self, y, t):
        """Calculate 3D position and project to 2D"""
        # Helix parameters
        radius = 8
        vertical_spacing = 0.5
        
        # Calculate angles for two strands
        angle1 = (y * vertical_spacing + t) % (2 * math.pi)
        angle2 = (y * vertical_spacing + t + math.pi) % (2 * math.pi)
        
        # 3D coordinates
        x1 = radius * math.cos(angle1)
        z1 = radius * math.sin(angle1)
        x2 = radius * math.cos(angle2)
        z2 = radius * math.sin(angle2)
        
        # Simple perspective projection
        perspective = 20
        proj_x1 = int(self.width/2 + x1 * perspective / (perspective + z1))
        proj_x2 = int(self.width/2 + x2 * perspective / (perspective + z2))
        
        return proj_x1, proj_x2, z1, z2
    
    def get_depth_char(self, z):
        """Get character based on depth"""
        depth_chars = ['░', '▒', '▓', '█']
        depth_index = int((z + 10) / 5) % len(depth_chars)
        return depth_chars[depth_index]
    
    def render(self):
        self.clear_screen()
        
        # Create buffer for the frame
        buffer = [[' ' for _ in range(self.width)] for _ in range(self.height)]
        depth_buffer = [[float('-inf') for _ in range(self.width)] for _ in range(self.height)]
        
        # Render helix
        for y in range(self.height):
            x1, x2, z1, z2 = self.calculate_position(y, self.time)
            
            # First strand
            if 0 <= x1 < self.width:
                char = self.get_depth_char(z1)
                buffer[y][x1] = char
                depth_buffer[y][x1] = z1
            
            # Second strand
            if 0 <= x2 < self.width:
                char = self.get_depth_char(z2)
                buffer[y][x2] = char
                depth_buffer[y][x2] = z2
            
            # Connecting pairs
            if 0 <= x1 < self.width and 0 <= x2 < self.width:
                pair = self.pairs[y % len(self.pairs)]
                mid_x = (x1 + x2) // 2
                if 0 <= mid_x < self.width:
                    buffer[y][mid_x] = pair[0] if z1 > z2 else pair[2]
        
        # Add title
        title = "DNA DOUBLE HELIX ANIMATION"
        title_x = (self.width - len(title)) // 2
        if title_x >= 0:
            for i, char in enumerate(title):
                if title_x + i < self.width:
                    buffer[0][title_x + i] = char
        
        # Add info
        info = f"Time: {self.time:.1f} | Press Ctrl+C to exit"
        info_x = (self.width - len(info)) // 2
        if info_x >= 0:
            for i, char in enumerate(info):
                if info_x + i < self.width:
                    buffer[self.height-1][info_x + i] = char
        
        # Print buffer
        for row in buffer:
            print(''.join(row))
        
        self.time += self.speed

def main():
    helix = DNAHelix()
    
    try:
        while True:
            helix.render()
            time.sleep(0.05)
    except KeyboardInterrupt:
        print("\nAnimation stopped. Goodbye!")
        sys.exit(0)

if __name__ == "__main__":
    main()
