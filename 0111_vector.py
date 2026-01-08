import curses
import random
import time
import math

# --- Configuration ---
WIDTH = 40
HEIGHT = 20
NUM_SNAKES = 3
START_LENGTH = 3
FOOD_COUNT = 5
SNAKE_CHARS = ['@', '#', '*']
FOOD_CHAR = 'o'

class Vector:
    """A simple 2D vector class for movement calculations."""
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def add(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def sub(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def normalize(self):
        mag = math.sqrt(self.x**2 + self.y**2)
        if mag == 0:
            return Vector(0, 0)
        return Vector(self.x / mag, self.y / mag)

class Food:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Snake:
    def __init__(self, x, y, char, color):
        self.body = [Vector(x, y) for _ in range(START_LENGTH)]
        self.direction = Vector(random.choice([-1, 0, 1]), random.choice([-1, 0, 1]))
        # Ensure non-zero start direction
        while self.direction.x == 0 and self.direction.y == 0:
            self.direction = Vector(random.choice([-1, 0, 1]), random.choice([-1, 0, 1]))
        self.char = char
        self.color = color
        self.alive = True
        self.grow_pending = 0

    def move(self, target_pos, all_snakes):
        if not self.alive:
            return

        head = self.body[-1]

        # 1. Calculate vector to nearest food
        to_food = target_pos.sub(head)
        desired_dir = to_food.normalize()

        # 2. Simple "steering" behavior
        # Determine potential moves (Up, Down, Left, Right)
        possible_moves = [
            Vector(0, -1), Vector(0, 1), Vector(-1, 0), Vector(1, 0)
        ]

        best_move = self.direction
        min_dist = float('inf')

        # Evaluate moves based on distance to food and collision avoidance
        for move in possible_moves:
            # Don't reverse immediately
            if move.x == -self.direction.x and move.y == -self.direction.y:
                continue

            next_pos = head.add(move)
            
            # Boundary check
            if next_pos.x < 0 or next_pos.x >= WIDTH or next_pos.y < 0 or next_pos.y >= HEIGHT:
                continue

            # Self-collision check
            collision = False
            for segment in self.body:
                if next_pos.x == segment.x and next_pos.y == segment.y:
                    collision = True
                    break
            
            # Collision with other snakes
            if not collision:
                for other in all_snakes:
                    if other != self and other.alive:
                        for segment in other.body:
                            if next_pos.x == segment.x and next_pos.y == segment.y:
                                collision = True
                                break
                    if collision: break

            if collision:
                continue

            # Heuristic: Choose move that minimizes distance to food
            # Dot product to check alignment with desired direction
            alignment = (move.x * desired_dir.x + move.y * desired_dir.y)
            
            # We want high alignment (move towards food)
            if alignment > 0:
                if alignment < min_dist: # Lower alignment score is actually worse here, so we flip logic slightly for variety
                    # Let's use Euclidean distance to food strictly
                    dist = math.sqrt((next_pos.x - target_pos.x)**2 + (next_pos.y - target_pos.y)**2)
                    if dist < min_dist:
                        min_dist = dist
                        best_move = move
                else:
                     # Fallback to keep momentum if food is far
                     best_move = move if best_move == self.direction else best_move

        self.direction = best_move
        new_head = head.add(self.direction)
        
        self.body.append(new_head)
        
        if self.grow_pending > 0:
            self.grow_pending -= 1
        else:
            self.body.pop(0) # Remove tail

    def check_eat(self, foods):
        if not self.alive:
            return
        
        head = self.body[-1]
        for food in foods[:]:
            if head.x == food.x and head.y == food.y:
                foods.remove(food)
                self.grow_pending += 1
                foods.append(Food(random.randint(0, WIDTH-1), random.randint(0, HEIGHT-1)))
                return True
        return False

def main(stdscr):
    # Setup curses
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(100)

    # Initialize colors
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)

    colors = [1, 2, 3]

    # Initialize entities
    foods = [Food(random.randint(0, WIDTH-1), random.randint(0, HEIGHT-1)) for _ in range(FOOD_COUNT)]
    snakes = []
    for i in range(NUM_SNAKES):
        s = Snake(random.randint(5, WIDTH-5), random.randint(5, HEIGHT-5), SNAKE_CHARS[i % 3], colors[i % 3])
        snakes.append(s)

    try:
        while True:
            stdscr.clear()

            # Draw Border
            stdscr.border(0)

            # Logic
            alive_count = 0
            for snake in snakes:
                if snake.alive:
                    alive_count += 1
                    
                    # Find nearest food
                    nearest_food = None
                    min_dist = float('inf')
                    for f in foods:
                        d = math.sqrt((snake.body[-1].x - f.x)**2 + (snake.body[-1].y - f.y)**2)
                        if d < min_dist:
                            min_dist = d
                            nearest_food = f
                    
                    if nearest_food:
                        snake.move(nearest_food, snakes)
                    
                    # Draw Snake
                    for segment in snake.body:
                        try:
                            stdscr.addch(segment.y + 1, segment.x + 1, snake.char, curses.color_pair(snake.color + 1))
                        except curses.error:
                            pass # Ignore drawing errors at edges

                    # Check collision with walls (simple check)
                    head = snake.body[-1]
                    if head.x < 0 or head.x >= WIDTH or head.y < 0 or head.y >= HEIGHT:
                        snake.alive = False

                    snake.check_eat(foods)

            # Draw Food
            for f in foods:
                try:
                    stdscr.addch(f.y + 1, f.x + 1, FOOD_CHAR, curses.color_pair(4))
                except curses.error:
                    pass

            # Status info
            status = f"Snakes Alive: {alive_count}/{NUM_SNAKES}"
            stdscr.addstr(0, 2, status, curses.color_pair(4))

            # Quit check
            key = stdscr.getch()
            if key == ord('q'):
                break

            stdscr.refresh()

    finally:
        curses.endwin()

if __name__ == "__main__":
    print("Starting Snake Simulation...")
    print("Controls: Press 'q' to quit.")
    time.sleep(1)
    curses.wrapper(main)
