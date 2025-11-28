import numpy as np
import pyaudio
import sys
import curses
from colorama import Fore, Back, Style, init
import time

# Initialize colorama for cross-platform color support
init()

# Audio settings
FORMAT = pyaudio.paFloat32
CHANNELS = 1
RATE = 44100
CHUNK = 1024

# ASCII art characters for different intensity levels
ASCII_CHARS = ' .:-=+*#%@'
BARS = ['░', '▒', '▓', '█']

class AudioVisualizer:
    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.stream = None
        self.running = False
        
    def start(self):
        """Initialize and start the audio stream"""
        try:
            self.stream = self.p.open(
                format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK
            )
            self.running = True
            return True
        except Exception as e:
            print(f"Error initializing audio: {e}")
            return False
    
    def stop(self):
        """Stop and clean up the audio stream"""
        self.running = False
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        self.p.terminate()
    
    def get_audio_data(self):
        """Get audio data from the stream"""
        if not self.stream:
            return None
        
        try:
            data = self.stream.read(CHUNK, exception_on_overflow=False)
            audio_data = np.frombuffer(data, dtype=np.float32)
            return audio_data
        except:
            return None
    
    def process_audio(self, audio_data):
        """Process audio data for visualization"""
        # Apply FFT to get frequency spectrum
        fft = np.fft.fft(audio_data)
        freq_bins = np.abs(fft[:len(fft)//2])
        
        # Normalize and smooth the data
        freq_bins = freq_bins / np.max(freq_bins + 1e-10)
        
        # Create frequency bands
        bands = np.array_split(freq_bins, 32)
        band_energies = [np.mean(band) for band in bands]
        
        return band_energies

def draw_ascii_visualizer(stdscr, energies):
    """Draw the ASCII visualizer using curses"""
    stdscr.clear()
    height, width = stdscr.getmaxyx()
    
    # Create color pairs if not already created
    if not hasattr(draw_ascii_visualizer, 'colors_initialized'):
        curses.start_color()
        curses.use_default_colors()
        for i in range(1, 8):
            curses.init_pair(i, i, -1)
        draw_ascii_visualizer.colors_initialized = True
    
    # Calculate bar dimensions
    bar_width = max(2, width // len(energies))
    max_bar_height = height - 4
    
    # Draw each frequency band
    for i, energy in enumerate(energies):
        bar_height = int(energy * max_bar_height)
        x = i * bar_width
        
        # Select color based on energy
        color_idx = min(6, int(energy * 7))
        
        # Draw the bar from bottom up
        for y in range(height - 2, height - 2 - bar_height, -1):
            if y >= 0:
                # Select character based on height
                char_idx = min(len(BARS) - 1, int((height - 2 - y) / max_bar_height * len(BARS)))
                char = BARS[char_idx]
                
                try:
                    stdscr.addch(y, x, char, curses.color_pair(color_idx))
                    if bar_width > 1:
                        stdscr.addch(y, x + 1, char, curses.color_pair(color_idx))
                except:
                    pass
    
    # Draw info text
    info_text = "🎵 Audio Visualizer - Press 'q' to quit"
    try:
        stdscr.addstr(0, 0, info_text, curses.A_BOLD)
        stdscr.addstr(height - 1, 0, f"Peak: {max(energies):.2f}", curses.A_DIM)
    except:
        pass
    
    stdscr.refresh()

def main():
    """Main function to run the visualizer"""
    print("🎵 Starting Audio Visualizer...")
    print("Make sure your microphone is enabled!")
    print("Press Ctrl+C to exit\n")
    
    visualizer = AudioVisualizer()
    
    if not visualizer.start():
        print("Failed to initialize audio. Exiting...")
        return
    
    try:
        # Initialize curses
        stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        stdscr.keypad(True)
        curses.curs_set(0)
        
        print("Visualizer started! Press 'q' to quit...")
        time.sleep(1)
        
        while visualizer.running:
            # Get and process audio data
            audio_data = visualizer.get_audio_data()
            if audio_data is not None:
                energies = visualizer.process_audio(audio_data)
                draw_ascii_visualizer(stdscr, energies)
            
            # Check for quit key
            try:
                key = stdscr.getch()
                if key == ord('q') or key == ord('Q'):
                    break
            except:
                pass
            
            time.sleep(0.05)  # Control refresh rate
    
    except KeyboardInterrupt:
        pass
    
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        # Clean up
        visualizer.stop()
        try:
            curses.endwin()
        except:
            pass
        print("\n👋 Visualizer stopped. Thanks for watching!")

if __name__ == "__main__":
    # Check required packages
    try:
        import pyaudio
        import numpy
        import colorama
        import curses
    except ImportError as e:
        print(f"Missing required package: {e}")
        print("Install with: pip install pyaudio numpy colorama")
        sys.exit(1)
    
    main()
