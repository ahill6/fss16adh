from __future__ import print_function, division
from math import e
from copy import deepcopy
import random
import sys
import numpy
import matplotlib.pyplot as plt


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


# Few Utility functions
def say(*lst):
  """
  Print whithout going to new line
  """
  print(*lst, end="")
  sys.stdout.flush()


def random_value(low, high, decimals=2):
  """
  Generate a random number between low and high.
  decimals incidicate number of decimal places
  """
  return round(random.uniform(low, high), decimals)


def gt(a, b): return a > b


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

  def __init__(self, name, do_minimize=True, low=0, high=1):
    """
    @param name: Name of the objective
    @param do_minimize: Flag indicating if objective has to be minimized or maximized
    """
    O.__init__(self, name=name, do_minimize=do_minimize, low=low, high=high)

  def normalize(self, val):
    if val < self.low:
      self.low = val
    elif val > self.high:
      self.high = val
    return (val - self.low) / (self.high - self.low)


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
    new = Point(self.decisions[:])
    if self.objectives:
      new.objectives = self.objectives[:]
    return new


class Problem(O):
  """
  Class representing the cone problem.
  """

  def __init__(self, decisions, objectives):
    """
    Initialize Problem.
    :param decisions -  Metadata for Decisions
    :param objectives - Metadata for Objectives
    """
    O.__init__(self)
    self.decisions = decisions
    self.objectives = objectives

  @staticmethod
  def evaluate(point):
    assert False

  @staticmethod
  def is_valid(point):
    return True

  def generate_one(self, retries=20):
    for _ in xrange(retries):
      point = Point([random_value(d.low, d.high) for d in self.decisions])
      if self.is_valid(point):
        return point
    raise RuntimeError("Exceeded max runtimes of %d" % 20)


