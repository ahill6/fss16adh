#from structures3 import Factory
from maxwalksat import mws
from simulatedannealer import annealer
from de import diffevolve
from particleswarm import pso

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

class Company(O):
    
    """A representation of a single company.
    """
    """
    def __init__(self, decisions, constraints):
        O.__init__(self, decisions = decisions, constraints = constraints, objectives = objectives)
    """
    def __init__ (self, data):
        decisions, constraints, objectives = readfile(data)
        O.__init__(self, decisions=decisions, constraints=constraints, objectives=objectives)
    
    def new_features():
        print("In work")
        sys.exit(0)
        
    def competitor_features():
        print("In work")
        sys.exit(0)
    
# read file and make company
"""
filename = "round1.xml"
problem = Problem(filename)
current_sol = problem.generate_one()
print(current_sol)
"""

filename = "round2.xml"
results = {}
method = [diffevolve]
#factory = Factory(filename, 10)

#print(len(factory.problems))
#print(factory.crossfeats)
#print(factory.problems[0])
#out = open('output.txt', 'w')

for m in method:
  results[str(m)] = m(filename,1) # added a second argument of number of companies.  Maybe will work with everyone since added in structures?
print results


# use different optimizers to attempt to optimize the problem
