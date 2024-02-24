from interaction import intro_box
from grid import Grid
from genetic_algo import run_algo


if __name__ == '__main__':
    intro_box()
    grid = Grid(algo_callback=run_algo)