class POM3(Problem):
  from pom3.pom3 import pom3 as pom3_helper
  helper = pom3_helper()
  #!!!! in simulate method should be the place for signaling ...(right?)
  def __init__(self):
    """
    Initialize the POM3 classes
    """
    names = ["Culture", "Criticality", "Criticality Modifier", "Initial Known",
             "Inter-Dependency", "Dynamism", "Size", "Plan", "Team Size", "Signals", "Price"]
    lows = [0.1, 0.82, 2, 0.40, 1, 1, 0, 0, 1, 0, 0]
    highs = [0.9, 1.20, 10, 0.70, 100, 50, 4, 5, 44, 63, 100000]
    #highs = [0.9, 1.20, 10, 0.70, 100, 50, 4, 5, 44, 4]
    decisions = [Decision(n, l, h) for n, l, h in zip(names, lows, highs)]
    objectives = [Objective("Cost", True, 0, 10000), Objective("Value", False, 0, 10000), Objective("Score", False, 0, 1),
                  Objective("Completion", False, 0, 1), Objective("Idle", True, 0, 1), Objective("Profit", False, 0, 1000000)]
    Problem.__init__(self, decisions, objectives)

  def is_valid(self, point):
    for s in range(len(self.decisions)):
      if not self.decisions[s].low < point.decisions[s] < self.decisions[s].high:
        return False
    return True
    
  def add_competitors(self, lst):
    self.companies = lst
    
  def set_requirements(self, requirements):
    self.requirements = requirements
    self.helper.set_requirements(self.requirements)
    
    
  def pick_dec(self, comp):
    r = random.randint(0, len(self.decisions)-1)
    name = self.decisions[r].name
    val = self.companies[comp].decisions[r]
    return name, val
  
  def final_evaluate(self, population):
    for p in population:
      p.objectives = self.evaluate(p)
    return population
  
    
  def sim_demand(self, results, price):
    """
    NEED:   scores from all companies
    OUTPUT: demand distribution
    """
    prior = [1.0/len(results) for x in results]
    tmp_valcost = [x[1]/x[0] if x[0] != 0 else -1 for x in results] # value/cost
    tmp_score   = [x[2]/x[3] if x[3] != 0 else -1 for x in results] # score/completion (sensical?)
    tmp_price = [x.decisions[-1] for x in self.companies] # need some way to use updated values
    tmp_price.append(price)
    tmp = [0 for _ in tmp_valcost]
    posterior = [0 for _ in tmp_valcost]
    
    tmp_sum = 0
    for x in range(len(tmp_valcost)):
      tmp[x] = tmp_valcost[x]*tmp_score[x]
      tmp_sum += tmp[x]
    for x in range(len(tmp)):
      tmp[x] /= tmp_sum
    
    tmp_sum = 0
    for x in range(len(prior)):
      posterior[x] = tmp[x]*prior[x]
      tmp_sum += posterior[x]
    for x in range(len(posterior)):
      posterior[x] /= tmp_sum
      
    return posterior
    
  def evaluate(self, point):
    if not point.objectives:
      signals = {}
      tmpcompanies = deepcopy(self.companies)
      for c in tmpcompanies:
        count = 1
        rand = c.decisions[9] # get the signaling decision variable
        # get decision variable 
        while rand > 1:
          i = rand % 2
          if i == 1:
            x,y = self.pick_dec(c.name)
            time = count if random.random() < 0.5 else count + 1
            if time in signals:
              signals[time].append({'name': c.name, 'decision': x, 'value': y})
            else:
              signals[time] = []
              signals[time].append({'name': c.name, 'decision': x, 'value': y})
          rand /= 2
          count += 2
          
      signal_times = signals.keys()
      
      #timesteps = problem.helper.numberOfShuffles
      timesteps = 10 # should be made dynamically somehow
      
      mytries = {}
      evaltries = []
      teamlist = []
      # for each of these companies, run the sim, return the top 3, display
      for c in tmpcompanies:
        teamlist.append(c)
      teamlist.append(point)
      
      self.helper.reset()
      self.helper.establish_teams(teamlist)
        
      for i in range(timesteps):
        if i in signal_times:
          for j in signals[i]:
            self.helper.change_team_decision(j['name'], j['decision'], j['value'])
            #if self.helper.quit_check(timesteps - i):
            if not self.helper.quit_check(timesteps - i): # this one is correct, the other is just so it runs for now
              print("Tap Out")
              #HERE somehow store the current state/company name/round HERE
              i = timesteps
        self.helper.step_sim(1)
          
      #need to remove duplicates(?)
      results = self.helper.calculate_results()
      distr = self.sim_demand(results, point.decisions[-1])
      price_tmp  = distr[-1]*point.decisions[-1]
      # calculate profit here, make it another thing to maximize
      tmp = []
      tmp = results[-1]
      tmp.append(price_tmp)
      point.objectives = tmp
      
      
    return point.objectives
    


"""
Utility tests
"""


def populate(problem, size):
  """
  Create a Point list of length size
  """
  population = []
  retries = size*100
  for _ in range(size):
    tmp = problem.generate_one()
    if tmp not in population:
      population.append(tmp)
    elif retries < 0:
      raise Exception("Could not create initial population")
    else:
      retries -= 1
  return population


