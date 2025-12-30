import time
import random
import shutil
import os
from datetime import datetime

class MatrixClock:
    def __init__(self):
        self.width, self.height = shutil.get_terminal_size()
        self.matrix_chars = 'ｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓﾔﾕﾖﾗﾘﾙﾚﾛﾜﾝ01'
        self.rain_drops = []
        self.clock_display = []
        self.last_time = ""
        
        # Initialize rain drops
        for _ in range(self.width // 2):
            self.rain_drops.append({
                'x': random.randint(0, self.width - 1),
                'y': random.randint(-self.height, 0),
                'speed': random.uniform(0.1, 0.5),
                'length': random.randint(5, 15)
            })
    
    def get_ascii_time(self):
        """Convert current time to ASCII art"""
        now = datetime.now().strftime("%H:%M:%S")
        
        if now == self.last_time:
            return self.clock_display
        
        self.last_time = now
        self.clock_display = []
        
        # ASCII numbers (simplified 5x7 font)
        numbers = {
            '0': ['  █  ', ' █ █ ', '█   █', '█   █', '█   █', ' █ █ ', '  █  '],
            '1': ['  █  ', ' ██  ', '  █  ', '  █  ', '  █  ', '  █  ', ' ████'],
            '2': [' ███ ', '█   █', '    █', '   █ ', '  █  ', ' █   ', '█████'],
            '3': ['████ ', '    █', '   █ ', '  █  ', '    █', '█   █', ' ███ '],
            '4': ['   █ ', '  ██ ', ' █ █ ', '█  █ ', '█████', '   █ ', '   █ '],
            '5': ['█████', '█    ', '████ ', '    █', '    █', '█   █', ' ███ '],
            '6': [' ███ ', '█   █', '█    ', '████ ', '█   █', '█   █', ' ███ '],
            '7': ['█████', '    █', '   █ ', '  █  ', ' █   ', '█    ', '█    '],
            '8': [' ███ ', '█   █', '█   █', ' ███ ', '█   █', '█   █', ' ███ '],
            '9': [' ███ ', '█   █', '█   █', ' ████', '    █', '   █ ', ' ███ '],
            ':': ['     ', '  █  ', '  █  ', '     ', '  █  ', '  █  ', '     ']
        }
        
        for digit in now:
            self.clock_display.append(numbers[digit])
        
        return self.clock_display
    
    def update_rain(self):
        """Update matrix rain positions"""
        for drop in self.rain_drops:
            drop['y'] += drop['speed']
            
            if drop['y'] > self.height + drop['length']:
                drop['y'] = -drop['length']
                drop['x'] = random.randint(0, self.width - 1)
                drop['speed'] = random.uniform(0.1, 0.5)
                drop['length'] = random.randint(5, 15)
    
    def render_frame(self):
        """Render the complete frame"""
        # Clear screen
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Create buffer
        buffer = [[' ' for _ in range(self.width)] for _ in range(self.height)]
        
        # Draw matrix rain
        for drop in self.rain_drops:
            for i in range(drop['length']):
                y = int(drop['y'] - i)
                if 0 <= y < self.height and 0 <= drop['x'] < self.width:
                    char = random.choice(self.matrix_chars)
                    if i == 0:
                        buffer[y][drop['x']] = '\033[1;37m' + char + '\033[0m'  # White for head
                    elif i < 3:
                        buffer[y][drop['x']] = '\033[1;32m' + char + '\033[0m'  # Bright green
                    else:
                        buffer[y][drop['x']] = '\033[0;32m' + char + '\033[0m'  # Dim green
        
        # Draw clock
        ascii_time = self.get_ascii_time()
        clock_width = len(ascii_time) * 6
        clock_start_x = (self.width - clock_width) // 2
        clock_start_y = self.height // 2 - 4
        
        for col_idx, column in enumerate(ascii_time):
            for row_idx, line in enumerate(column):
                x = clock_start_x + col_idx * 6
                y = clock_start_y + row_idx
                
                if 0 <= y < self.height and 0 <= x < self.width:
                    for char_x, char in enumerate(line):
                        if char == '█' and x + char_x < self.width:
                            # Create glow effect
                            buffer[y][x + char_x] = '\033[1;33;40m' + char + '\033[0m'
        
        # Render buffer to screen
        for row in buffer:
            print(''.join(row))
        
        # Add info text
        info_text = f"Matrix Clock - {datetime.now().strftime('%Y-%m-%d')} | Press Ctrl+C to exit"
        print(f"\033[1;36m{info_text.center(self.width)}\033[0m")
    
    def run(self):
        """Main loop"""
        try:
            while True:
                self.update_rain()
                self.render_frame()
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\n\033[1;32mMatrix Clock terminated. Stay in the matrix.\033[0m")

if __name__ == "__main__":
    clock = MatrixClock()
    clock.run()
