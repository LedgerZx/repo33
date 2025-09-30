import curses
import random
import time

# Initialize the screen
stdscr = curses.initscr()
curses.curs_set(0)
sh, sw = stdscr.getmaxyx()
w = curses.newwin(sh, sw, 0, 0)
w.keypad(1)
w.timeout(100)

# Ball properties
ball_x = sw // 2
ball_y = sh // 2
ball_dx = 1
ball_dy = 1

# Main loop
while True:
    w.clear()

    # Draw the ball
    w.addch(ball_y, ball_x, 'O')

    # Update ball position
    ball_x += ball_dx
    ball_y += ball_dy

    # Check for wall collisions
    if ball_x <= 0 or ball_x >= sw - 1:
        ball_dx = -ball_dx
    if ball_y <= 0 or ball_y >= sh - 1:
        ball_dy = -ball_dy

    # Refresh the screen
    w.refresh()
    time.sleep(0.05)

    # Check for user input to exit
    key = w.getch()
    if key == ord('q'):
        break

# Clean up
curses.endwin()
