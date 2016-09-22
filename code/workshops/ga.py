
# All the imports
from __future__ import print_function, division
from math import *
import random
import sys
import operator
import matplotlib.pyplot as plt

# TODO 1: Enter your unity ID here
__author__ = "ahill6"


class O:
    """
    Basic Class which
        - Helps dynamic updates
        - Pretty Prints
    """

    def __init__(self, **kwargs):
        self.has().update(**kwargs)

    def has(self):
        return self.__dict__

    def update(self, **kwargs):
        self.has().update(kwargs)
        return self

    def __repr__(self):
        show = [':%s %s' % (k, self.has()[k])
                for k in sorted(self.has().keys())
                if k[0] is not "_"]
        txt = ' '.join(show)
        if len(txt) > 60:
            show = map(lambda x: '\t' + x + '\n', show)
        return '{' + ' '.join(show) + '}'


print("Unity ID: ", __author__)


# Few Utility functions
def say(*lst):
    """
    Print without going to new line
    """
    print(*lst, end="")
    sys.stdout.flush()


def random_value(low, high, decimals=2):
    """
    Generate a random number between low and high.
    decimals incidicate number of decimal places
    """
    return round(random.uniform(low, high), decimals)


def lt(a, b): return a < b


def shuffle(lst):
    """
    Shuffle a list
    """
    random.shuffle(lst)
    return lst


class Decision(O):
    """
    Class indicating Decision of a problem
    """

    def __init__(self, name, low, high):
        """
        @param name: Name of the decision
        @param low: minimum value
        @param high: maximum value
        """
        O.__init__(self, name=name, low=low, high=high)


class Objective(O):
    """
    Class indicating Objective of a problem
    """

    def __init__(self, name, do_minimize=True):
        """
        @param name: Name of the objective
        @param do_minimize: Flag indicating if objective has to be minimized or maximized
        """
        O.__init__(self, name=name, do_minimize=do_minimize)


class Point(O):
    """
    Represents a member of the population
    """

    def __init__(self, decisions):
        O.__init__(self)
        self.decisions = decisions
        self.objectives = None

    def __hash__(self):
        return hash(tuple(self.decisions))

    def __eq__(self, other):
        return self.decisions == other.decisions

    def clone(self):
        new = Point(self.decisions)
        new.objectives = self.objectives
        return new


class Problem(O):
    """
    Class representing the cone problem.
    """

    def __init__(self):
        O.__init__(self)
        # TODO 2: Code up decisions and objectives below for the problem
        # using the auxilary classes provided above.
        self.decisions = [Decision('r', 0, 10), Decision('h', 0, 20)]
        self.objectives = [Objective('S'), Objective('T')]

    @staticmethod
    def evaluate(point):
        [r, h] = point.decisions
        S = pi * r * sqrt(r ** 2 + h ** 2)
        T = pi * r * (r + sqrt(r ** 2 + h ** 2))
        point.objectives = [S, T]
        # TODO 3: Evaluate the objectives S and T for the point.
        return point.objectives

    @staticmethod
    def is_valid(point):
        [r, h] = point.decisions
        # TODO 4: Check if the point has valid decisions
        return ((h * (r ** 2) * pi / 3) > 200)

    def generate_one(self):
        # TODO 5: Generate a valid instance of Point.
        while True:
            point = Point([random_value(d.low, d.high) for d in self.decisions])
            if Problem.is_valid(point):
                return point


def populate(problem, size):
    population = []
    for i in xrange(size):
        population.append(problem.generate_one())
    # TODO 6: Create a list of points of length 'size'
    return population


def crossover(mom, dad):
    # TODO 7: Create a new point which contains decisions from
    # the first half of mom and second half of dad
    split = len(mom.decisions) // 2
    baby = mom.decisions[split:] + dad.decisions[:split]
    return Point(baby)


def mutate(problem, point, mutation_rate=0.01):
    # TODO 8: Iterate through all the decisions in the point
    # and if the probability is less than mutation rate
    # change the decision(randomly set it between its max and min).
    for i in xrange(len(point.decisions)):
        if random.random() < mutation_rate:
            point.decisions[i] = random_value(problem.decisions[i].low, problem.decisions[i].high)
    return point


def bdom(problem, one, two):
    """
    Return if one dominates two
    """
    strictly_better = False
    objs_one = problem.evaluate(one)
    objs_two = problem.evaluate(two)
    for i in xrange(len(objs_one)):
        if objs_two[i] < objs_one[i]:
            return False
        elif objs_one[i] < objs_two[i]:
            strictly_better = True

    if strictly_better:
        return True
    return False
    # TODO 9: Return True/False based on the definition
    # of bdom above.


def fitness(problem, population, point):
    dominates = 0
    # TODO 10: Evaluate fitness of a point.
    # For this workshop define fitness of a point
    # as the number of points dominated by it.
    # For example point dominates 5 members of population,
    # then fitness of point is 5.
    for pt in population:
        if pt != point:
            if bdom(problem, point, pt):
                dominates += 1
    return dominates


def elitism(problem, population, retain_size):
    # TODO 11: Sort the population with respect to the fitness
    # of the points and return the top 'retain_size' points of the population
    d = dict()
    for i in population:
        d[i] = fitness(problem, population, i)
    new_list = sorted(population, key=lambda x: d[x], reverse=True)
    return new_list[:retain_size]


def ga(pop_size=100, gens=250):
    problem = Problem()
    population = populate(problem, pop_size)
    [problem.evaluate(point) for point in population]
    initial_population = [point.clone() for point in population]
    gen = 0
    while gen < gens:
        say(".")
        children = []
        for _ in range(pop_size):
            mom = random.choice(population)
            dad = random.choice(population)
            while (mom == dad):
                dad = random.choice(population)
            child = mutate(problem, crossover(mom, dad))
            if problem.is_valid(child) and child not in population + children:
                children.append(child)
        population += children
        population = elitism(problem, population, pop_size)
        gen += 1
    print("")
    return initial_population, population


def plot_pareto(initial, final):
    initial_objs = [point.objectives for point in initial]
    final_objs = [point.objectives for point in final]
    initial_x = [i[0] for i in initial_objs]
    initial_y = [i[1] for i in initial_objs]
    final_x = [i[0] for i in final_objs]
    final_y = [i[1] for i in final_objs]
    plt.scatter(initial_x, initial_y, color='b', marker='+', label='initial')
    plt.scatter(final_x, final_y, color='r', marker='o', label='final')
    plt.title("Scatter Plot between initial and final population of GA")
    plt.ylabel("Total Surface Area(T)")
    plt.xlabel("Curved Surface Area(S)")
    plt.legend(loc=9, bbox_to_anchor=(0.5, -0.175), ncol=2)
    plt.show()


initial, final = ga()
plot_pareto(initial, final)
