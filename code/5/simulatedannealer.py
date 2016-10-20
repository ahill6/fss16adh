from __future__ import print_function
from xml.etree import ElementTree
import sys, random, copy, math


def better(a, b):
    """Returns true if a is better than b by whatever metric is put here
    (domination, fitness function, greater than, less than, et al.)
    """
    if isinstance(a, (list, tuple)) and len(a) == 1:
        a = a[0]
    if isinstance(b, (list, tuple)) and len(b) == 1:
        b = b[0]
    try:
        if isinstance(a+0.0,float) and isinstance(b+0.0,float):
            return a < b
    except:
        pass
    else:
        return bdom(a, b)
    """
    if isinstance(a, (list, tuple)) and len(a) == 1:
        a = a[0]
    if isinstance(b, (list, tuple)) and len(b) == 1:
        b = b[0]
        
    return a < b
    
    return bdom(a,b, problem)
    """
    
def bdom(x, y):
    """multi objective
    Added later, still needs work to make more general"""
    betters = 0
    if len(x) != len(y):
        raise IndexError("Error, two items have different lengths",x,y)
    for obj in xrange(len(x)):
        if x[obj] < y[obj] : betters += 1 # need to generalize so it can also handle >
        elif x[obj] != y[obj]: return False
    return betters > 0

"""
def cdom(x, y):
    "many objective"
    def w(better):
        return -1 if better == less else 1 # I like this idea, but need to work on this particular implementation
    def expLoss(w,x1,y1,n):
        return -1*e**( w*(x1 - y1) / n )
    def loss(x, y):
        losses= []
        n = min(len(x),len(y))
        for obj in abouts._objs:
            x1, y1  = x[obj.pos]  , y[obj.pos]
            x1, y1  = obj.norm(x1), obj.norm(y1)
            losses += [expLoss( w(obj.want),x1,y1,n)]
        return sum(losses) / n
    l1= loss(x,y)
    l2= loss(y,x)
    return l1 < l2 
"""

def same(x)  : return x
def less(x,y): return x < y
def more(x,y): return x > y


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


def random_value(low, high, decimals=2):
    """
    Generate a random number between low and high.
    decimals incidicate number of decimal places
    """
    return round(random.uniform(low, high), decimals)


def output(x): print(x, end="") # print without newline


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
        while True:
            sol = Solution([random_value(d.low, d.high) for d in self.decisions])
            if Problem.is_valid(self, sol):
                return sol
    
def randomjump(low,high):
    return low + random.random()*(high-low) # this can be used either as a percentage of the whole space or just step length

def P(current, next, heat):
    """Calculates the probability of a "dumb" jump.  Likelihood decreases as k increases
    """
    # this doesn't work unless the "better" method is < or >.  Is there a way to do this with bdom/cdom?
    if isinstance(current, (list, tuple)):
        current = current[0]
    if isinstance(next, (list, tuple)):
        next = next[0]
        
    max = 199960004.0 # need to figure out how to change this/set it automatically for new problems...ugh
    min = 2.0
    old = (current - min) / (max - min)
    new = (next - min) / (max - min)
    
    if heat != 0:
        return math.exp((old-new)/heat)
    else:
        print("heat = 0, divide by zero")
        print (current, next, heat)
        sys.exit()
        
def singlemove(prob, cur):
    index = random.randint(0,len(prob.decisions)-1)
    jumpsize = (prob.decisions[index].high - prob.decisions[index].low)*.01
    cur.decisions[index] += randomjump(-jumpsize, jumpsize)
    return cur
    
def multimove(prob, cur):
    for i in range(len(prob.decisions)):
        jumpsize = (prob.decisions[i].high - prob.decisions[i].low)*.01
        cur.decisions[i] += randomjump(-jumpsize, jumpsize)
    return cur
    
def annealer(filename):  # need to figure out how to get this to work with multiple dimensions/objectives/decisions
    """The only part of this file specific to Simulated Annealing.  This is the SA algorithm.
    """
    move = multimove # figure out a more elegant way to set this, but can pick whichever.
    #move = singlemove
    
    if filename == None:
        print("SA no file")
        filename = "osyczka2.xml"
    problem = Problem(filename)
    omax = problem.omax    # this needs to also be specified in model.  I am calling it omax even though it could be a minimum
    #omax = -3000
    current_sol = problem.generate_one()
    current_obj = problem.evaluate(problem, current_sol)
    best_sol = copy.deepcopy(current_sol)
    best_obj = copy.deepcopy(current_obj)
    k = 1
    kmax = 1000.0 #need another part of file for state constants(?)
    
    # NEED TO CHANGE ALL OF THESE "<" TO "BETTER" and get a good implementation of "better"
    # Run Simulated Annealer
    while (k < kmax and current_obj > omax):
        next_sol = move(problem, current_sol)
        next_obj = problem.evaluate(problem, next_sol)
        if next_obj < best_obj:
            # We have a new best!
            current_sol = copy.deepcopy(next_sol)
            current_obj = copy.deepcopy(next_obj)
            best_sol = copy.deepcopy(next_sol)
            best_obj = copy.deepcopy(next_obj)
            #output("!")
        elif next_obj < current_obj:
            # Incremental improvement
            current_sol = copy.deepcopy(next_sol)
            current_obj = copy.deepcopy(next_obj)
            #output("+")
        elif P(current_obj, next_obj, k/kmax) < random.random():
            # At some probability, jump to the new location despite being worse
            current_sol = copy.deepcopy(next_sol)
            current_obj = copy.deepcopy(next_obj)
            #output("?")
        else:
            output(".") # nothing special happened
        k += 1
        if k%25 == 0:
            print("\t", best_obj)
            
    print("\nEnded at", k)
    print("state \t", best_sol)
    print("energy\t", best_obj)
    return best_sol