import tkinter as tk
from tkinter import messagebox

def show_message():
    messagebox.showinfo("Info", "Button Clicked!")

# Create the main window
root = tk.Tk()
root.title("Simple Webpage")

# Set the size of the window
root.geometry("300x200")

# Create a button
button = tk.Button(root, text="Click Me", command=show_message)

# Place the button in the window
button.pack(pady=50)

# Run the application
root.mainloop()
