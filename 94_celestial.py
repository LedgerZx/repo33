import pygame
import math
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1200, 800
FPS = 60
G = 6.67430e-11  # Gravitational constant
SCALE = 250 / 1e9  # Scale: 250 pixels = 1 billion km
TIMESTEP = 3600 * 24  # One day in seconds

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
DARK_GREY = (80, 78, 81)

class CelestialBody:
    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass
        
        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0
        
        self.x_vel = 0
        self.y_vel = 0
        
    def draw(self, win, offset_x, offset_y):
        x = self.x * SCALE + WIDTH // 2 + offset_x
        y = self.y * SCALE + HEIGHT // 2 + offset_y
        
        if len(self.orbit) > 2:
            points = []
            for point in self.orbit:
                x, y = point[0] * SCALE + WIDTH // 2 + offset_x, point[1] * SCALE + HEIGHT // 2 + offset_y
                points.append((x, y))
            
            if len(points) > 2:
                pygame.draw.lines(win, self.color, False, points, 1)
        
        pygame.draw.circle(win, self.color, (int(x), int(y)), self.radius)
        
        if not self.sun:
            distance_text = FONT.render(f"{round(self.distance_to_sun/1e9, 1)} Gm", 1, WHITE)
            win.blit(distance_text, (x - distance_text.get_width()/2, y + self.radius))
    
    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)
        
        if other.sun:
            self.distance_to_sun = distance
        
        force = G * self.mass * other.mass / distance ** 2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        
        return force_x, force_y
    
    def update_position(self, bodies):
        total_fx = total_fy = 0
        for body in bodies:
            if self == body:
                continue
                
            fx, fy = self.attraction(body)
            total_fx += fx
            total_fy += fy
        
        self.x_vel += total_fx / self.mass * TIMESTEP
        self.y_vel += total_fy / self.mass * TIMESTEP
        
        self.x += self.x_vel * TIMESTEP
        self.y += self.y_vel * TIMESTEP
        
        self.orbit.append((self.x, self.y))
        
        if len(self.orbit) > 500:
            self.orbit.pop(0)

def create_solar_system():
    sun = CelestialBody(0, 0, 30, YELLOW, 1.98892e30)
    sun.sun = True
    
    earth = CelestialBody(-1.496e11, 0, 16, BLUE, 5.9742e24)
    earth.y_vel = 29.78e3
    
    mars = CelestialBody(-2.279e11, 0, 12, RED, 6.39e23)
    mars.y_vel = 24.07e3
    
    mercury = CelestialBody(5.79e10, 0, 8, DARK_GREY, 3.3e23)
    mercury.y_vel = -47.4e3
    
    venus = CelestialBody(-1.082e11, 0, 14, WHITE, 4.8685e24)
    venus.y_vel = -35.02e3
    
    # Add some asteroids
    asteroids = []
    for _ in range(50):
        distance = random.uniform(2.2e11, 3.2e11)  # Asteroid belt region
        angle = random.uniform(0, 2 * math.pi)
        x = distance * math.cos(angle)
        y = distance * math.sin(angle)
        
        asteroid = CelestialBody(x, y, 2, DARK_GREY, random.uniform(1e15, 1e17))
        
        # Calculate orbital velocity
        orbital_speed = math.sqrt(G * sun.mass / distance)
        asteroid.x_vel = -orbital_speed * math.sin(angle)
        asteroid.y_vel = orbital_speed * math.cos(angle)
        
        asteroids.append(asteroid)
    
    return [sun, earth, mars, mercury, venus] + asteroids

def main():
    global FONT
    FONT = pygame.font.SysFont("comicsans", 16)
    
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Space Simulation")
    clock = pygame.time.Clock()
    
    bodies = create_solar_system()
    
    offset_x = 0
    offset_y = 0
    zoom = 1.0
    
    running = True
    paused = False
    
    while running:
        clock.tick(FPS)
        
        win.fill(BLACK)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key == pygame.K_r:
                    bodies = create_solar_system()
                    offset_x = 0
                    offset_y = 0
                    zoom = 1.0
        
        # Camera controls
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            offset_x += 10
        if keys[pygame.K_RIGHT]:
            offset_x -= 10
        if keys[pygame.K_UP]:
            offset_y += 10
        if keys[pygame.K_DOWN]:
            offset_y -= 10
        if keys[pygame.K_PLUS] or keys[pygame.K_EQUALS]:
            zoom *= 1.05
        if keys[pygame.K_MINUS]:
            zoom /= 1.05
        
        if not paused:
            for body in bodies:
                body.update_position(bodies)
        
        for body in bodies:
            body.draw(win, offset_x, offset_y)
        
        # Display controls
        controls = [
            "Controls:",
            "Arrow Keys: Pan camera",
            "+/-: Zoom in/out",
            "Space: Pause/Resume",
            "R: Reset simulation"
        ]
        
        y_offset = 10
        for text in controls:
            rendered = FONT.render(text, 1, WHITE)
            win.blit(rendered, (10, y_offset))
            y_offset += 20
        
        # Display FPS and body count
        fps_text = FONT.render(f"FPS: {int(clock.get_fps())}", 1, WHITE)
        win.blit(fps_text, (WIDTH - 100, 10))
        
        body_count = FONT.render(f"Bodies: {len(bodies)}", 1, WHITE)
        win.blit(body_count, (WIDTH - 100, 30))
        
        if paused:
            pause_text = FONT.render("PAUSED", 1, WHITE)
            win.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, 50))
        
        pygame.display.update()
    
    pygame.quit()

if __name__ == "__main__":
    main()
