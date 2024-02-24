import random
from utils_and_const import UP, DOWN, LEFT, RIGHT, N, manhattan_distance
from grid import Grid
from interaction import num_children


class Gene:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if not isinstance(other, Gene):
            return False
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def copy(self):
        return Gene(self.x, self.y)


class Chromosome:
    def __init__(self, grid: Grid):
        self.grid = grid
        self.genes = set()
        self.length = 0   # length of the chromosome
        self.stuck = False  # is this chromosome reached an end point
        self.distance = 0
        self.fitness_value = 0
        self.list_dir = []
        self.parent_value = 0
        self.direction_changes = 0

    def generate(self, min_length, max_length):
        curr_gene = Gene(self.grid.start_point[0], self.grid.start_point[1])
        self.genes.add(curr_gene)

        length = random.randint(min_length, max_length)  # length of the chromosome will be randomized

        while len(self.genes) < length:
            directions = [UP, DOWN, RIGHT, LEFT]
            available_directions = directions.copy()
            while available_directions:
                rand = random.choice(available_directions)  # randomly choose a direction
                next_ = next_gene(curr_gene, direction=rand)  # get the next coordinates using the direction
                if self.is_safe(next_):  # check if a move in this direction is valid
                    if next_ not in self.genes:   # check if coordinates already exists
                        curr_gene = next_.copy()
                        self.genes.add(next_)
                        self.list_dir.append(rand)
                        break

                available_directions.remove(rand)  # choose another direction

            # In case the inside loop ended because there wasn't available directions
            if not available_directions:
                self.stuck = True
                break

        self.length = len(self.genes)

        # calculate the distance from the end of the path to the finish point
        self.distance = manhattan_distance(curr_gene, Gene(self.grid.end_point[0], self.grid.end_point[1]))
        self.cal_fitness()

    def cal_fitness(self):
        """
        Calculate the fitness value of the chromosome
        :return: None
        """

        # Iterate through the path and count the changes in direction
        for i in range(1, len(self.list_dir)):
            if self.list_dir[i] != self.list_dir[i - 1]:
                self.direction_changes += 1

        self.length = len(self.genes)
        self.fitness_value = 1 / (
                ((self.distance + 1) ** 8) + (self.length ** 4) + (self.direction_changes ** 4)
        )

    def is_safe(self,  gene: Gene):
        # check if coordinates inside grid
        if (
                gene.x < 0
                or gene.y < 0
                or gene.x > (N-1)
                or gene.y > (N-1)
        ):
            return False

        # check if it's not an obstacle
        if self.grid.grid[gene.x][gene.y]['obstacle']:
            return False

        return True


def next_gene(gene: Gene, direction) -> Gene:

    assert direction in [UP, DOWN, LEFT, RIGHT]

    next_point = ()
    if direction == UP:
        next_point = gene.x - 1, gene.y
    if direction == DOWN:
        next_point = gene.x + 1, gene.y
    if direction == LEFT:
        next_point = gene.x, gene.y - 1
    if direction == RIGHT:
        next_point = gene.x, gene.y + 1

    return Gene(next_point[0], next_point[1])


def mutation(chrom):
    # in average, one of the entire new population will have a mutation
    if not random.randint(0, num_children):
        # generating "small" change: appending the path at a random point by single step (in the same direction)
        rand = random.randint(0, len(chrom.list_dir) - 1)
        chrom.list_dir = chrom.list_dir[:rand] + [chrom.list_dir[rand]] + chrom.list_dir[rand:]


