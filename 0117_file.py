#!/usr/bin/env python3
import os
import sys
import argparse
from pathlib import Path
from collections import defaultdict
import time
from datetime import datetime

class FileSystemVisualizer:
    def __init__(self, path=".", max_depth=3, min_size_kb=100):
        self.path = Path(path)
        self.max_depth = max_depth
        self.min_size_kb = min_size_kb
        self.file_sizes = defaultdict(int)
        self.dir_sizes = defaultdict(int)
        self.total_size = 0
        self.colors = {
            'reset': '\033[0m',
            'red': '\033[91m',
            'green': '\033[92m',
            'yellow': '\033[93m',
            'blue': '\033[94m',
            'magenta': '\033[95m',
            'cyan': '\033[96m',
            'white': '\033[97m',
            'bold': '\033[1m'
        }
    
    def format_size(self, size_bytes):
        """Convert bytes to human readable format"""
        if size_bytes == 0:
            return "0B"
        units = ['B', 'KB', 'MB', 'GB', 'TB']
        i = 0
        while size_bytes >= 1024 and i < len(units)-1:
            size_bytes /= 1024.0
            i += 1
        return f"{size_bytes:.2f}{units[i]}"
    
    def get_color_for_size(self, size_bytes):
        """Return color based on file size"""
        if size_bytes < 1024 * 100:  # < 100KB
            return self.colors['green']
        elif size_bytes < 1024 * 1024:  # < 1MB
            return self.colors['yellow']
        elif size_bytes < 1024 * 1024 * 100:  # < 100MB
            return self.colors['blue']
        elif size_bytes < 1024 * 1024 * 1024:  # < 1GB
            return self.colors['magenta']
        else:  # >= 1GB
            return self.colors['red']
    
    def scan_directory(self, path, depth=0):
        """Recursively scan directory and collect file sizes"""
        if depth > self.max_depth:
            return
        
        try:
            for item in path.iterdir():
                if item.is_file():
                    try:
                        size = item.stat().st_size
                        self.file_sizes[str(item)] = size
                        self.total_size += size
                        
                        # Update parent directory sizes
                        parent = str(item.parent)
                        while parent != str(self.path.parent):
                            self.dir_sizes[parent] += size
                            parent = str(Path(parent).parent)
                    except (OSError, PermissionError):
                        pass
                elif item.is_dir():
                    self.scan_directory(item, depth + 1)
        except (OSError, PermissionError):
            pass
    
    def generate_tree(self):
        """Generate a visual tree representation of the directory structure"""
        tree = []
        tree.append(f"{self.colors['bold']}{self.colors['cyan']}File System Visualization{self.colors['reset']}")
        tree.append(f"{self.colors['bold']}Path: {self.path}{self.colors['reset']}")
        tree.append(f"{self.colors['bold']}Total Size: {self.format_size(self.total_size)}{self.colors['reset']}")
        tree.append(f"{self.colors['bold']}Scan Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{self.colors['reset']}")
        tree.append("-" * 80)
        
        # Sort directories by size
        sorted_dirs = sorted(self.dir_sizes.items(), key=lambda x: x[1], reverse=True)
        
        for dir_path, size in sorted_dirs[:10]:  # Top 10 directories
            rel_path = os.path.relpath(dir_path, self.path)
            depth = rel_path.count(os.sep)
            indent = "  " * depth
            color = self.get_color_for_size(size)
            tree.append(f"{indent}📁 {color}{rel_path}{self.colors['reset']} - {self.format_size(size)}")
        
        tree.append("-" * 80)
        
        # Sort files by size
        sorted_files = sorted(self.file_sizes.items(), key=lambda x: x[1], reverse=True)
        
        for file_path, size in sorted_files[:10]:  # Top 10 files
            rel_path = os.path.relpath(file_path, self.path)
            depth = rel_path.count(os.sep)
            indent = "  " * depth
            color = self.get_color_for_size(size)
            file_name = os.path.basename(file_path)
            tree.append(f"{indent}📄 {color}{file_name}{self.colors['reset']} - {self.format_size(size)}")
        
        return "\n".join(tree)
    
    def run(self):
        """Run the visualization"""
        print(f"{self.colors['bold']}Scanning directory: {self.path}{self.colors['reset']}")
        start_time = time.time()
        self.scan_directory(self.path)
        scan_time = time.time() - start_time
        print(f"{self.colors['bold']}Scan completed in {scan_time:.2f} seconds{self.colors['reset']}")
        print("\n")
        print(self.generate_tree())

def main():
    parser = argparse.ArgumentParser(description="Visualize file system usage")
    parser.add_argument("path", nargs="?", default=".", help="Path to directory (default: current directory)")
    parser.add_argument("--depth", type=int, default=3, help="Maximum scan depth (default: 3)")
    parser.add_argument("--min-size", type=int, default=100, help="Minimum file size in KB to display (default: 100)")
    
    args = parser.parse_args()
    
    visualizer = FileSystemVisualizer(args.path, args.depth, args.min_size)
    visualizer.run()

if __name__ == "__main__":
    main()
