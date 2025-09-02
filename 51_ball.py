import curses
import time
import random

# Initialize the screen
stdscr = curses.initscr()
curses.curs_set(0)  # Hide the cursor
sh, sw = stdscr.getmaxyx()  # Get screen dimensions
w = curses.newwin(sh, sw, 0, 0)  # Create a new window

# Ball properties
ball_x = sw // 2
ball_y = sh // 2
ball_dx = 1
ball_dy = 1

# Game loop
try:
    while True:
        # Clear the screen
        w.clear()

        # Draw the ball
        w.addch(ball_y, ball_x, 'O')

        # Update ball position
        ball_x += ball_dx
        ball_y += ball_dy

        # Check for collisions with walls
        if ball_x <= 0 or ball_x >= sw - 1:
            ball_dx = -ball_dx
        if ball_y <= 0 or ball_y >= sh - 1:
            ball_dy = -ball_dy

        # Refresh the screen
        w.refresh()

        # Control the speed of the animation
        time.sleep(0.05)

except KeyboardInterrupt:
    pass

finally:
    # Restore the terminal to its original state
    curses.endwin()
