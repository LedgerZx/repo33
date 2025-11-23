import math
import time
import os
import sys
from typing import List, Tuple

class DNAHelix3D:
    def __init__(self, width: int = 80, height: int = 24):
        self.width = width
        self.height = height
        self.time = 0
        self.rotation_speed = 0.05
        self.helix_radius = 8
        self.helix_height = 15
        self.base_pairs = 20
        self.z_buffer = [[-float('inf')] * width for _ in range(height)]
        self.screen = [[' '] * width for _ in range(height)]
        
        # Characters for different depths
        self.depth_chars = ' .:-=+*#%@'
        
    def rotate_point_3d(self, x: float, y: float, z: float, angle_x: float, angle_y: float) -> Tuple[float, float, float]:
        """Rotate a 3D point around X and Y axes"""
        # Rotate around Y axis
        cos_y = math.cos(angle_y)
        sin_y = math.sin(angle_y)
        x_rot = x * cos_y - z * sin_y
        z_rot = x * sin_y + z * cos_y
        
        # Rotate around X axis
        cos_x = math.cos(angle_x)
        sin_x = math.sin(angle_x)
        y_rot = y * cos_x - z_rot * sin_x
        z_final = y * sin_x + z_rot * cos_x
        
        return x_rot, y_rot, z_final
    
    def project_3d_to_2d(self, x: float, y: float, z: float) -> Tuple[int, int, float]:
        """Project 3D coordinates to 2D screen with perspective"""
        if z + 10 <= 0:
            return None
        
        perspective_scale = 30 / (z + 10)
        screen_x = int(self.width / 2 + x * perspective_scale)
        screen_y = int(self.height / 2 - y * perspective_scale)
        
        return screen_x, screen_y, z
    
    def draw_helix_strand(self, offset: float, char: str):
        """Draw one strand of the DNA helix"""
        for i in range(self.base_pairs * 4):
            t = i / 4.0
            y = (t - self.base_pairs / 2) * (self.helix_height / self.base_pairs)
            
            # Create helix shape
            angle = t * 2 * math.pi / 4 + offset
            x = self.helix_radius * math.cos(angle)
            z = self.helix_radius * math.sin(angle)
            
            # Apply rotation
            x_rot, y_rot, z_rot = self.rotate_point_3d(
                x, y, z, 
                math.sin(self.time) * 0.3, 
                self.time
            )
            
            # Project to 2D
            result = self.project_3d_to_2d(x_rot, y_rot, z_rot)
            if result:
                screen_x, screen_y, depth = result
                
                if 0 <= screen_x < self.width and 0 <= screen_y < self.height:
                    # Update z-buffer and screen if closer to viewer
                    if depth > self.z_buffer[screen_y][screen_x]:
                        self.z_buffer[screen_y][screen_x] = depth
                        # Choose character based on depth
                        depth_index = min(int((depth + 10) / 20 * len(self.depth_chars)), 
                                        len(self.depth_chars) - 1)
                        self.screen[screen_y][screen_x] = self.depth_chars[depth_index]
    
    def draw_base_pairs(self):
        """Draw connecting base pairs between strands"""
        for i in range(self.base_pairs):
            t = i
            y = (t - self.base_pairs / 2) * (self.helix_height / self.base_pairs)
            
            # Calculate positions for both strands
            angle1 = t * 2 * math.pi / 4 + self.time
            angle2 = angle1 + math.pi
            
            # First strand point
            x1 = self.helix_radius * math.cos(angle1)
            z1 = self.helix_radius * math.sin(angle1)
            x1_rot, y1_rot, z1_rot = self.rotate_point_3d(
                x1, y, z1, 
                math.sin(self.time) * 0.3, 
                self.time
            )
            
            # Second strand point
            x2 = self.helix_radius * math.cos(angle2)
            z2 = self.helix_radius * math.sin(angle2)
            x2_rot, y2_rot, z2_rot = self.rotate_point_3d(
                x2, y, z2, 
                math.sin(self.time) * 0.3, 
                self.time
            )
            
            # Draw line between points (simplified as a few points)
            for j in range(5):
                t_line = j / 4.0
                x_line = x1_rot + (x2_rot - x1_rot) * t_line
                y_line = y1_rot + (y2_rot - y1_rot) * t_line
                z_line = z1_rot + (z2_rot - z1_rot) * t_line
                
                result = self.project_3d_to_2d(x_line, y_line, z_line)
                if result:
                    screen_x, screen_y, depth = result
                    
                    if 0 <= screen_x < self.width and 0 <= screen_y < self.height:
                        if depth > self.z_buffer[screen_y][screen_x]:
                            self.z_buffer[screen_y][screen_x] = depth
                            self.screen[screen_y][screen_x] = '-'
    
    def render(self):
        """Render the complete DNA helix"""
        # Clear buffers
        self.z_buffer = [[-float('inf')] * self.width for _ in range(self.height)]
        self.screen = [[' '] * self.width for _ in range(self.height)]
        
        # Draw both strands
        self.draw_helix_strand(0, '@')
        self.draw_helix_strand(math.pi, '#')
        
        # Draw base pairs
        self.draw_base_pairs()
        
        # Convert screen to string
        return '\n'.join(''.join(row) for row in self.screen)
    
    def animate(self):
        """Run the animation"""
        try:
            while True:
                # Clear screen
                os.system('cls' if os.name == 'nt' else 'clear')
                
                # Render frame
                frame = self.render()
                print(frame)
                
                # Add info text
                print(f"\nDNA Helix 3D Animation | Time: {self.time:.2f} | Press Ctrl+C to exit")
                
                # Update time
                self.time += self.rotation_speed
                
                # Control frame rate
                time.sleep(0.03)
                
        except KeyboardInterrupt:
            print("\nAnimation stopped. Goodbye!")

def main():
    """Main function to run the DNA helix animation"""
    print("Initializing 3D DNA Helix Animation...")
    print("This script creates a rotating DNA double helix in your terminal!")
    print("\nControls:")
    print("- The helix will automatically rotate")
    print("- Press Ctrl+C to exit")
    print("\nStarting animation in 2 seconds...")
    
    time.sleep(2)
    
    # Create and run animation
    helix = DNAHelix3D()
    helix.animate()

if __name__ == "__main__":
    main()
