from __future__ import print_function
from xml.etree import ElementTree
import sys, random, copy


def better(a, b):
    """Returns true if a is better than b by whatever metric is put here
    (domination, fitness function, greater than, less than, et al.)
    """
    if isinstance(a, (list, tuple)):
        a = a[0]
    if isinstance(b, (list, tuple)):
        b = b[0]
    """
    if a < 0:
        return False
    """
    return a < b


def xml_reader(filename):
    tree = ElementTree.parse(filename)
    root = tree.getroot()
    return tree


def readdata(filename):  # this was originally intended for bulk input of files, but it now only does one.
    if '.xml' in filename:
        data = xml_reader(filename)
    else:
        print("need to get csv reader")
    return data


def read_data(filename):
    xmltree = readdata(filename)
    decisions = []
    objectives = []
    constraints = []

    for cin in xmltree.findall('constraint'):
        constraints.append(Constraint(cin.text))

    for bound in xmltree.iter('bound'):
        varname = bound.find('var').text
        low = float(bound.find('min').text)
        high = float(bound.find('max').text)
        decisions.append(Decision(varname, low, high))

    for ener in xmltree.iter('energy'):
        varname = ener.find('function').text
        func = varname
        minimize = ener.find('minimize').text
        objectives.append(Objective(varname, func, minimize))

    return decisions, objectives, constraints


def random_value(low, high, decimals=2):
    """
    Generate a random number between low and high.
    decimals incidicate number of decimal places
    """
    return round(random.uniform(low, high), decimals)


def output(x): print(x, end="")


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


class Constraint(O):
    """
    class indicating a Constraint of the problem
    """

    def __init__(self, value):
        """
        @param value: the constraint, entered as a boolean formula
        """
        O.__init__(self, value=value)


class Decision(O):
    """
    Class indicating Decision of a problem (a variable with its bounds)
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

    def __init__(self, name, func, do_minimize=True):
        """
        @param name: Name of the objective
        @param func: Function to compute this objective value
        @param do_minimize: Flag indicating if objective has to be minimized or maximized
        """
        O.__init__(self, name=name, func=func, do_minimize=do_minimize)


class Solution(O):
    """
    Represents a solution
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
        new = Solution(self.decisions)
        new.objectives = self.objectives
        return new


class Problem(O):
    """
    Class representing the problem.
    """

    def __init__(self, filename):
        O.__init__(self)
        self.decisions, self.objectives, self.constraints = read_data(filename)

    @staticmethod
    def evaluate(self, sol):
        if (len(sol.decisions) != len(self.decisions)):
            raise IndexError("Error, solution and decisions different lengths")

        var = []
        for i in xrange(len(self.decisions)):
            var.append(self.decisions[i].name)
        tmp = zip(var, sol.decisions)

        thismodule = sys.modules[__name__]

        for key, value in tmp:
            setattr(thismodule, key, value)

        ener = []
        for obj in self.objectives:
            ener.append(eval(obj.func))

        sol.objectives = ener
        return sol.objectives

    @staticmethod
    def is_valid(self, sol):
        var = []
        for i in xrange(len(self.decisions)):
            var.append(self.decisions[i].name)
        tmp = zip(var, sol.decisions)

        thismodule = sys.modules[__name__]

        for key, value in tmp:
            setattr(thismodule, key, value)
        for check in self.constraints:
            if not eval(check.value):
                return False
        for i in xrange(len(self.decisions)):
            if not (self.decisions[i].low <= sol.decisions[0] <= self.decisions[i].high):
                return False
        return True

    def generate_one(self):
        while True:
            sol = Solution([random_value(d.low, d.high) for d in self.decisions])
            if Problem.is_valid(self, sol):
                return sol


def p():
    return 0.5


def maxwalksat(retries=10, changes=300):
    datafile = "osyczka.xml"
    problem = Problem(datafile)
    omax = -3000
    current_sol = problem.generate_one()
    best_sol = current_sol
    best_obj = problem.evaluate(problem, best_sol)

    for i in xrange(retries):
        current_sol = problem.generate_one()
        print("\n",current_sol)
        for j in xrange(changes):
            current_obj = problem.evaluate(problem, current_sol)
            if better(current_obj, omax):
                return current_sol
            if better(current_obj, best_obj):
                best_sol = copy.deepcopy(current_sol)
                best_obj = copy.deepcopy(current_obj)
                output("!")
            if p() < random.random():
                rand = random.randint(0, len(problem.decisions) - 1)
                tmp = current_sol
                tmp.decisions[rand] = current_sol.decisions[rand] + problem.decisions[rand].high

                while not problem.is_valid(problem, tmp):
                    tmp.decisions[rand] = random_value(problem.decisions[rand].low, problem.decisions[rand].high)
                current_sol = tmp
                output("#")
            else:
                rand = random.randint(0, len(problem.decisions) - 1)
                dirmax = problem.decisions[rand].high
                dirmin = problem.decisions[rand].low
                tmp = copy.deepcopy(current_sol)
                cur = current_sol.decisions[rand]
                jump = (dirmax - dirmin) / 10.0
                k = cur + jump
                tmp_best = copy.deepcopy(tmp)
                tmp_best_score = current_obj
                while (k) < dirmax:  # going in the positive direction
                    tmp.decisions[rand] = k
                    score = 'a'
                    if problem.is_valid(problem, tmp):
                        score = problem.evaluate(problem, tmp)
                    if better(score, tmp_best_score):
                        tmp_best = copy.deepcopy(tmp)
                        tmp_best_score = score
                    k += jump
                k = cur - jump
                while (k) > dirmin:  # going in the negative direction
                    tmp.decisions[rand] = k
                    score = 'a'
                    if problem.is_valid(problem, tmp):
                        score = problem.evaluate(problem, tmp)
                    if better(score, tmp_best_score):
                        tmp_best = copy.deepcopy(tmp)
                        tmp_best_score = score
                    k -= jump
                # If we are jumping all the way to the best one found
                current_sol = copy.deepcopy(tmp_best)
                # If we are taking one step in the direction of best one found
                """
                tmp = current_sol
                if current_sol.decisions[rand] > tmp_best.decisions[rand]:
                    while tmp.decisions[rand] > dirmin:
                        tmp.decisions[rand] -= jump
                        if problem.is_valid(problem, tmp):
                            current_sol = tmp
                            break
                elif current_sol.decisions[rand] > tmp_best.decisions[rand]:
                    while tmp.decisions[rand] > dirmin:
                        tmp.decisions[rand] -= jump
                        if problem.is_valid(problem, tmp):
                            current_sol = tmp
                            break
                else:
                    pass
                """
                output(".")
            if ((j + 1) % 25 == 0):
                print("\n")
        print("\n", best_sol)
    return best_sol


print("\n", maxwalksat())