def crossover(mom, dad):
  """
  Create a new point which contains decisions from
  the first half of mom and second half of dad
  """
  n = len(mom.decisions)
  return Point(mom.decisions[:n // 2] + dad.decisions[n // 2:])


def mutate(problem, point, mutation_rate=0.01):
  """
  Iterate through all the decisions in the point
  and if the probability is less than mutation rate
  change the decision(randomly set it between its max and min).
  """
  for i, decision in enumerate(problem.decisions):
    if random.random() < mutation_rate:
      point.decisions[i] = random_value(decision.low, decision.high)
  return point

def cdom(problem, one, two):
  # don't forget to normalize objective scores
  "many objective"
  objs_one = problem.evaluate(one)
  objs_two = problem.evaluate(two)
  """
  if isinstance(objs_one[-1], (list, tuple)):
    del objs_one[-1] # Don't forget to remove these eventually.  Right now take off "features"
  if isinstance(objs_two[-1], (list, tuple)):
    del objs_two[-1] # Don't forget to remove these eventually.  Right now take off "features"
  """
  
  def w(better):
    return -1 if better else 1
  def expLoss(w,x1,y1,n):
    return -1*e**( w*(x1 - y1) / n )
  def loss(x, y):
    losses= []
    n = min(len(x),len(y))
    for obj in range(len(problem.objectives)):
      objtmp = problem.objectives[obj]
      x1, y1  = x[obj]  , y[obj]
      if abs(y1 - x1) < (objtmp.high - objtmp.low)*.0001:
        continue
      x1, y1  = objtmp.normalize(x1), objtmp.normalize(y1)
      losses += [expLoss( w(objtmp.do_minimize),x1,y1,n)]
    return sum(losses) / n
  l1= loss(objs_one,objs_two)
  l2= loss(objs_two, objs_one)
  return l1 < l2 
  
def bdom(problem, one, two):
  """
  Return if one dominates two based
  
  on binary domintation
  """
  objs_one = problem.evaluate(one)
  objs_two = problem.evaluate(two)
  objs_one = [problem.objectives[i].normalize(objs_one[i]) for i in range(len(objs_one))]
  objs_two = [problem.objectives[i].normalize(objs_two[i]) for i in range(len(objs_two))]
  dominates = False
  for i, obj in enumerate(problem.objectives):
    better = lt if obj.do_minimize else gt
    if better(objs_one[i], objs_two[i]):
      dominates = True
    elif objs_one[i] != objs_two[i]:
      return False
  return dominates

def compare(problem, one, two, dom_func=cdom):
  return dom_func(problem, one, two)

def fitness(problem, population, point, dom_func):
  """
  Evaluate fitness of a point based on the definition in the previous block.
  For example point dominates 5 members of population,
  then fitness of point is 5.
  """
  return len([1 for another in population if dom_func(problem, point, another)])


def elitism(problem, population, retain_size, dom_func):
  """
  Sort the population with respect to the fitness
  of the points and return the top 'retain_size' points of the population
  """

  fitnesses = []
  for point in population:
    fitnesses.append((fitness(problem, population, point, dom_func), point))
  population = [tup[1] for tup in sorted(fitnesses, reverse=True)]
  return population[:retain_size]

def sampling(problem, init_pop, sample_size=100, keep_size=25, dom_func=cdom, verbose=True):
  # generate sample_size points
  initial_population = populate(problem, sample_size)
  
  for point in initial_population:
    point.objectives = problem.evaluate(point)
  
  population = [point.clone() for point in initial_population]
  #keep the keep_size best
  population = elitism(problem, population, keep_size, dom_func)
  
  if verbose: print("*")
  return population


def cdomga(problem, inp_population=None, retain_size=10, gens=10, dom_func=cdom, verbose=True):

  population = [point.clone() for point in inp_population]
  
  for point in population:
    point.objectives = problem.evaluate(point)

  initial_population = [point.clone() for point in population]
  for _ in range(gens):
    if verbose: say(".")
    children = []
    for _ in range(retain_size):
      mom = random.choice(population)
      dad = random.choice(population)
      while mom == dad:
        dad = random.choice(population)
      child = mutate(problem, crossover(mom, dad))
      if problem.is_valid(child) and child not in population + children:
        children.append(child)
    population += children
    population = elitism(problem, population, retain_size, dom_func)
  if verbose: print("")
  return population
  
def wrap(num, dec):    
    low, high = dec.low, dec.high
    return low if low==high else low + ((num - low) % (high - low))
def cap(num, dec):  return max(dec.low, min(dec.high, num))
    
def pso(problem, initial_population, iterations=100, trim=cap):
  def generate_velocity(problem, needed):
    """Generate initial swarm velocities with very small values (< .0001% of range).
    """
    return [[random.random()*(y.high-y.low)/100000.0 for y in problem.decisions] for k in range(needed)]
    
  location = []
  velocity = []
  swarm = deepcopy(initial_population)
  #generate initial population
  velocity = generate_velocity(problem, len(swarm))
  best = elitism(problem, swarm, 1, cdom)[0]
  velocity = numpy.array(velocity)
  
  """the magic parameters below have been selected as follows:
  k - per suggestion from class notes
  w,p - engineering judgment (i.e. experimentation, took best values)
  """
  k = .1
  w = 3.0
  p = 4.1  # see if these need to be changed (based on problem size/number of decisions??)
  
  #run pso
  for i in range(iterations):
    say(".")
    for k in range(len(swarm)):
      # move, update asynchronously
      velocity[k] = k*(w*velocity[k] + p*numpy.subtract(best.decisions, swarm[k].decisions))
      # even with the constriction factor, velocity was increasing without bound, use Nmax = Vmax
      velocity[k] = [trim(velocity[k][i], problem.decisions[i]) for i in range(len(problem.decisions))]
      dt = swarm[k].decisions + velocity[k]
            
      for j in range(len(dt)):
        if dt[j] != trim(dt[j], problem.decisions[j]):
          velocity[k][j] = 0.0
          dt[j] = trim(dt[j], problem.decisions[j])
        swarm[k].decisions = dt
      
        if compare(problem, swarm[k], best):
          print(best)
          best = deepcopy(swarm[k])
          print(best)
    
  return swarm


def de(problem, initial_population, gens=100, trim=cap):
    def next_generation(problem, f, cf, frontier, total=0.0, n=0):
        """Calculates next generation"""
        for x in frontier:
            new = extrapolate(problem, frontier, x, f, cf)
            if compare(problem, new, x): # TODO - figure out where elitism works and whether I need to make a "better" in problem....
                if new not in frontier:
                    x.objectives = deepcopy(new.objectives)
                    x.decisions  = deepcopy(new.decisions)
            """The below items can be added again if an early-out thing is implemented"""
            #total += x.objectives[0] # need a way to early out for multiple objectives
            #n = len(x.objectives)
        #return total, n
    
    def extrapolate(problem, frontier,one,f,cf):
        cr = 0.5
        retries = 5
        
        # pick one and know which one
        out = deepcopy(one)
        
        # pick three others
        two,three,four = threeOthers(frontier,one)
        changed = False
        
        #mutate the decisions of the three you picked (de/rand/1)
        for d in range(len(frontier[0].decisions)):
            retries = 5
            x,y,z = two.decisions[d], three.decisions[d], four.decisions[d]
            if random.random() < cr:
                changed = True
                new     = x + f*(y - z)
                out.decisions[d]  = trim(new, problem.decisions[d]) # keep in range
            if not changed:
                rand = random.choice([two, three, four])
                out.decisions[d] = rand.decisions[d]
            out.objectives = problem.evaluate(out) #TODO - will evaluate move to factory?
            retries -= 1
            if not problem.is_valid(out) and retries > 0:
                d -= 1 # retry this one if mutation is invalid
            if retries <= 0:
                print("WARNING - retries exceeded")
        return out
    
    def threeOthers(wholeset, leaveout=None): 
        def oneOther():
            retries = len(wholeset) - 1 # if you've tried everything in the set and can't get a valid subset, give up. (this assumes small sets)
            if len(seen) > 0:
                x = seen[0]
            while x in seen and retries > 0:
                x = random.choice(wholeset)
                retries -= 1
            if retries <= 0:
                print(len(seen), len(wholeset), leaveout)
                raise Exception("Pick three others failed.  Too many retries.")
                
            seen.append(x)
            return x
            
        seen = [leaveout]
        #seen = [x for x in leaveout]
        a = oneOther()
        b = oneOther()
        c = oneOther()
        return a, b, c
        
    #set magic parameters
    rounds=gens
    np=10*len(problem.decisions)
    #better = problem.better # not implemented
    f=0.75 # TODO - look up if the magic parameters are supposed to be set relative to the # of decisions or something (i.e. do these need to change)
    cf=0.3
    epsilon=0.01
    
    #generate initial population
    frontier = deepcopy(initial_population)
    
    #go
    for k in range(rounds):
      say(".")
      next_generation(problem, f, cf, frontier)
      #total, n = next_generation(problem, f, cf, frontier)
      """ABOVE - only setting equal to something if have an early-out condition
      implement some kind of early-out having to do with change from last generation?
      """
    return frontier


def __main():
  competitors = 3
  problem = POM3()
  pop_size = 20
  init_population = populate(problem, pop_size)
  # print(normalize(problem, ga(problem, init_population, retain_size=pop_size, gens=50, verbose=True)[1])[0])

class Company(O):
  def __init__(self, mydec, name):
    O.__init__(self, decisions=mydec, name=name)
  """
  def __init__(self, **kwargs):
    O.__init__(self, **kwargs)
  """
    
    
class POM3_Factory(O):
    def __init__(self, num_companies):
      companies = []
      
      problem = POM3()
      base_decisions = populate(problem, 1)
      
      # how many companies?
      for i in range(num_companies):
        problem = POM3()
        requirements = POM3.helper.initialization(4, 15) # need a better way to decide these values
        
        # set my decisions
        decisions = []
        mine = deepcopy(base_decisions[0])
        mine.decisions[7] = random_value(problem.decisions[7].low, problem.decisions[7].high)
        
        
        # set my beliefs on other peoples' decisions (at first same as mine except strategy is random)
        for k in range(num_companies-1):
          tmp = base_decisions[0].clone()
          tmp.decisions[7] = random_value(problem.decisions[7].low, problem.decisions[7].high)
          decisions.append(tmp)
          
        # Add the above to a "Company" entry
        companies.append(Company(mine, decisions, i, problem, requirements))
      O.__init__(self, companies=companies)

    def run_sim(self):
      sigs = [x.my_decisions.decisions[2] for x in self.companies]
      problem = POM3()
      print("So far, so good.")
      mytries = {}
      evaltries = []
      # for each of these companies, run the sim, return the top 3, display
      for c in self.companies:
        tmp = deepcopy(c.decisions)
        tmp.append(c.my_decisions)
        
        c.problem.helper.set_requirements(c.requirements)
        c.problem.helper.reset()
        c.problem.helper.establish_teams(tmp)
        c.problem.helper.reset_teams()
        results = c.problem.helper.simulate()
        for r in range(len(results)-1):
          c.decisions[r].objectives = results[r]
        c.my_decisions.objectives = results[-1]
        
        #need to remove duplicates(?)
        mytries[c.name] = c.my_decisions
        evaltries.append(c.my_decisions)
      
      
      print(elitism(problem, evaltries, 3, cdom))
    
    
    def variance_test(self, num_companies):
      results = []
      
      problem = POM3()
      requirements = POM3.helper.initialization(4, 50) # need a better way to decide these values
      problem.helper.set_requirements(requirements)
      
      # run 100 sims
      for i in range(num_companies):
        mine = [random_value(d.low, d.high) for d in problem.decisions]
        #self.companies.append(Company(mine, [], i, problem, requirements))
        cur = Company(Point(mine), [], i, problem, requirements)
        obj = problem.evaluate(cur.my_decisions)
        results.append(obj)
      # return min/max/std var/median/mean of each objective
      meds = numpy.median(results, axis=0)
      mins = numpy.amin(results, axis=0)
      maxs = numpy.amax(results, axis=0)
      means = numpy.mean(results, axis=0)
      stds = numpy.std(results, axis=0)
      print("Medians")
      print(meds)
      print("Minimums")
      print(mins)
      print("Maximums")
      print(maxs)
      print("Means")
      print(means)
      print("Standard Deviations")
      print(stds)

def optimize(method, num_companies, inp_population=None, retain_size=10, gens=100, dom_func=cdom, verbose=True):
  """Describe method here"""
  # I got one more problem
  problem = POM3()
  companies = []
  if method == 'de':
    method = de
  elif method == 'pso':
    method = pso
  elif method == 'cdomga':
    method = cdomga
  elif method == 'sampling':
    method = sampling
  else:
    method = de # add nsga2?
  requirements = POM3.helper.initialization(4, 15) # need a better way to decide these values  
  # NB - changed probability in POM3 requirements so it is far more likely to get cross-tree constraints
  
  # setup competition
  for i in range(num_companies):
    companies.append(Company([random_value(d.low, d.high) for d in problem.decisions], i))
  
  problem.add_competitors(companies)
  problem.set_requirements(requirements)
  
  # generate initial population    
  if inp_population is None:
    population = populate(problem, retain_size)
  else:
    population = [point.clone() for point in inp_population]
  for point in population:
    point.objectives = problem.evaluate(point)
  initial_population = [point.clone() for point in population]
  
  # run optimizer, do elitism on results (all optimizers return whole frontier/swarm)
  #intermediate = problem.final_evaluate(method(problem, initial_population, gens)) # final eval needed?
  intermediate = method(problem, initial_population, gens)
  population = elitism(problem, intermediate, 10, dom_func)
  
  return initial_population, population
  
  
if __name__ == "__main__":
  __main()