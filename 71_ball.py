import curses
import time
import random

# Initialize the screen
stdscr = curses.initscr()
curses.curs_set(0)  # Hide the cursor
height, width = stdscr.getmaxyx()

# Set up the initial position and velocity of the ball
ball_y, ball_x = height // 2, width // 2
velocity_y, velocity_x = 1, 1

# Define the ball character
ball_char = 'O'

# Define the delay between frames
delay = 0.1

try:
    while True:
        # Clear the screen
        stdscr.clear()

        # Update the ball's position
        ball_y += velocity_y
        ball_x += velocity_x

        # Check for collisions with the walls
        if ball_y <= 0 or ball_y >= height - 1:
            velocity_y = -velocity_y
        if ball_x <= 0 or ball_x >= width - 1:
            velocity_x = -velocity_x

        # Draw the ball
        stdscr.addch(ball_y, ball_x, ball_char)

        # Refresh the screen
        stdscr.refresh()

        # Wait for the specified delay
        time.sleep(delay)

except KeyboardInterrupt:
    # Exit gracefully on keyboard interrupt
    pass

finally:
    # Restore the terminal to its original state
    curses.endwin()
