import turtle

# Set up the screen
screen = turtle.Screen()
screen.bgcolor("white")

# Create a turtle object
tree = turtle.Turtle()
tree.speed(0)  # Fastest drawing speed
tree.color("brown", "green")
tree.left(90)
tree.penup()
tree.backward(100)
tree.pendown()

# Function to draw a branch
def draw_branch(branch_length, t):
    if branch_length > 5:
        t.forward(branch_length)
        t.right(20)
        draw_branch(branch_length - 15, t)
        t.left(40)
        draw_branch(branch_length - 15, t)
        t.right(20)
        t.backward(branch_length)

# Draw the tree
draw_branch(75, tree)

# Hide the turtle and display the window
tree.hideturtle()
screen.mainloop()
