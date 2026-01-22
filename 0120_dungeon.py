import random
import os
import time
import keyboard
from collections import deque

class DungeonCrawler:
    def __init__(self, width=80, height=24):
        self.width = width
        self.height = height
        self.dungeon = [[' ' for _ in range(width)] for _ in range(height)]
        self.player_pos = None
        self.enemies = []
        self.items = []
        self.visited = [[False for _ in range(width)] for _ in range(height)]
        self.health = 100
        self.max_health = 100
        self.score = 0
        self.level = 1
        self.exp = 0
        self.exp_to_next = 100
        
    def generate_dungeon(self):
        # Clear dungeon
        self.dungeon = [[' ' for _ in range(self.width)] for _ in range(self.height)]
        self.enemies = []
        self.items = []
        
        # Generate rooms
        rooms = []
        min_room_size = 5
        max_room_size = 12
        max_rooms = 15
        
        for _ in range(max_rooms):
            room_width = random.randint(min_room_size, max_room_size)
            room_height = random.randint(min_room_size, max_room_size)
            x = random.randint(1, self.width - room_width - 1)
            y = random.randint(1, self.height - room_height - 1)
            
            # Check if room overlaps with existing rooms
            overlap = False
            for rx, ry, rw, rh in rooms:
                if not (x + room_width < rx or x > rx + rw or 
                        y + room_height < ry or y > ry + rh):
                    overlap = True
                    break
            
            if not overlap:
                rooms.append((x, y, room_width, room_height))
                # Create room
                for ry in range(y, y + room_height):
                    for rx in range(x, x + room_width):
                        if ry == y or ry == y + room_height - 1 or rx == x or rx == x + room_width - 1:
                            self.dungeon[ry][rx] = '#'
                        else:
                            self.dungeon[ry][rx] = '.'
        
        # Connect rooms with corridors
        for i in range(len(rooms) - 1):
            x1, y1, w1, h1 = rooms[i]
            x2, y2, w2, h2 = rooms[i+1]
            
            # Center of rooms
            cx1, cy1 = x1 + w1 // 2, y1 + h1 // 2
            cx2, cy2 = x2 + w2 // 2, y2 + h2 // 2
            
            # Create L-shaped corridor
            if random.choice([True, False]):
                # Horizontal first, then vertical
                for x in range(min(cx1, cx2), max(cx1, cx2) + 1):
                    self.dungeon[cy1][x] = '.'
                for y in range(min(cy1, cy2), max(cy1, cy2) + 1):
                    self.dungeon[y][cx2] = '.'
            else:
                # Vertical first, then horizontal
                for y in range(min(cy1, cy2), max(cy1, cy2) + 1):
                    self.dungeon[y][cx1] = '.'
                for x in range(min(cx1, cx2), max(cx1, cx2) + 1):
                    self.dungeon[cy2][x] = '.'
        
        # Place player in first room
        if rooms:
            x, y, w, h = rooms[0]
            self.player_pos = [x + w // 2, y + h // 2]
            self.visited[y + h // 2][x + w // 2] = True
        
        # Place enemies in rooms
        for i, (x, y, w, h) in enumerate(rooms[1:], 1):
            if random.random() < 0.7:  # 70% chance of enemies in a room
                num_enemies = random.randint(1, 3)
                for _ in range(num_enemies):
                    ex = random.randint(x + 1, x + w - 2)
                    ey = random.randint(y + 1, y + h - 2)
                    enemy_type = random.choice(['g', 'o', 'D'])  # goblin, orc, dragon
                    self.enemies.append({
                        'pos': [ex, ey],
                        'type': enemy_type,
                        'health': 10 * (1 + enemy_type.count('D') * 5),
                        'damage': 5 * (1 + enemy_type.count('o') + enemy_type.count('D') * 2)
                    })
        
        # Place items in rooms
        for x, y, w, h in rooms:
            if random.random() < 0.5:  # 50% chance of item in a room
                ix = random.randint(x + 1, x + w - 2)
                iy = random.randint(y + 1, y + h - 2)
                item_type = random.choice(['!', '$', '*'])  # potion, gold, weapon
                self.items.append({
                    'pos': [ix, iy],
                    'type': item_type
                })
        
        # Place exit in last room
        if rooms:
            x, y, w, h = rooms[-1]
            self.dungeon[y + h // 2][x + w // 2] = '>'
    
    def move_player(self, dx, dy):
        new_x = self.player_pos[0] + dx
        new_y = self.player_pos[1] + dy
        
        # Check boundaries
        if 0 <= new_x < self.width and 0 <= new_y < self.height:
            # Check if not a wall
            if self.dungeon[new_y][new_x] != '#':
                # Check for enemies
                enemy_at_pos = None
                for enemy in self.enemies:
                    if enemy['pos'] == [new_x, new_y]:
                        enemy_at_pos = enemy
                        break
                
                if enemy_at_pos:
                    # Combat
                    damage = random.randint(5, 10) + self.level
                    enemy_at_pos['health'] -= damage
                    self.score += 10
                    
                    if enemy_at_pos['health'] <= 0:
                        self.enemies.remove(enemy_at_pos)
                        self.exp += 20 * (1 + enemy_at_pos['type'].count('o') + enemy_at_pos['type'].count('D') * 3)
                        self.score += 50
                        self.player_pos = [new_x, new_y]
                        self.visited[new_y][new_x] = True
                    else:
                        # Enemy attacks back
                        self.health -= enemy_at_pos['damage']
                else:
                    # Move player
                    self.player_pos = [new_x, new_y]
                    self.visited[new_y][new_x] = True
                    
                    # Check for items
                    item_at_pos = None
                    for item in self.items:
                        if item['pos'] == [new_x, new_y]:
                            item_at_pos = item
                            break
                    
                    if item_at_pos:
                        self.collect_item(item_at_pos)
                    
                    # Check for exit
                    if self.dungeon[new_y][new_x] == '>':
                        self.next_level()
    
    def collect_item(self, item):
        if item['type'] == '!':  # Health potion
            self.health = min(self.max_health, self.health + 30)
            self.score += 20
        elif item['type'] == '$':  # Gold
            self.score += 50
        elif item['type'] == '*':  # Weapon upgrade
            self.score += 30
        
        self.items.remove(item)
    
    def next_level(self):
        self.level += 1
        self.exp_to_next = 100 * self.level
        self.max_health += 10
        self.health = self.max_health
        self.generate_dungeon()
    
    def update_enemies(self):
        for enemy in self.enemies:
            # Simple AI: move towards player if in line of sight
            if random.random() < 0.3:  # 30% chance to move each turn
                dx = 0
                dy = 0
                
                if enemy['pos'][0] < self.player_pos[0]:
                    dx = 1
                elif enemy['pos'][0] > self.player_pos[0]:
                    dx = -1
                
                if enemy['pos'][1] < self.player_pos[1]:
                    dy = 1
                elif enemy['pos'][1] > self.player_pos[1]:
                    dy = -1
                
                # Try to move
                new_x = enemy['pos'][0] + dx
                new_y = enemy['pos'][1] + dy
                
                if (0 <= new_x < self.width and 0 <= new_y < self.height and 
                    self.dungeon[new_y][new_x] != '#'):
                    
                    # Check if player is at new position
                    if [new_x, new_y] == self.player_pos:
                        self.health -= enemy['damage']
                    else:
                        enemy['pos'] = [new_x, new_y]
    
    def render(self):
        os.system('clear' if os.name == 'posix' else 'cls')
        
        # Create a copy of the dungeon for rendering
        render_dungeon = [row[:] for row in self.dungeon]
        
        # Add enemies
        for enemy in self.enemies:
            x, y = enemy['pos']
            if self.visited[y][x]:
                render_dungeon[y][x] = enemy['type']
        
        # Add items
        for item in self.items:
            x, y = item['pos']
            if self.visited[y][x]:
                render_dungeon[y][x] = item['type']
        
        # Add player
        if self.player_pos:
            x, y = self.player_pos
            render_dungeon[y][x] = '@'
        
        # Apply fog of war
        for y in range(self.height):
            for x in range(self.width):
                if not self.visited[y][x]:
                    render_dungeon[y][x] = ' '
        
        # Print dungeon
        for row in render_dungeon:
            print(''.join(row))
        
        # Print status
        print(f"Health: {self.health}/{self.max_health}  Level: {self.level}  Score: {self.score}  Exp: {self.exp}/{self.exp_to_next}")
        print("Controls: Arrow keys to move, Q to quit")
    
    def run(self):
        self.generate_dungeon()
        
        while self.health > 0:
            self.render()
            
            # Handle input
            key_pressed = False
            while not key_pressed:
                if keyboard.is_pressed('up'):
                    self.move_player(0, -1)
                    key_pressed = True
                elif keyboard.is_pressed('down'):
                    self.move_player(0, 1)
                    key_pressed = True
                elif keyboard.is_pressed('left'):
                    self.move_player(-1, 0)
                    key_pressed = True
                elif keyboard.is_pressed('right'):
                    self.move_player(1, 0)
                    key_pressed = True
                elif keyboard.is_pressed('q'):
                    print("Game over! Thanks for playing!")
                    return
                time.sleep(0.1)
            
            # Update enemies
            self.update_enemies()
            
            # Check level up
            if self.exp >= self.exp_to_next:
                self.level += 1
                self.exp_to_next = 100 * self.level
                self.max_health += 10
                self.health = self.max_health
        
        print(f"Game over! You reached level {self.level} with a score of {self.score}!")

if __name__ == "__main__":
    print("Dungeon Crawler - ASCII Roguelike")
    print("==================================")
    print("Symbols:")
    print("@ = You (the player)")
    print("# = Wall")
    print(". = Floor")
    print("> = Exit to next level")
    print("g = Goblin (weak enemy)")
    print("o = Orc (medium enemy)")
    print("D = Dragon (strong enemy)")
    print("! = Health potion")
    print("$ = Gold")
    print("* = Weapon upgrade")
    print("\nControls: Arrow keys to move, Q to quit")
    print("\nPress any key to start...")
    input()
    
    game = DungeonCrawler()
    game.run()
