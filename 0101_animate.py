import numpy as np
import pyaudio
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque

# Audio settings
FORMAT = pyaudio.paFloat32
CHANNELS = 1
RATE = 44100
CHUNK = 1024
BAR_COUNT = 50

# Initialize audio stream
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

# Setup the plot
fig, ax = plt.subplots(figsize=(12, 6))
fig.patch.set_facecolor('#0a0a0a')
ax.set_facecolor('#0a0a0a')

# Create bars
x = np.arange(BAR_COUNT)
bars = ax.bar(x, np.zeros(BAR_COUNT), color='#00ff00', width=0.8)
ax.set_ylim(0, 1)
ax.set_xlim(0, BAR_COUNT)
ax.set_axis_off()

# Smooth the data
smooth_data = deque(maxlen=5)

# Animation function
def animate(frame):
    try:
        # Read audio data
        data = np.frombuffer(stream.read(CHUNK), dtype=np.float32)
        
        # Apply window function to reduce spectral leakage
        windowed = data * np.hanning(len(data))
        
        # Compute FFT
        fft = np.fft.fft(windowed)
        freq = np.abs(fft[:len(fft)//2])
        
        # Normalize and log scale
        freq = np.log10(freq + 1)
        freq = freq / np.max(freq) if np.max(freq) > 0 else freq
        
        # Downsample to bar count
        step = len(freq) // BAR_COUNT
        bar_data = np.array([np.mean(freq[i:i+step]) for i in range(0, len(freq), step)][:BAR_COUNT])
        
        # Smooth the data
        smooth_data.append(bar_data)
        smoothed = np.mean(smooth_data, axis=0)
        
        # Update bars
        for bar, height in zip(bars, smoothed):
            bar.set_height(height)
            
            # Color based on frequency
            if height > 0.7:
                bar.set_color('#ff0066')  # Pink for high
            elif height > 0.4:
                bar.set_color('#00ff66')  # Cyan for mid
            else:
                bar.set_color('#0066ff')  # Blue for low
                
    except Exception as e:
        pass
    
    return bars

# Create animation
anim = animation.FuncAnimation(fig, animate, interval=20, blit=True)

plt.tight_layout()
plt.show()

# Cleanup
stream.stop_stream()
stream.close()
p.terminate()
