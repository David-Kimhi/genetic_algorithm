"""
This program demonstrate using genetic algorithm to find a path, short as possible, between two points in a grid.
The starting point is known, while the finish point is unknown.

The starting and finishing point are selected randomly.
We'll use a large pool of possible solutions (we'll call them "chromosomes"),
 and the genetic algorithm will pick the best routs to the finish point

 To run this program successfully you must have numpy and matplotlib installed

The running time of this program is directly depends on how big the greed is,
and on how many obstacle are in the greed.

"""

import random
from tkinter import *
from grid import Grid
from interaction import get_num_chromosomes, get_num_generations, get_stop_generations, get_num_children
from utils_and_const import N, roulette_wheel, reverse_roulette_wheel, UP, DOWN, LEFT, RIGHT, mutation, manhattan_distance
from objects import Chromosome, Gene, next_gene


def run_algo(grid: Grid):
    pool = generate_pool(grid)
    run_generations(grid=grid, pool=pool)


def generate_pool(grid: Grid):
    grid.log('Generation pool...')

    num_chromosomes = get_num_chromosomes()

    pool = []

    min_length = manhattan_distance(
        Gene(grid.start_point[0], grid.start_point[1]),
        Gene(grid.end_point[0], grid.end_point[1])
    )
    max_length = available_cells(grid=grid)
    while len(pool) < num_chromosomes:
        chrom = Chromosome(grid=grid)
        chrom.generate(min_length, max_length)
        pool.append(chrom)

    return pool


def make_child(parent1, parent2, grid: Grid):

    num_children = get_num_children()

    child = Chromosome(grid=grid)
    # randomly choose the part to split between parent1 and parent2
    divider = random.randint(0, min(len(parent1.list_dir), len(parent2.list_dir)))
    part1 = parent1.list_dir[:divider]
    part2 = parent2.list_dir[divider:]

    child.list_dir = part1 + part2
    mutation(child, num_children)
    adjust_child(child=child, grid=grid)
    return child


def adjust_child(child: Chromosome, grid: Grid):
    new_list_dir = []
    curr_gene = Gene(grid.start_point[0], grid.start_point[1])
    child.genes.add(curr_gene)

    for direction in child.list_dir:
        next_ = next_gene(gene=curr_gene, direction=direction)
        # check the original direction from parent
        if child.is_safe(gene=next_) and next_ not in child.genes:
            new_list_dir.append(direction)
            child.genes.add(next_)
            curr_gene = next_.copy()
        else:
            # if direction from parent isn't valid - choose another direction randomly
            options = {UP, DOWN, LEFT, RIGHT}
            options.remove(direction)  # remove original direction from options
            options = list(options)  # (for shuffle function)
            random.shuffle(options)  # shuffle directions
            found = False  # flag to indicate if some direction is valid
            for option in options:
                next_ = next_gene(gene=curr_gene, direction=option)
                if child.is_safe(gene=next_) and next_ not in child.genes:
                    new_list_dir.append(direction)
                    child.genes.add(next_)
                    curr_gene = next_.copy()
                    found = True
                    break

            if not found:
                child.stuck = True
                break

    child.list_dir = new_list_dir.copy()
    child.distance = manhattan_distance(curr_gene, Gene(grid.end_point[0], grid.end_point[1]))
    child.cal_fitness()


def birth(grid: Grid, pool):

    num_children = get_num_children()

    for _ in range(num_children):
        # choose parents, with higher chance for fitted chromosomes
        parent1 = roulette_wheel(pool)
        pool.remove(parent1)    # remove the parent from pool. make sure it's done before picking the second parent
        parent2 = roulette_wheel(pool)
        pool.remove(parent2)

        # flip a coin to switch the parents (
        if random.randint(0, 1):
            temp = parent1
            parent1 = parent2
            parent2 = temp

        child = make_child(parent1, parent2, grid)

        grid.paint_chromosome(child)
        pool.extend([child, parent1, parent2])


def death(grid: Grid, pool):

    num_chromosomes = get_num_chromosomes()

    for _ in range(len(pool) - num_chromosomes):
        candidate = reverse_roulette_wheel(pool)
        pool.remove(candidate)
        grid.clear_chrom(candidate)


def available_cells(grid: Grid):
    count = 0
    for i in range(N):
        for j in range(N):
            cell = grid.grid[i][j]
            if (i, j) not in (grid.start_point, grid.end_point) and not cell['obstacle']:
                count += 1

    return count


def run_generations(grid: Grid, pool):
    # show the first generation's paths on the grid

    grid.log('Generation 1')

    grid.paint_chromosomes(pool)

    last_max_fitness = calc_max_fitness(pool)

    no_change_count = 0

    num_generations = get_num_generations()
    stop_generations = get_stop_generations()

    for i in range(num_generations -1):
        if not grid.running:
            return
        grid.log(f'Generation {i + 2}')
        birth(grid, pool)
        death(grid, pool)

        new_max_fitness = calc_max_fitness(pool)
        if new_max_fitness == last_max_fitness:
            no_change_count += 1
        else:
            no_change_count = 0

        last_max_fitness = new_max_fitness

        if no_change_count >= stop_generations:
            grid.log('No-change limit has reached.')
            break

    # show winning chrom
    winning_chrom = [chrom for chrom in pool if chrom.fitness_value == last_max_fitness][0]
    grid.paint_winning_chrom(winning_chrom)

    grid.log("Finished")


def calc_max_fitness(pool: list[Chromosome]):
    max_ = 0
    for chrom in pool:
        if chrom.fitness_value > max_:
            max_ = chrom.fitness_value
    return max_

