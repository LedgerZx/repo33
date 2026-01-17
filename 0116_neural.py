import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import time

class NeuralArtGenerator:
    def __init__(self, img_size=256):
        self.img_size = img_size
        self.model = None
        self.current_image = None
        self.iteration = 0
        self.color_mode = 'vibrant'
        
        # Create coordinate grids for spatial features
        x = np.linspace(-1, 1, img_size)
        y = np.linspace(-1, 1, img_size)
        self.X, self.Y = np.meshgrid(x, y)
        
        # Initialize the neural network
        self.build_model()
        
    def build_model(self):
        """Build a neural network that generates images from coordinate inputs"""
        # Input layer for coordinates
        input_coords = layers.Input(shape=(2,))
        
        # Create a deep network with periodic activations for interesting patterns
        x = input_coords
        
        # Add several layers with different activation functions
        for i in range(8):
            # Vary the number of neurons per layer
            units = 32 if i % 2 == 0 else 16
            
            # Add dense layer
            x = layers.Dense(units)(x)
            
            # Apply different activation functions based on layer
            if i % 3 == 0:
                x = layers.Activation(tf.math.sin)(x)  # Periodic activation
            elif i % 3 == 1:
                x = layers.Activation(tf.nn.relu)(x)  # ReLU
            else:
                x = layers.Activation(tf.nn.tanh)(x)  # Tanh
            
            # Add some noise for randomness
            x = layers.GaussianNoise(0.05)(x)
        
        # Output layer with 3 channels (RGB)
        outputs = layers.Dense(3, activation='sigmoid')(x)
        
        # Create the model
        self.model = keras.Model(inputs=input_coords, outputs=outputs)
        
        # Initialize with random weights
        self.initialize_weights()
    
    def initialize_weights(self):
        """Initialize model weights with random values"""
        for layer in self.model.layers:
            if hasattr(layer, 'kernel_initializer'):
                layer.kernel_initializer = tf.keras.initializers.RandomNormal(mean=0.0, stddev=0.5)
                layer.build(layer.input_shape)
    
    def generate_image(self, zoom=1.0, offset_x=0.0, offset_y=0.0, rotation=0.0):
        """Generate an image using the neural network"""
        # Prepare coordinate inputs
        coords = np.stack([
            (self.X.flatten() * zoom + offset_x) * np.cos(rotation) - 
            (self.Y.flatten() * zoom + offset_y) * np.sin(rotation),
            (self.X.flatten() * zoom + offset_x) * np.sin(rotation) + 
            (self.Y.flatten() * zoom + offset_y) * np.cos(rotation)
        ], axis=-1)
        
        # Generate predictions
        preds = self.model.predict(coords, verbose=0)
        
        # Reshape to image format
        img = preds.reshape(self.img_size, self.img_size, 3)
        
        # Apply color mode
        if self.color_mode == 'vibrant':
            # Enhance color saturation
            img = np.power(img, 0.6)
        elif self.color_mode == 'pastel':
            # Soften colors
            img = np.power(img, 1.5)
        elif self.color_mode == 'grayscale':
            # Convert to grayscale
            gray = np.mean(img, axis=2, keepdims=True)
            img = np.concatenate([gray, gray, gray], axis=2)
        
        return img
    
    def evolve_network(self, mutation_rate=0.1):
        """Randomly mutate the network weights to evolve the art"""
        for layer in self.model.layers:
            if hasattr(layer, 'kernel'):
                # Get current weights
                weights = layer.get_weights()
                
                # Apply mutations
                new_weights = []
                for w in weights:
                    # Random mutations
                    mutations = np.random.normal(0, mutation_rate, w.shape)
                    new_w = w + mutations
                    
                    # Ensure weights stay in reasonable range
                    new_w = np.clip(new_w, -2, 2)
                    new_weights.append(new_w)
                
                # Set mutated weights
                layer.set_weights(new_weights)
    
    def setup_interactive_plot(self):
        """Setup an interactive plot with controls"""
        # Create figure
        self.fig, (self.ax, self.control_ax) = plt.subplots(1, 2, figsize=(14, 7), 
                                                             gridspec_kw={'width_ratios': [3, 1]})
        
        # Initial image
        self.current_image = self.generate_image()
        self.im = self.ax.imshow(self.current_image)
        self.ax.set_title('Neural Network Art Generator')
        self.ax.axis('off')
        
        # Add controls
        self.add_controls()
        
        # Connect event handlers
        self.fig.canvas.mpl_connect('key_press_event', self.on_key)
        
        plt.tight_layout()
    
    def add_controls(self):
        """Add interactive controls to the plot"""
        # Clear control axis
        self.control_ax.clear()
        self.control_ax.axis('off')
        
        # Title for controls
        self.control_ax.text(0.5, 0.95, 'Controls', ha='center', fontsize=14, weight='bold')
        
        # Instructions
        instructions = [
            "Press 'e' to evolve",
            "Press 'r' to reset",
            "Press 's' to save image",
            "Press 'c' to change color mode",
            "Use arrow keys to pan",
            "Use +/- to zoom"
        ]
        
        for i, instruction in enumerate(instructions):
            self.control_ax.text(0.5, 0.85 - i*0.08, instruction, ha='center')
        
        # Status info
        self.status_text = self.control_ax.text(0.5, 0.15, f"Iteration: {self.iteration}", 
                                                ha='center')
        self.color_text = self.control_ax.text(0.5, 0.05, f"Color Mode: {self.color_mode}", 
                                              ha='center')
    
    def on_key(self, event):
        """Handle keyboard events"""
        if event.key == 'e':
            # Evolve the network
            self.evolve_network()
            self.iteration += 1
            self.update_image()
            self.status_text.set_text(f"Iteration: {self.iteration}")
            self.fig.canvas.draw()
        elif event.key == 'r':
            # Reset the network
            self.initialize_weights()
            self.iteration = 0
            self.update_image()
            self.status_text.set_text(f"Iteration: {self.iteration}")
            self.fig.canvas.draw()
        elif event.key == 's':
            # Save the current image
            timestamp = int(time.time())
            plt.imsave(f'neural_art_{timestamp}.png', self.current_image)
            print(f"Image saved as neural_art_{timestamp}.png")
        elif event.key == 'c':
            # Change color mode
            modes = ['vibrant', 'pastel', 'grayscale']
            current_idx = modes.index(self.color_mode)
            self.color_mode = modes[(current_idx + 1) % len(modes)]
            self.color_text.set_text(f"Color Mode: {self.color_mode}")
            self.update_image()
            self.fig.canvas.draw()
        elif event.key == 'right':
            # Pan right
            self.update_image(offset_x=0.1)
            self.fig.canvas.draw()
        elif event.key == 'left':
            # Pan left
            self.update_image(offset_x=-0.1)
            self.fig.canvas.draw()
        elif event.key == 'up':
            # Pan up
            self.update_image(offset_y=-0.1)
            self.fig.canvas.draw()
        elif event.key == 'down':
            # Pan down
            self.update_image(offset_y=0.1)
            self.fig.canvas.draw()
        elif event.key == '+' or event.key == '=':
            # Zoom in
            self.update_image(zoom=0.8)
            self.fig.canvas.draw()
        elif event.key == '-':
            # Zoom out
            self.update_image(zoom=1.2)
            self.fig.canvas.draw()
    
    def update_image(self, zoom=1.0, offset_x=0.0, offset_y=0.0, rotation=0.0):
        """Update the current image with new parameters"""
        self.current_image = self.generate_image(zoom, offset_x, offset_y, rotation)
        self.im.set_data(self.current_image)
    
    def run(self):
        """Run the interactive neural art generator"""
        self.setup_interactive_plot()
        plt.show()

if __name__ == "__main__":
    # Create and run the neural art generator
    art_gen = NeuralArtGenerator(img_size=256)
    art_gen.run()
