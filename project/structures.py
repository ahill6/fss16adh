from xml.etree import ElementTree
from copy import deepcopy
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
    
def pick_n(wholeset, n, leaveout=None, cap=False):
    def oneOther():
        retries = len(wholeset) - 1 # if you've tried everything in the set and can't get a valid subset, give up. (this assumes small sets)
        if len(seen) > 0:
            x = seen[0]
        while x in seen and retries > 0:
            if isinstance(wholeset, set):
                x = random.sample(wholeset,1)
            else:
                x = random.choice(wholeset)
            retries -= 1
        if retries <= 0:
            if not cap:
                print(len(seen), len(wholeset), leaveout)
                raise Exception("Pick n failed.  Too many retries.")
            else:
                return -1
            
        seen.append(x)
        return x

    selection = set()
    if isinstance(wholeset, set) and leaveout == None:
        if len(wholeset) < n:
            if cap:
                return wholeset
            else:
                return set()
        else:
            selection = set(random.sample(wholeset, int(n)))
            return selection
            
    if leaveout == None or len(leaveout) == 1:    
        seen = [leaveout]
    else:
        seen = [x for x in leaveout]

    n = int(n)
    
    for counter in range(n):
        tmp = oneOther()
        if tmp == -1:
            break
        else:
            selection.add(tmp)
    
    return selection

"""Helper methods for io
"""
def read_data(filename):
    """Takes tree returned from xml_reader and builds the model from that data
    """
    xmltree = readdata(filename)
    decisions = []
    objectives = []
    constraints = []
    features = []

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
    
    for feat in xmltree.iter('feature'):
        varname = feat.find('name').text
        cost = feat.find('cost').text
        payoff = feat.find('cost').text
        features.append(Feature(varname, cost, payoff))
    
    earlyout = eval(xmltree.find('omax').text)
    evaluate = xmltree.find('evaluationMethod').text

    return decisions, objectives, constraints, features, earlyout, evaluate

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

class Feature(O):
    """
    Class indicating Objective of a problem
    """

    def __init__(self, name, cost=1, payoff=1):
        """
        @param name: Name of the objective
        @param func: Function to compute this objective value
        @param do_minimize: Flag indicating if objective has to be minimized or maximized
        """
        O.__init__(self, name=name, cost=cost, payoff=payoff)

class Solution(O):
    """
    Represents a solution
    """

    def __init__(self, decisions, features, opp):
        O.__init__(self)
        self.decisions = decisions
        self.objectives = None
        self.features = features
        self.opponent_features = opp
        self.old_features = deepcopy(features)

    def __hash__(self):
        return hash(tuple(self.decisions))

    def __eq__(self, other):
        return self.decisions == other.decisions

    def clone(self):
        new = Solution(self.decisions, self.features, self.opponent_features)
        new.objectives = self.objectives
        new.old_features = self.old_features
        return new
        
    def new_features(self, p, problem):
        successes = int(min(round((p/10000.0)/random.random()), len(self.features)))
        #successes = 1 if random.random() < p/100.0 else 0 
        return pick_n(problem.all_features - self.features, successes, cap=True) #ugh
        
    def competitor_features(self, p):
        # TODO - replace the [0] indices with something that allows arbitrary index- and figure out how storing this data for multi-company case.
        successes = int(min(round((p/10.0)/random.random()), len(self.opponent_features - self.features)))
        #successes = 1 if random.random() < p/90.0 else 0
        return pick_n((set(self.opponent_features) - set(self.features)), successes, cap=True)


class Problem(O):
    """
    Class representing the problem.
    """

    def __init__(self, filename, companies=0):
        decs, objs, consts, initfeats, omax, evalu = read_data(filename) 
        mine = self.generate_initial_features(initfeats)
        theirs = []
        for i in range(companies):
            theirs.append(self.generate_initial_features(initfeats, mine))
        O.__init__(self, decisions=decs, objectives=objs, constraints=consts, omax=omax, my_features=mine, opponent_features=theirs, all_features=set(initfeats))
        
    def generate_initial_features(self, allfeatures, preexisting=None, low=None, high=None):
        """TODO - still just random generation.  WAnt some commonality between starting feature sets.
        """
        base = len(allfeatures)//5
        low = low or int(max(0.5*base, 0))
        high = high or int(max(1.5*base, low+1))
        features = random_value(low, high, decimals=0)
        """
        if preexisting != None:
            unique = set()
            for item in preexisting:
                if random.random() < 0.1:
                    unique.add(item)
        else:
            unique = preexisting
        """            
        #tmp = pick_n(allfeatures, features, leaveout=unique)
        #if len(tmp - preexisiting) == len(tmp):
            #random.sample(preexisting,1)
            
        return pick_n(allfeatures, features, leaveout=preexisting)
        
    def evaluate(self, sol):
        """This is a model-specific evaluation method.  I am nearly certain there is a better way to do this, 
        even if it is just putting this in a different file and importing it as part of the model...
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
            
        #1) calculate what new features you get
        a = sol.new_features(new_feature_effort, self)
        
        #2) calculate what competitor features you get
        b = sol.competitor_features(catchup_feature_effort) # this will need to be transferred to the factory for the n-companies case
        maxnew = min(len(a)+len(b), 2*len(sol.features))
        c = pick_n(a.union(b), maxnew)
        #3) calculate the score with these values
        soltmp = deepcopy(sol)
        soltmp.features.update(c)
        if self.is_valid(self, soltmp):
            sol.features = deepcopy(soltmp.features)
            
        """Now that all variables in the objective functions have values, evaluating them
        is simply a matter of calling "eval" on the objectives (already inputted as mathematical operations)
        """
        ener = []
        for obj in self.objectives:
            ener.append(eval(obj.func))

        sol.objectives = ener
        return sol
        
        
    @staticmethod
    #def evaluate(self, sol):
    def evaluate_a(self, sol):
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
    
    def generate_pop(self, n):
        population = []
        population.append(self.generate_one())
        opp = population[0].opponent_features
        for x in range(n):
            population.append(self.generate_one(opp))
        
        return population
        
    def generate_one(self, opponent=None):
        """Generate one valid solution"""
        retries = 250 #make this configurable
        while retries > 0:
            if opponent == None:
                sol = Solution([random_value(d.low, d.high) for d in self.decisions], self.generate_initial_features(self.all_features), self.generate_initial_features((self.all_features)))
            else:
                sol = Solution([random_value(d.low, d.high) for d in self.decisions], self.generate_initial_features(self.all_features), opponent)
            if self.is_valid(self, sol):
                return sol
            retries -= 1
        raise Exception('Problem too hard, unable to generate a valid solution randomly')

class Factory():
    # make n many Solutions
    print("yes")
    
    # populate their decisions, objectives, constraints somehow