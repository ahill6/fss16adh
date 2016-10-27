from xml.etree import ElementTree
import sys, random

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

def random_value(low, high, decimals=2):
    """
    Generate a random number between low and high.
    decimals incidicate number of decimal places
    """
    return round(random.uniform(low, high), decimals)

"""Helper methods for io
"""
def read_data(filename):
    """Takes tree returned from xml_reader and builds the model from that data
    """
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
    
    earlyout = eval(xmltree.find('omax').text)

    return decisions, objectives, constraints, earlyout

def xml_reader(filename):
    """Reads an xml file into a tree that can be parsed.
    Here the model is created as an xml document, this reads in the model
    Future versions will have all the I/O abstracted into an I/O class
    """
    tree = ElementTree.parse(filename)
    root = tree.getroot()
    return tree


def readdata(filename):  
    """Generic reader that acts as a quarterback to different file-specific I/O operations
    """
    if '.xml' in filename:
        data = xml_reader(filename)
    else:
        print("need to get csv reader")
    return data

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
        self.decisions, self.objectives, self.constraints, self.omax = read_data(filename)

    @staticmethod
    def evaluate(self, sol):
        """evaluates the objective value(s) for a given solution
        """
        if (len(sol.decisions) != len(self.decisions)):
            raise IndexError("Error, solution and decisions different lengths")
        
        var = []
        for i in xrange(len(self.decisions)):
            var.append(self.decisions[i].name)
        tmp = zip(var, sol.decisions) # tmp now has all variable names and the values of sol for those variables

        thismodule = sys.modules[__name__]

        """Take the variable/value pairs, and set the variable to the value
        (e.g. sol.decisions has 4 for a.  This uses setattr to automatically write the
        statement "a = 4".)
        """
        for key, value in tmp:
            setattr(thismodule, key, value)

        """Now that all variables in the objective functions have values, evaluating them
        is simply a matter of calling "eval" on the objectives (already inputted as mathematical operations)
        """
        ener = []
        for obj in self.objectives:
            ener.append(eval(obj.func))

        sol.objectives = ener
        return sol.objectives

    @staticmethod
    def is_valid(self, sol):
        """Checks whether a solution is valid by seeing if all decision variables are within their bounds, 
        and whether all constraints are met.  Uses same trick as evaluate to assign values.
        """
        
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
            if not (self.decisions[i].low <= sol.decisions[i] <= self.decisions[i].high):
                return False
        return True

    def generate_one(self):
        """Generate one valid solution"""
        retries = 250 #make this configurable
        while retries > 0:
            sol = Solution([random_value(d.low, d.high) for d in self.decisions])
            if Problem.is_valid(self, sol):
                return sol
            retries -= 1
        raise Exception('Problem too hard, unable to generate a valid solution randomly')

class Factory():
    # make n many Solutions
    print("yes")
    # populate their decisions, objectives, constraints somehow