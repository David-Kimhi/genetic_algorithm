import random


N = 40
CELL_SIZE = 20
# game-box constants

NUM_OBSTACLES = N//2

PADDING = 10
BUTTON_BAR_HEIGHT = 60

BUTTON_WIDTH = 40
BUTTON_HEIGHT = 10

LEFT_BAR_SIZE = 200

# constants to represent a directions of moving in the greed
UP = 0
LEFT = 1
DOWN = 2
RIGHT = 3

DIRECTIONS = 4  # number of directions


def roulette_wheel(pool):
    """
    Implement a roulette wheel for picking random chromosome from pool,
    considering its fitness value
    :param pool: pool of chromosomes
    :return: The chosen chromosome
    """
    fit_values = [chrom.fitness_value for chrom in pool]
    max_value = sum(fit_values)
    pick = random.uniform(0, max_value)  # pick a random value between the sum and 0
    current = 0

    #  the bigger values have more chance to get picked
    for chrom in pool:
        current += chrom.fitness_value
        if current > pick:
            return chrom


def reverse_roulette_wheel(pool):
    """
    Same as roulette wheel, except that in this case we're choosing the least fitted chromosome.
    :param pool: Collection of chromosomes
    :return: The chosen chromosome
    """
    fit_values = [1/chrom.fitness_value for chrom in pool]
    max_value = sum(fit_values)
    pick = random.uniform(0, max_value)
    current = 0

    for chrom in pool:
        current += 1/chrom.fitness_value
        if current > pick:
            return chrom


def mutation(chrom, max_number):
    # in average, one of the entire new population will have a mutation
    if not random.randint(0, max_number):
        # generating "small" change
        rand_rotation_times = random.randint(1, 3)
        rand_location = random.randint(0, len(chrom.list_dir) - 1)
        rand_start_or_end = random.randint(0,1)
        if rand_start_or_end:
            new_list_dir = chrom.list_dir[:rand_location]
            for dir_ in chrom.list_dir[rand_location:]:
                new_list_dir.append(rotate_direction(dir_, rand_rotation_times))
        else:
            new_list_dir = []
            for dir_ in chrom.list_dir[:rand_location]:
                new_list_dir.append(rotate_direction(dir_, rand_rotation_times))
            new_list_dir = new_list_dir + chrom.list_dir[rand_location:]

        chrom.list_dir = new_list_dir


def manhattan_distance(point1, point2):
    return abs(point1.x - point2.x) + abs(point1.y - point2.y)


def rotate_direction(direction, times):
    return (direction + times) % 4



