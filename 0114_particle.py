import pygame
import numpy as np
import random
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1200, 800
BACKGROUND_COLOR = (10, 10, 20)
FPS = 60
G = 0.5  # Gravitational constant
PARTICLE_COUNT = 150
TRAIL_LENGTH = 20

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-2, 2)
        self.mass = random.uniform(1, 5)
        self.radius = int(self.mass * 2)
        self.color = (
            random.randint(100, 255),
            random.randint(100, 255),
            random.randint(100, 255)
        )
        self.trail = []
        
    def apply_force(self, fx, fy):
        ax = fx / self.mass
        ay = fy / self.mass
        self.vx += ax
        self.vy += ay
        
    def update(self):
        # Update position
        self.x += self.vx
        self.y += self.vy
        
        # Add damping
        self.vx *= 0.999
        self.vy *= 0.999
        
        # Bounce off walls
        if self.x <= self.radius or self.x >= WIDTH - self.radius:
            self.vx *= -0.8
            self.x = max(self.radius, min(WIDTH - self.radius, self.x))
            
        if self.y <= self.radius or self.y >= HEIGHT - self.radius:
            self.vy *= -0.8
            self.y = max(self.radius, min(HEIGHT - self.radius, self.y))
        
        # Update trail
        self.trail.append((int(self.x), int(self.y)))
        if len(self.trail) > TRAIL_LENGTH:
            self.trail.pop(0)
    
    def draw(self, screen):
        # Draw trail
        if len(self.trail) > 1:
            for i in range(len(self.trail) - 1):
                alpha = int(255 * (i / len(self.trail)))
                color = (*self.color, alpha)
                start_pos = self.trail[i]
                end_pos = self.trail[i + 1]
                pygame.draw.line(screen, self.color[:3], start_pos, end_pos, 1)
        
        # Draw particle with glow effect
        for i in range(3):
            glow_radius = self.radius + (3 - i) * 3
            glow_alpha = 30 - i * 10
            glow_color = tuple(min(255, c + glow_alpha) for c in self.color)
            pygame.draw.circle(screen, glow_color, (int(self.x), int(self.y)), glow_radius)
        
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

def calculate_gravitational_force(p1, p2):
    dx = p2.x - p1.x
    dy = p2.y - p1.y
    distance = math.sqrt(dx**2 + dy**2)
    
    if distance < p1.radius + p2.radius:
        return 0, 0  # Prevent collision
    
    # Calculate gravitational force
    force = G * p1.mass * p2.mass / (distance**2)
    
    # Calculate force components
    fx = force * (dx / distance)
    fy = force * (dy / distance)
    
    return fx, fy

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Gravitational Particle System")
    clock = pygame.time.Clock()
    
    # Create particles
    particles = []
    for _ in range(PARTICLE_COUNT):
        x = random.randint(50, WIDTH - 50)
        y = random.randint(50, HEIGHT - 50)
        particles.append(Particle(x, y))
    
    # Create a central massive particle
    center_particle = Particle(WIDTH // 2, HEIGHT // 2)
    center_particle.mass = 20
    center_particle.radius = 15
    center_particle.color = (255, 200, 100)
    center_particle.vx = 0
    center_particle.vy = 0
    particles.append(center_particle)
    
    running = True
    mouse_pressed = False
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pressed = True
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_pressed = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Add new particle at mouse position
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    particles.append(Particle(mouse_x, mouse_y))
                elif event.key == pygame.K_r:
                    # Reset particles
                    particles.clear()
                    for _ in range(PARTICLE_COUNT):
                        x = random.randint(50, WIDTH - 50)
                        y = random.randint(50, HEIGHT - 50)
                        particles.append(Particle(x, y))
        
        # Clear screen
        screen.fill(BACKGROUND_COLOR)
        
        # Apply gravitational forces between particles
        for i, p1 in enumerate(particles):
            for j, p2 in enumerate(particles):
                if i != j:
                    fx, fy = calculate_gravitational_force(p1, p2)
                    p1.apply_force(fx, fy)
        
        # Update and draw particles
        for particle in particles:
            particle.update()
            particle.draw(screen)
        
        # Draw mouse attraction when pressed
        if mouse_pressed:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for particle in particles:
                dx = mouse_x - particle.x
                dy = mouse_y - particle.y
                distance = math.sqrt(dx**2 + dy**2)
                if distance > 0:
                    force = 50 / distance
                    fx = force * (dx / distance)
                    fy = force * (dy / distance)
                    particle.apply_force(fx, fy)
            
            pygame.draw.circle(screen, (255, 255, 255), (mouse_x, mouse_y), 20, 2)
        
        # Draw instructions
        font = pygame.font.Font(None, 24)
        instructions = [
            "SPACE: Add particle at mouse",
            "R: Reset particles",
            "Click & Hold: Attract particles"
        ]
        for i, text in enumerate(instructions):
            text_surface = font.render(text, True, (150, 150, 150))
            screen.blit(text_surface, (10, 10 + i * 25))
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()

if __name__ == "__main__":
    main()
