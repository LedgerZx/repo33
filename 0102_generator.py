import time
import random
from math import log, sqrt
from typing import Generator, Tuple

def mandelbrot_generator(c: complex, max_iter: int = 100) -> Generator[Tuple[int, complex], None, int]:
    """
    Generator that yields each iteration of the Mandelbrot calculation.
    Returns the final iteration count when exhausted.
    """
    z = 0
    for n in range(max_iter):
        if abs(z) > 2:
            return n
        yield n, z
        z = z*z + c
    return max_iter

def pixel_generator(width: int, height: int, 
                   xmin: float, xmax: float, 
                   ymin: float, ymax: float) -> Generator[Tuple[int, int, complex], None, None]:
    """
    Generator that yields pixel coordinates and their corresponding complex numbers.
    """
    for y in range(height):
        for x in range(width):
            real = xmin + (x / width) * (xmax - xmin)
            imag = ymin + (y / height) * (ymax - ymin)
            yield x, y, complex(real, imag)

def color_generator(iterations: int, max_iter: int) -> Tuple[int, int, int]:
    """
    Generates colors based on iteration count.
    """
    if iterations == max_iter:
        return (0, 0, 0)
    
    # Smooth coloring algorithm
    smooth = iterations + 1 - log(log(sqrt(2)), 2)
    hue = int(smooth * 137.5) % 360  # Golden angle for nice color distribution
    saturation = 100
    value = 100 if iterations < max_iter else 0
    
    # HSV to RGB conversion
    c = value * saturation / 100
    x = c * (1 - abs((hue / 60) % 2 - 1))
    m = value - c
    
    if hue < 60:
        r, g, b = c, x, 0
    elif hue < 120:
        r, g, b = x, c, 0
    elif hue < 180:
        r, g, b = 0, c, x
    elif hue < 240:
        r, g, b = 0, x, c
    elif hue < 300:
        r, g, b = x, 0, c
    else:
        r, g, b = c, 0, x
    
    return (int((r + m) * 255), int((g + m) * 255), int((b + m) * 255))

def render_mandelbrot(width: int, height: int, 
                      xmin: float, xmax: float, 
                      ymin: float, ymax: float,
                      max_iter: int = 100) -> None:
    """
    Renders the Mandelbrot set using generator functions.
    """
    print(f"Rendering Mandelbrot set ({width}x{height})...")
    start_time = time.time()
    
    # Create a simple ASCII representation
    chars = " .:-=+*#%@"
    output = []
    
    for x, y, c in pixel_generator(width, height, xmin, xmax, ymin, ymax):
        gen = mandelbrot_generator(c, max_iter)
        iterations = -1
        
        # Consume the generator to get the final iteration count
        for iterations, _ in gen:
            pass
        
        if iterations == -1:
            iterations = max_iter
        
        # Map iterations to character
        char_idx = min(int(iterations * len(chars) / max_iter), len(chars) - 1)
        output.append(chars[char_idx])
        
        # Add newline at end of row
        if x == width - 1:
            output.append('\n')
    
    print(''.join(output))
    print(f"Rendered in {time.time() - start_time:.2f} seconds")

def zoom_generator(center_x: float, center_y: float, 
                  initial_scale: float, zoom_factor: float = 0.5) -> Generator[Tuple[float, float, float, float], None, None]:
    """
    Generator that yields progressively zoomed-in viewports.
    """
    scale = initial_scale
    while True:
        yield (center_x - scale, center_x + scale, 
               center_y - scale, center_y + scale)
        scale *= zoom_factor

def interesting_points_generator() -> Generator[Tuple[float, float, str], None, None]:
    """
    Generator that yields interesting points in the Mandelbrot set.
    """
    points = [
        (-0.7269, 0.1889, "Spiral"),
        (-0.8, 0.156, "Seahorse Valley"),
        (-0.7533, 0.1138, "Elephant Valley"),
        (-0.161, 1.0407, "Mini Mandelbrot"),
        (-1.25066, 0.02012, "Triple Spiral"),
        (-0.748, 0.1, "Lightning"),
    ]
    
    while True:
        yield random.choice(points)

def main():
    print("Mandelbrot Set Explorer")
    print("=======================")
    
    # Initial parameters
    width, height = 80, 40
    xmin, xmax = -2.5, 1.5
    ymin, ymax = -2, 2
    
    # Render initial view
    render_mandelbrot(width, height, xmin, xmax, ymin, ymax, max_iter=50)
    
    # Interactive exploration
    print("\nExploring interesting points...")
    points_gen = interesting_points_generator()
    
    for i in range(3):
        x, y, name = next(points_gen)
        print(f"\nZooming into {name} at ({x:.4f}, {y:.4f})")
        
        zoom_gen = zoom_generator(x, y, 0.5)
        for j in range(3):
            xmin, xmax, ymin, ymax = next(zoom_gen)
            render_mandelbrot(width, height, xmin, xmax, ymin, ymax, max_iter=100)
            time.sleep(0.5)
    
    print("\nExploration complete!")

if __name__ == "__main__":
    main()
