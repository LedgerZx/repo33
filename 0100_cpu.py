#!/usr/bin/env python3
import time
import psutil
import random
import math
from collections import deque

class CPUMonitor:
    def __init__(self, width=60, height=20):
        self.width = width
        self.height = height
        self.history = deque(maxlen=width)
        self.chars = " .:-=+*#%@"
        self.colors = {
            'cpu': '\033[91m',    # Red
            'mem': '\033[94m',    # Blue
            'disk': '\033[93m',   # Yellow
            'net': '\033[92m',    # Green
            'reset': '\033[0m'
        }
        
    def get_system_stats(self):
        cpu = psutil.cpu_percent(interval=0.1)
        mem = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent
        net_sent = psutil.net_io_counters().bytes_sent
        net_recv = psutil.net_io_counters().bytes_recv
        return cpu, mem, disk, net_sent, net_recv
    
    def create_bar(self, value, width, char='█'):
        filled = int(value * width / 100)
        empty = width - filled
        return char * filled + ' ' * empty
    
    def create_wave(self, frame):
        wave = []
        for x in range(self.width):
            y = int(math.sin(x * 0.2 + frame * 0.1) * 5 + self.height // 2)
            if 0 <= y < self.height:
                wave.append((x, y))
        return wave
    
    def render(self):
        cpu, mem, disk, net_sent, net_recv = self.get_system_stats()
        self.history.append(cpu)
        
        # Clear screen
        print('\033[2J\033[H', end='')
        
        # Header
        print(f"{self.colors['cpu']}╔{'═' * (self.width - 2)}╗{self.colors['reset']}")
        print(f"{self.colors['cpu']}║{'SYSTEM MONITOR':^^{self.width - 2}}║{self.colors['reset']}")
        print(f"{self.colors['cpu']}╚{'═' * (self.width - 2)}╝{self.colors['reset']}\n")
        
        # CPU graph
        print(f"{self.colors['cpu']}CPU: {cpu:5.1f}%{self.colors['reset']}")
        for y in range(self.height - 3, -1, -1):
            line = ""
            for x, val in enumerate(self.history):
                threshold = (y + 1) * 100 / (self.height - 2)
                if val >= threshold:
                    idx = min(int(val / 10), len(self.chars) - 1)
                    line += self.colors['cpu'] + self.chars[idx] + self.colors['reset']
                else:
                    line += " "
            print(line)
        
        # Resource bars
        print(f"\n{self.colors['mem']}MEM: {mem:5.1f}% [{self.create_bar(mem, 30)}]{self.colors['reset']}")
        print(f"{self.colors['disk']}DSK: {disk:5.1f}% [{self.create_bar(disk, 30)}]{self.colors['reset']}")
        print(f"{self.colors['net']}NET: ↑{net_sent/1024/1024:6.1f}MB ↓{net_recv/1024/1024:6.1f}MB{self.colors['reset']}")
        
        # Animated wave effect
        frame = time.time() * 2
        wave = self.create_wave(frame)
        print("\n" + " " * (self.width // 2 - 10) + "╔" + "═" * 20 + "╗")
        print(" " * (self.width // 2 - 10) + "║" + "WAVE VISUALIZER".center(20) + "║")
        print(" " * (self.width // 2 - 10) + "╚" + "═" * 20 + "╗")
        for y in range(5):
            line = " " * (self.width // 2 - 10) + "║"
            for x in range(20):
                if (x, y) in wave:
                    line += self.colors['net'] + '~' + self.colors['reset']
                else:
                    line += " "
            line += "║"
            print(line)
        print(" " * (self.width // 2 - 10) + "╚" + "═" * 20 + "╝")
        
        # Random stats
        print(f"\n{'=' * self.width}")
        print(f"Processes: {len(psutil.pids())}")
        print(f"Boot time: {time.ctime(psutil.boot_time())}")
        print(f"Uptime: {time.time() - psutil.boot_time():.0f} seconds")
        print(f"{'=' * self.width}")

def main():
    monitor = CPUMonitor()
    try:
        while True:
            monitor.render()
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\nMonitoring stopped. Goodbye!")

if __name__ == "__main__":
    main()
