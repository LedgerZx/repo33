import random
import time
import os
import sys
from collections import deque

class MazeGame:
    def __init__(self, width=21, height=11):
        self.width = width if width % 2 == 1 else width + 1
        self.height = height if height % 2 == 1 else height + 1
        self.maze = []
        self.player_pos = [1, 1]
        self.exit_pos = [self.width - 2, self.height - 2]
        self.visited = set()
        self.path = []
        self.move_count = 0
        self.trail = []
        
    def generate_maze(self):
        # Initialize maze with walls
        self.maze = [['█' for _ in range(self.width)] for _ in range(self.height)]
        
        # Recursive backtracking maze generation
        def carve(x, y):
            self.maze[y][x] = ' '
            directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
            random.shuffle(directions)
            
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 < nx < self.width - 1 and 0 < ny < self.height - 1:
                    if self.maze[ny][nx] == '█':
                        self.maze[y + dy // 2][x + dx // 2] = ' '
                        carve(nx, ny)
        
        carve(1, 1)
        self.maze[self.exit_pos[1]][self.exit_pos[0]] = 'E'
        
        # Add some random items
        for _ in range(random.randint(3, 7)):
            x, y = random.randint(1, self.width - 2), random.randint(1, self.height - 2)
            if self.maze[y][x] == ' ' and (x, y) != tuple(self.player_pos):
                self.maze[y][x] = random.choice(['$', '♠', '♥', '♦', '♣'])
    
    def find_path(self):
        # BFS pathfinding to exit
        queue = deque([(self.player_pos[0], self.player_pos[1], [])])
        visited = set()
        
        while queue:
            x, y, path = queue.popleft()
            
            if (x, y) == (self.exit_pos[0], self.exit_pos[1]):
                return path + [(x, y)]
            
            if (x, y) in visited:
                continue
                
            visited.add((x, y))
            
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if self.maze[ny][nx] != '█':
                        queue.append((nx, ny, path + [(x, y)]))
        
        return []
    
    def display(self):
        os.system('clear' if os.name == 'posix' else 'cls')
        
        # Create display copy
        display = [row[:] for row in self.maze]
        
        # Show trail
        for x, y in self.trail[-10:]:  # Show last 10 positions
            if display[y][x] == ' ':
                display[y][x] = '.'
        
        # Show path hint if requested
        if hasattr(self, 'show_hint') and self.show_hint and self.path:
            for x, y in self.path[:5]:  # Show first 5 steps of path
                if display[y][x] == ' ':
                    display[y][x] = '·'
        
        # Place player
        display[self.player_pos[1]][self.player_pos[0]] = '@'
        
        # Print maze with stats
        print("═" * (self.width + 2))
        for row in display:
            print("║" + "".join(row) + "║")
        print("═" * (self.width + 2))
        print(f"Moves: {self.move_count} | Position: ({self.player_pos[0]}, {self.player_pos[1]})")
        print("Controls: WASD/Arrow keys to move, H for hint, R to restart, Q to quit")
        
        # Check for items
        cell = self.maze[self.player_pos[1]][self.player_pos[0]]
        if cell in ['$', '♠', '♥', '♦', '♣']:
            print(f"You found a {cell}!")
            self.maze[self.player_pos[1]][self.player_pos[0]] = ' '
    
    def move(self, dx, dy):
        new_x = self.player_pos[0] + dx
        new_y = self.player_pos[1] + dy
        
        if 0 <= new_x < self.width and 0 <= new_y < self.height:
            if self.maze[new_y][new_x] != '█':
                self.trail.append((self.player_pos[0], self.player_pos[1]))
                self.player_pos = [new_x, new_y]
                self.move_count += 1
                self.visited.add((new_x, new_y))
                
                # Check win condition
                if (new_x, new_y) == (self.exit_pos[0], self.exit_pos[1]):
                    return True
        return False
    
    def animate_solution(self):
        if not self.path:
            print("No path found!")
            return
        
        print("Showing solution path...")
        time.sleep(1)
        
        temp_pos = self.player_pos[:]
        for x, y in self.path:
            self.player_pos = [x, y]
            self.display()
            time.sleep(0.1)
        
        self.player_pos = temp_pos
    
    def run(self):
        self.generate_maze()
        self.path = self.find_path()
        self.show_hint = False
        
        while True:
            self.display()
            
            # Non-blocking input check
            try:
                import msvcrt
                if msvcrt.kbhit():
                    key = msvcrt.getch().decode('utf-8').lower()
                else:
                    time.sleep(0.1)
                    continue
            except ImportError:
                # Unix-like systems
                import select
                import termios
                import tty
                
                old_settings = termios.tcgetattr(sys.stdin)
                try:
                    tty.setraw(sys.stdin.fileno())
                    if select.select([sys.stdin], [], [], 0.1)[0]:
                        key = sys.stdin.read(1).lower()
                    else:
                        continue
                finally:
                    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
            
            # Handle input
            if key in ['w', 'a', 's', 'd']:
                moves = {'w': (0, -1), 'a': (-1, 0), 's': (0, 1), 'd': (1, 0)}
                if self.move(*moves[key]):
                    print("\n🎉 Congratulations! You escaped the maze!")
                    print(f"Total moves: {self.move_count}")
                    print(f"Explored: {len(self.visited)} cells")
                    break
            elif key == 'h':
                self.show_hint = not self.show_hint
            elif key == 'r':
                self.__init__(self.width, self.height)
                self.generate_maze()
                self.path = self.find_path()
            elif key == 'q':
                print("Thanks for playing!")
                break
            elif key == '\x03':  # Ctrl+C
                raise KeyboardInterrupt

if __name__ == "__main__":
    try:
        print("🌀 Dynamic Maze Explorer 🌀")
        print("Find your way to the exit (E)!")
        time.sleep(2)
        
        game = MazeGame()
        game.run()
    except KeyboardInterrupt:
        print("\nGame interrupted. Thanks for playing!")
