import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# global variables - widget entries
num_chromosomes_entry = None
num_generations_entry = None
stop_generations_entry = None

# global parameters - game parameters
num_chromosomes = num_children = num_generations = stop_generations = 0


def get_num_chromosomes():
    return num_chromosomes


def get_num_children():
    return num_children


def get_num_generations():
    return num_generations


def get_stop_generations():
    return stop_generations


def submit_action(root: tk.Tk):
    global num_chromosomes_entry, num_generations_entry, stop_generations_entry
    global num_chromosomes, num_children, num_generations, stop_generations
    try:
        num_chromosomes = int(num_chromosomes_entry.get())
        num_generations = int(num_generations_entry.get())
        stop_generations = int(stop_generations_entry.get())
        num_children = num_chromosomes // 20  # max number of the new chromosome created out of the selected parents

        # Check if the values are valid
        if num_chromosomes % 10 != 0:
            raise ValueError("Number of chromosomes must be a multiple of 10.")
        if num_chromosomes < 20:
            raise ValueError("Number of chromosomes must be at least 20.")
        if num_generations <= 0 or stop_generations <= 0:
            raise ValueError("Number of generations and stop generations must be positive integers.")

        # If the values are valid, proceed with your algorithm
        print(f"Number of chromosomes: {num_chromosomes}")
        print(f"Number of generations: {num_generations}")
        print(f"Stop training after {stop_generations} generations without change")

        # Close the window
        root.destroy()
    except ValueError as e:
        # Show an error message if the values are not valid
        messagebox.showerror("Invalid Input", str(e))


def intro_box():
    global num_chromosomes_entry, num_generations_entry, stop_generations_entry

    # Set up the main application window
    root = tk.Tk()
    root.title("Genetic Algorithm Game")

    # Create a frame to hold the widgets
    frame = ttk.Frame(root, padding="10")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    # Add a welcome label
    welcome_label = ttk.Label(frame, text="Welcome to the Genetic Algorithm Game!", anchor=tk.CENTER)
    welcome_label.grid(row=0, column=0, columnspan=2, pady=10)

    # Add input labels and entry boxes
    num_chromosomes_label = ttk.Label(frame, text="Number of chromosomes (multiple of 10):")
    num_chromosomes_label.grid(row=1, column=0, sticky=tk.W, pady=5)
    num_chromosomes_entry = ttk.Entry(frame)
    num_chromosomes_entry.grid(row=1, column=1, sticky=tk.E, pady=5)

    num_generations_label = ttk.Label(frame, text="Number of generations:")
    num_generations_label.grid(row=2, column=0, sticky=tk.W, pady=5)
    num_generations_entry = ttk.Entry(frame)
    num_generations_entry.grid(row=2, column=1, sticky=tk.E, pady=5)

    stop_generations_label = ttk.Label(frame, text="Stop after generations without change:")
    stop_generations_label.grid(row=3, column=0, sticky=tk.W, pady=5)
    stop_generations_entry = ttk.Entry(frame)
    stop_generations_entry.grid(row=3, column=1, sticky=tk.E, pady=5)

    # Add a submit button
    submit_button = ttk.Button(frame, text="Submit", command=lambda: submit_action(root))
    submit_button.grid(row=4, column=0, columnspan=2, pady=10)

    # Start the Tkinter event loop
    root.mainloop()
