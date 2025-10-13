import turtle
import math

def draw_hexagon(turtle, side_length):
    for _ in range(6):
        turtle.forward(side_length)
        turtle.right(60)

def draw_hexagonal_grid(turtle, side_length, rows, cols):
    for row in range(rows):
        for col in range(cols):
            x = col * (side_length * 2) - (cols * side_length)
            y = row * (side_length * math.sqrt(3)) - (rows * side_length * math.sqrt(3) / 2)
            turtle.up()
            turtle.goto(x, y)
            turtle.down()
            draw_hexagon(turtle, side_length)
            turtle.up()
            turtle.goto(x + side_length, y)
            turtle.down()

def main():
    side_length = 50
    rows = 5
    cols = 5
    my_turtle = turtle.Turtle()
    my_win = turtle.Screen()
    my_turtle.speed(0)
    draw_hexagonal_grid(my_turtle, side_length, rows, cols)
    my_win.exitonclick()

if __name__ == "__main__":
    main()
