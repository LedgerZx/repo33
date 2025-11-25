import numpy as np
import pyaudio
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque

class AudioVisualizer:
    def __init__(self):
        # Audio parameters
        self.FORMAT = pyaudio.paFloat32
        self.CHANNELS = 1
        self.RATE = 44100
        self.CHUNK = 1024
        self.BARS = 50
        
        # Initialize audio stream
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.CHUNK
        )
        
        # Frequency bins for visualization
        self.freq_bins = np.fft.fftfreq(self.CHUNK, 1/self.RATE)[:self.CHUNK//2]
        self.bar_indices = np.linspace(0, len(self.freq_bins)-1, self.BARS, dtype=int)
        
        # Visualization setup
        self.fig, self.ax = plt.subplots(figsize=(12, 6))
        self.fig.patch.set_facecolor('#0a0a0a')
        self.ax.set_facecolor('#0a0a0a')
        
        # Create bars with gradient colors
        self.bars = self.ax.bar(
            range(self.BARS),
            np.zeros(self.BARS),
            color=plt.cm.plasma(np.linspace(0.3, 0.9, self.BARS)),
            edgecolor='none',
            alpha=0.9
        )
        
        # Styling
        self.ax.set_xlim(-0.5, self.BARS-0.5)
        self.ax.set_ylim(0, 1)
        self.ax.set_title('🎵 Real-Time Audio Visualizer 🎵', 
                         color='white', fontsize=16, pad=20)
        self.ax.set_xlabel('Frequency Bands', color='white', fontsize=10)
        self.ax.set_ylabel('Amplitude', color='white', fontsize=10)
        self.ax.tick_params(colors='white')
        for spine in self.ax.spines.values():
            spine.set_visible(False)
        
        # Smooth amplitude history
        self.amplitude_history = deque(maxlen=5)
        
    def get_audio_data(self):
        """Read audio data from microphone and compute FFT"""
        try:
            data = self.stream.read(self.CHUNK, exception_on_overflow=False)
            data = np.frombuffer(data, dtype=np.float32)
            
            # Apply window function to reduce spectral leakage
            window = np.hanning(len(data))
            windowed_data = data * window
            
            # Compute FFT
            fft_data = np.fft.fft(windowed_data)
            magnitude = np.abs(fft_data[:len(fft_data)//2])
            
            # Normalize and log scale
            magnitude = np.log1p(magnitude)
            magnitude = magnitude / np.max(magnitude + 1e-10)
            
            # Resample to bar count
            bar_data = magnitude[self.bar_indices]
            
            return bar_data
            
        except Exception as e:
            print(f"Audio error: {e}")
            return np.zeros(self.BARS)
    
    def update(self, frame):
        """Update visualization with new audio data"""
        data = self.get_audio_data()
        
        # Add smoothing
        self.amplitude_history.append(data)
        if len(self.amplitude_history) > 0:
            smoothed_data = np.mean(self.amplitude_history, axis=0)
        else:
            smoothed_data = data
        
        # Update bars with smooth animation
        for bar, height in zip(self.bars, smoothed_data):
            bar.set_height(height)
            
            # Dynamic color intensity based on amplitude
            intensity = min(1.0, height * 1.5)
            bar.set_alpha(0.3 + intensity * 0.7)
        
        # Dynamic y-axis scaling
        max_amp = np.max(smoothed_data)
        if max_amp > 0.1:
            self.ax.set_ylim(0, max_amp * 1.2)
        
        return self.bars
    
    def start(self):
        """Start the visualization"""
        print("🎤 Audio Visualizer Started!")
        print("🔊 Make some noise to see the visualization!")
        print("🛑 Close the window to stop")
        
        # Create animation
        self.ani = animation.FuncAnimation(
            self.fig, self.update, interval=30, blit=True, cache_frame_data=False
        )
        
        plt.tight_layout()
        plt.show()
    
    def cleanup(self):
        """Clean up resources"""
        if hasattr(self, 'stream'):
            self.stream.stop_stream()
            self.stream.close()
        if hasattr(self, 'audio'):
            self.audio.terminate()

def main():
    visualizer = AudioVisualizer()
    try:
        visualizer.start()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    finally:
        visualizer.cleanup()

if __name__ == "__main__":
    main()
