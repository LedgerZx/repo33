import turtle

def draw_triangle(t, x, y, size):
    """Draw a triangle with the given size at the specified position."""
    t.penup()
    t.goto(x, y)
    t.pendown()
    t.begin_fill()
    for _ in range(3):
        t.forward(size)
        t.left(120)
    t.end_fill()

def sierpinski(t, x, y, size, depth):
    """Recursively draw the Sierpinski Triangle."""
    if depth == 0:
        draw_triangle(t, x, y, size)
    else:
        sierpinski(t, x, y, size / 2, depth - 1)
        sierpinski(t, x - size / 2, y - size * (3 ** 0.5) / 6, size / 2, depth - 1)
        sierpinski(t, x + size / 2, y - size * (3 ** 0.5) / 6, size / 2, depth - 1)

def main():
    """Main function to set up the turtle and draw the Sierpinski Triangle."""
    screen = turtle.Screen()
    screen.bgcolor("white")

    t = turtle.Turtle()
    t.speed(0)  # Fastest speed

    # Set up the initial position and size
    x = 0
    y = 200
    size = 400
    depth = 5  # Adjust the depth for more or fewer iterations

    sierpinski(t, x, y, size, depth)

    turtle.done()

if __name__ == "__main__":
    main()
