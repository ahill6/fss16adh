from structures import Problem

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
    

# read file and make company
filename = "specialization.xml"
problem = Problem(filename)
current_sol = problem.generate_one()
print(current_sol)
    
# use different optimizers to attempt to optimize the problem
