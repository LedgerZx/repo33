import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
import random

class TerrainGenerator:
    def __init__(self, width=100, height=100, scale=20.0, octaves=6, persistence=0.5, lacunarity=2.0):
        self.width = width
        self.height = height
        self.scale = scale
        self.octaves = octaves
        self.persistence = persistence
        self.lacunarity = lacunarity
        self.seed = random.randint(0, 1000)
        
    def fade(self, t):
        """Smoothing function for Perlin noise"""
        return t * t * t * (t * (t * 6 - 15) + 10)
    
    def lerp(self, a, b, t):
        """Linear interpolation"""
        return a + t * (b - a)
    
    def grad(self, hash_val, x, y):
        """Generate pseudo-random gradient vector"""
        h = hash_val & 3
        u = x if h < 2 else y
        v = y if h < 2 else x
        return (u if (h & 1) == 0 else -u) + (v if (h & 2) == 0 else -v)
    
    def perlin_noise(self, x, y):
        """Generate Perlin noise value for given coordinates"""
        # Determine grid cell coordinates
        x0 = int(np.floor(x))
        x1 = x0 + 1
        y0 = int(np.floor(y))
        y1 = y0 + 1
        
        # Determine interpolation weights
        sx = self.fade(x - x0)
        sy = self.fade(y - y0)
        
        # Hash coordinates of the corners of the cell
        def hash_func(x, y):
            h = (x * 374761393 + y * 668265263 + self.seed) % 1073741824
            return h
        
        n00 = self.grad(hash_func(x0, y0), x - x0, y - y0)
        n10 = self.grad(hash_func(x1, y0), x - x1, y - y0)
        n01 = self.grad(hash_func(x0, y1), x - x0, y - y1)
        n11 = self.grad(hash_func(x1, y1), x - x1, y - y1)
        
        # Interpolate along x
        nx0 = self.lerp(n00, n10, sx)
        nx1 = self.lerp(n01, n11, sx)
        
        # Interpolate along y
        nxy = self.lerp(nx0, nx1, sy)
        
        return nxy
    
    def octave_noise(self, x, y):
        """Generate fractal noise using multiple octaves"""
        total = 0.0
        amplitude = 1.0
        max_value = 0.0
        
        for _ in range(self.octaves):
            total += self.perlin_noise(x * amplitude, y * amplitude) * amplitude
            max_value += amplitude
            amplitude *= self.persistence
        
        return total / max_value
    
    def generate_terrain(self):
        """Generate terrain height map"""
        terrain = np.zeros((self.height, self.width))
        
        for y in range(self.height):
            for x in range(self.width):
                nx = x / self.width - 0.5
                ny = y / self.height - 0.5
                
                # Generate base noise
                elevation = self.octave_noise(nx * self.scale, ny * self.scale)
                
                # Add ridges for mountain-like features
                ridge_noise = abs(self.octave_noise(nx * self.scale * 2, ny * self.scale * 2))
                elevation = elevation * 0.7 + ridge_noise * 0.3
                
                # Add some detail
                detail = self.octave_noise(nx * self.scale * 4, ny * self.scale * 4) * 0.1
                elevation += detail
                
                terrain[y, x] = elevation
        
        # Normalize to [0, 1]
        terrain = (terrain - terrain.min()) / (terrain.max() - terrain.min())
        
        # Apply elevation curve for more realistic terrain
        terrain = np.power(terrain, 1.5)
        
        return terrain
    
    def apply_erosion(self, terrain, iterations=50):
        """Apply simple hydraulic erosion simulation"""
        for _ in range(iterations):
            new_terrain = terrain.copy()
            
            for y in range(1, self.height - 1):
                for x in range(1, self.width - 1):
                    # Calculate height differences with neighbors
                    neighbors = [
                        terrain[y-1, x], terrain[y+1, x],
                        terrain[y, x-1], terrain[y, x+1]
                    ]
                    
                    avg_height = np.mean(neighbors)
                    height_diff = terrain[y, x] - avg_height
                    
                    # Erode high points, deposit in low points
                    if height_diff > 0.01:
                        erosion_amount = height_diff * 0.1
                        new_terrain[y, x] -= erosion_amount
                        
                        # Distribute eroded material to neighbors
                        for ny in range(y-1, y+2):
                            for nx in range(x-1, x+2):
                                if 0 <= ny < self.height and 0 <= nx < self.width:
                                    if ny != y or nx != x:
                                        new_terrain[ny, nx] += erosion_amount / 8
            
            terrain = new_terrain
        
        return terrain
    
    def get_biome_color(self, height):
        """Assign colors based on elevation (biomes)"""
        if height < 0.2:
            return (0.2, 0.4, 0.8)  # Deep water
        elif height < 0.3:
            return (0.4, 0.6, 0.9)  # Shallow water
        elif height < 0.35:
            return (0.8, 0.7, 0.5)  # Beach
        elif height < 0.5:
            return (0.3, 0.6, 0.2)  # Grassland
        elif height < 0.7:
            return (0.2, 0.4, 0.1)  # Forest
        elif height < 0.85:
            return (0.5, 0.4, 0.3)  # Mountain
        else:
            return (0.9, 0.9, 0.9)  # Snow

def visualize_terrain(terrain, generator):
    """Create 3D visualization of the terrain"""
    fig = plt.figure(figsize=(15, 10))
    
    # Create 3D subplot
    ax = fig.add_subplot(111, projection='3d')
    
    # Create mesh grid
    x = np.arange(0, generator.width, 1)
    y = np.arange(0, generator.height, 1)
    X, Y = np.meshgrid(x, y)
    
    # Apply colors based on elevation
    colors = np.zeros((generator.height, generator.width, 3))
    for y in range(generator.height):
        for x in range(generator.width):
            colors[y, x] = generator.get_biome_color(terrain[y, x])
    
    # Create surface plot
    surf = ax.plot_surface(X, Y, terrain, facecolors=colors, 
                          linewidth=0, antialiased=True, shade=True)
    
    # Set labels and title
    ax.set_xlabel('X Coordinate')
    ax.set_ylabel('Y Coordinate')
    ax.set_zlabel('Elevation')
    ax.set_title('Procedural Terrain Generation', fontsize=16, fontweight='bold')
    
    # Set viewing angle
    ax.view_init(elev=30, azim=45)
    
    # Add colorbar legend
    sm = plt.cm.ScalarMappable(cmap=cm.terrain, norm=plt.Normalize(vmin=0, vmax=1))
    sm.set_array([])
    cbar = fig.colorbar(sm, ax=ax, shrink=0.5, aspect=5)
    cbar.set_label('Elevation', rotation=270, labelpad=15)
    
    plt.tight_layout()
    plt.show()

def main():
    print("Generating procedural terrain...")
    
    # Create terrain generator
    generator = TerrainGenerator(
        width=80,
        height=80,
        scale=15.0,
        octaves=5,
        persistence=0.6,
        lacunarity=2.0
    )
    
    # Generate terrain
    terrain = generator.generate_terrain()
    
    # Apply erosion for more realistic features
    print("Applying erosion simulation...")
    terrain = generator.apply_erosion(terrain, iterations=30)
    
    # Visualize the terrain
    print("Creating 3D visualization...")
    visualize_terrain(terrain, generator)
    
    # Print terrain statistics
    print(f"\nTerrain Statistics:")
    print(f"Min elevation: {terrain.min():.3f}")
    print(f"Max elevation: {terrain.max():.3f}")
    print(f"Mean elevation: {terrain.mean():.3f}")
    print(f"Standard deviation: {terrain.std():.3f}")

if __name__ == "__main__":
    main()
