import random
import time
import tkinter as tk

from utils_and_const import N, CELL_SIZE, PADDING, NUM_OBSTACLES
from threading import Thread


class Grid:
    def __init__(self, algo_callback=None):

        self.algo_callback = algo_callback

        rows = cols = N
        self.root = tk.Tk()

        canvas_width = cols * CELL_SIZE
        canvas_height = rows * CELL_SIZE
        self.root.title("Game Grid")

        # Create a canvas and scrollbars to make the main_frame scrollable
        self.container = tk.Canvas(self.root)
        self.vsb = tk.Scrollbar(self.root, orient="vertical", command=self.container.yview)
        self.hsb = tk.Scrollbar(self.root, orient="horizontal", command=self.container.xview)
        self.container.configure(yscrollcommand=self.vsb.set, xscrollcommand=self.hsb.set)

        self.vsb.pack(side="right", fill="y")
        self.hsb.pack(side="bottom", fill="x")
        self.container.pack(side="left", fill="both", expand=True)

        # Create the main_frame inside the container canvas
        self.main_frame = tk.Frame(self.container)
        self.container.create_window((0, 0), window=self.main_frame, anchor="nw")

        # Log window frame
        self.log_frame = tk.Frame(self.main_frame)
        self.log_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

        # Clear log button
        self.clear_log_button = tk.Button(self.log_frame, text="Clear Log", command=self.clear_log)
        self.clear_log_button.pack(side=tk.BOTTOM, pady=5)

        # Log window with scrollbar
        self.log_text = tk.Text(self.log_frame, state=tk.DISABLED, width=40, height=20)
        self.log_scroll = tk.Scrollbar(self.log_frame, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=self.log_scroll.set)
        self.log_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create a frame for the buttons and pack it to the left of the main frame
        self.button_frame = tk.Frame(self.main_frame, pady=PADDING*20)
        self.button_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Create and pack the buttons in the button frame
        self.button_run = tk.Button(self.button_frame, text="Run Algorithm", command=self.run)
        self.button_run.grid(row=0, column=0, sticky="ew")
        self.button_frame.grid_rowconfigure(0, weight=1)
        self.button_obs = tk.Button(self.button_frame, text="Add Obstacles", command=self.add_obstacles)
        self.button_obs.grid(row=1, column=0, sticky="ew")
        self.button_frame.grid_rowconfigure(1, weight=1)
        self.button_stop = tk.Button(self.button_frame, text="Stop", command=self.stop)
        self.button_stop.grid(row=2, column=0, sticky="ew")
        self.button_frame.grid_rowconfigure(2, weight=1)
        self.button_clear = tk.Button(self.button_frame, text="Clear", command=self.clear)
        self.button_clear.grid(row=3, column=0, sticky="ew")
        self.button_clear.config(state=tk.DISABLED)
        self.button_frame.grid_rowconfigure(3, weight=1)

        # Create and place the canvas in the main frame
        self.canvas = tk.Canvas(self.main_frame, width=canvas_width, height=canvas_height, bg="white")
        self.canvas.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.grid = self.create_grid(rows, cols, CELL_SIZE)

        # Define and paint the start and ending point
        self.start_point = 1, 1
        self.end_point = N-2, N-2
        start_cell = self.grid[self.start_point[0]][self.start_point[1]]
        end_cell = self.grid[self.end_point[0]][self.end_point[1]]
        self.canvas.itemconfig(start_cell['rect'], fill='blue')
        self.canvas.itemconfig(end_cell['rect'], fill='red')

        # Update scrollregion after adding content and binding mouse scroll
        self.main_frame.bind("<Configure>", lambda e: self.container.configure(scrollregion=self.container.bbox("all")))
        self.container.bind("<MouseWheel>", lambda e: self.container.yview_scroll(int(-1 * (e.delta / 120)), "units"))

        self.running = False
        self.running_thread = Thread(target=self.thread_run)

        self.root.mainloop()

    def create_grid(self, rows, cols, cell_size):
        grid = []
        for i in range(rows):
            row = []
            for j in range(cols):
                x1 = j * cell_size
                y1 = i * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size
                rect = self.canvas.create_rectangle(x1, y1, x2, y2, fill='yellow', outline='black')
                row.append({'rect': rect, 'times': 0, 'obstacle': False})
            grid.append(row)
        return grid

    def paint_cell(self, cell):
        cell_value = max(0, min(20, cell['times']))

        intensity = cell_value / 20
        red = 255
        green = int(255 * (1 - intensity) + 165 * intensity)
        blue = 0

        color = f'#{red:02x}{green:02x}{blue:02x}'

        self.canvas.itemconfig(cell['rect'], fill=color)

    def paint_winning_chrom(self, chrom):
        for gene in chrom.genes:
            if (gene.x, gene.y) in (self.start_point, self.end_point):
                continue
            cell = self.grid[gene.x][gene.y]
            self.canvas.itemconfig(cell['rect'], fill='green')

    def paint_chromosome(self, chromosome):
        for gene in chromosome.genes:
            if (gene.x, gene.y) in (self.start_point, self.end_point):
                continue
            cell = self.grid[gene.x][gene.y]
            cell['times'] += 1
            self.paint_cell(cell=cell)

    def clear_chrom(self, chrom):
        for gene in chrom.genes:
            if (gene.x, gene.y) in (self.start_point, self.end_point):
                continue
            cell = self.grid[gene.x][gene.y]
            cell['times'] -= 1
            self.paint_cell(cell=cell)

    def run(self):
        # disable adding obstacles while running
        self.button_obs.config(state=tk.DISABLED)

        # disable clearing the canvas
        self.button_clear.config(state=tk.DISABLED)

        # disable running algo again
        self.button_run.config(state=tk.DISABLED)

        # update running flag
        self.running = True

        # start thread
        self.running_thread.start()

    def thread_run(self):

        self.log('Running algorithm...')

        if self.algo_callback:
            self.algo_callback(self)

        # change flag to not running
        self.running = False

        # enable clear button
        self.button_clear.config(state=tk.NORMAL)

    def paint_chromosomes(self, pool):
        for chrom in pool:
            self.paint_chromosome(chrom)

    def add_obstacles(self):
        self.log("Adding obstacles...")
        available_cells = []
        for i in range(N):
            for j in range(N):
                cell = self.grid[i][j]
                if (i, j) not in (self.start_point, self.end_point) and not cell['obstacle']:
                    available_cells.append((i, j))

        for _ in range(NUM_OBSTACLES):
            if not available_cells:
                break

            rand_x, rand_y = random.choice(available_cells)
            available_cells.remove((rand_x, rand_y))
            cell = self.grid[rand_x][rand_y]
            cell['obstacle'] = True
            self.canvas.itemconfig(cell['rect'], fill='black')
            self.root.update()

        # enable clearing the board
        self.button_clear.config(state=tk.NORMAL)

        self.log('Done')

    def stop(self):
        # update the flag, this will end the thread run
        self.running = False

        self.log('Stopped')

    def clear(self):
        self.log('Clearing...')
        for i in range(N):
            for j in range(N):
                cell = self.grid[i][j]
                if (i, j) in (self.start_point, self.end_point):
                    continue
                cell['times'] = 0
                cell['obstacle'] = False
                self.canvas.itemconfig(cell['rect'], fill='yellow')

        # enable all buttons
        self.button_obs.config(state=tk.NORMAL)
        self.button_run.config(state=tk.NORMAL)
        self.button_stop.config(state=tk.NORMAL)

        # assign new thread for next runs
        self.running_thread = Thread(target=self.thread_run)

        self.log('Cleared')

    def log(self, message):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + '\n')
        self.log_text.config(state=tk.DISABLED)
        self.log_text.see(tk.END)

    def clear_log(self):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete('1.0', tk.END)
        self.log_text.config(state=tk.DISABLED)
