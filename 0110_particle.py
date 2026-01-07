import pygame
import numpy as np
import random
import math

class Particle:
    def __init__(self, x, y, screen_width, screen_height):
        self.x = x
        self.y = y
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-2, 2)
        self.radius = random.uniform(2, 8)
        self.mass = self.radius * 0.5
        self.color = (
            random.randint(100, 255),
            random.randint(100, 255),
            random.randint(100, 255)
        )
        self.trail = []
        self.max_trail_length = 20
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.gravity_strength = 0.1
        
    def update(self, particles, mouse_pos=None):
        # Apply gravity to other particles
        for other in particles:
            if other != self:
                dx = other.x - self.x
                dy = other.y - self.y
                distance = math.sqrt(dx**2 + dy**2)
                
                if distance > 0 and distance < 200:
                    # Gravitational attraction
                    force = (self.gravity_strength * self.mass * other.mass) / (distance**2)
                    ax = force * (dx / distance) / self.mass
                    ay = force * (dy / distance) / self.mass
                    self.vx += ax
                    self.vy += ay
        
        # Mouse interaction
        if mouse_pos:
            dx = mouse_pos[0] - self.x
            dy = mouse_pos[1] - self.y
            distance = math.sqrt(dx**2 + dy**2)
            
            if distance < 150 and distance > 0:
                # Repel from mouse
                force = 50 / distance
                self.vx -= force * (dx / distance)
                self.vy -= force * (dy / distance)
        
        # Apply damping
        self.vx *= 0.99
        self.vy *= 0.99
        
        # Update position
        self.x += self.vx
        self.y += self.vy
        
        # Add to trail
        self.trail.append((self.x, self.y))
        if len(self.trail) > self.max_trail_length:
            self.trail.pop(0)
        
        # Bounce off walls
        if self.x - self.radius < 0 or self.x + self.radius > self.screen_width:
            self.vx *= -0.8
            self.x = max(self.radius, min(self.screen_width - self.radius, self.x))
        
        if self.y - self.radius < 0 or self.y + self.radius > self.screen_height:
            self.vy *= -0.8
            self.y = max(self.radius, min(self.screen_height - self.radius, self.y))
    
    def draw(self, screen):
        # Draw trail
        for i, pos in enumerate(self.trail):
            alpha = i / len(self.trail)
            trail_color = tuple(int(c * alpha) for c in self.color)
            pygame.draw.circle(screen, trail_color, (int(pos[0]), int(pos[1])), 
                             int(self.radius * alpha * 0.5))
        
        # Draw particle with glow effect
        for i in range(3):
            glow_radius = self.radius * (3 - i)
            glow_alpha = 0.1 * (i + 1)
            glow_color = tuple(int(c * glow_alpha) for c in self.color)
            pygame.draw.circle(screen, glow_color, (int(self.x), int(self.y)), 
                             int(glow_radius))
        
        # Draw main particle
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 
                         int(self.radius))

class ParticleSystem:
    def __init__(self, width=1200, height=800, num_particles=50):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Interactive Particle System")
        self.clock = pygame.time.Clock()
        self.particles = []
        self.running = True
        self.mouse_pos = None
        self.show_connections = True
        
        # Create particles
        for _ in range(num_particles):
            x = random.uniform(50, width - 50)
            y = random.uniform(50, height - 50)
            self.particles.append(Particle(x, y, width, height))
    
    def draw_connections(self):
        for i, p1 in enumerate(self.particles):
            for p2 in self.particles[i+1:]:
                dx = p1.x - p2.x
                dy = p1.y - p2.y
                distance = math.sqrt(dx**2 + dy**2)
                
                if distance < 100:
                    alpha = 1 - (distance / 100)
                    color = (100 * alpha, 150 * alpha, 255 * alpha)
                    pygame.draw.line(self.screen, color, 
                                   (int(p1.x), int(p1.y)), 
                                   (int(p2.x), int(p2.y)), 1)
    
    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        # Add new particle at mouse position
                        if self.mouse_pos:
                            self.particles.append(
                                Particle(self.mouse_pos[0], self.mouse_pos[1], 
                                       self.width, self.height)
                            )
                    elif event.key == pygame.K_c:
                        # Toggle connections
                        self.show_connections = not self.show_connections
                    elif event.key == pygame.K_r:
                        # Reset particles
                        self.particles.clear()
                        for _ in range(50):
                            x = random.uniform(50, self.width - 50)
                            y = random.uniform(50, self.height - 50)
                            self.particles.append(Particle(x, y, self.width, self.height))
                elif event.type == pygame.MOUSEMOTION:
                    self.mouse_pos = event.pos
            
            # Clear screen
            self.screen.fill((10, 10, 20))
            
            # Update and draw particles
            for particle in self.particles:
                particle.update(self.particles, self.mouse_pos)
                particle.draw(self.screen)
            
            # Draw connections between nearby particles
            if self.show_connections:
                self.draw_connections()
            
            # Draw instructions
            font = pygame.font.Font(None, 24)
            instructions = [
                "SPACE: Add particle at mouse",
                "C: Toggle connections",
                "R: Reset particles",
                "Move mouse to repel particles"
            ]
            for i, text in enumerate(instructions):
                text_surface = font.render(text, True, (150, 150, 150))
                self.screen.blit(text_surface, (10, 10 + i * 25))
            
            # Show particle count
            count_text = font.render(f"Particles: {len(self.particles)}", True, (150, 150, 150))
            self.screen.blit(count_text, (self.width - 150, 10))
            
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()

if __name__ == "__main__":
    system = ParticleSystem()
    system.run()
