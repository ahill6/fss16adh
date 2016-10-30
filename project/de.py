from structures import Problem
from copy import deepcopy
from random import choice, random
"""
Basic Differential Evolution implementation.
"""

#helper methods
def greaterthan(a, b):  return a > b
def lessthan(a, b): return a < b
def wrap(num, dec):    
    low, high = dec.low, dec.high
    return low if low==high else low + ((num - low) % (high - low))
def cap(num, dec):  return max(dec.low, min(dec.high, num))

def compare(problem, a, b):
    """Returns True if a better than b by whatever measure (<, >, bdom, cdom).
    Automatically selects bdom if numbers are not scalars or a list of length 1
    (cdom not yet implemented).
    """
    a1 = problem.evaluate(a).objectives
    b1 = problem.evaluate(b).objectives
    if isinstance(a1, (list, tuple)) and len(a1) == 1:
        a1 = a1[0]
    if isinstance(b1, (list, tuple)) and len(b1) == 1:
        b1 = b1[0]
    try:
        if isinstance(a1+0.0,float) and isinstance(b1+0.0,float):
            return better(problem, a1,b1)
    except:
        return bdom(problem, a1, b1)

def bdom(problem, x, y):
    """multi objective"""
    betters = 0
    if len(x) != len(y):
        raise IndexError("Error, two items have different lengths",x,y)
    for obj in xrange(len(x)):
        bdombetter = lessthan if problem.objectives[obj].do_minimize else greaterthan
        if bdombetter(x[obj], y[obj]): betters += 1
        elif x[obj] != y[obj]: return False
    return betters > 0

# settings and variables for information    
better = lessthan
trim = cap
counter = 0 # tracking program executions for debugging
front_again_count = 0 # counting restarts for information

def diffevolve(datafile, num_players=0):
    #import model
    problem = Problem(datafile, num_players)
    
    #set magic parameters
    max=100
    np=10*len(problem.decisions)
    #better = problem.better # not implemented
    f=0.75
    cf=0.3
    epsilon=0.01
    
    #generate initial population
    frontier = problem.generate_pop(np) 
    
    #go
    for k in range(max):
        #total, n = next_generation(problem, f, cf, frontier)
        next_generation(problem, f, cf, frontier)
        """
        if total/n > (1-epsilon): # need something that would work for bdom/cdom too for early out
            return frontier
        """
    front_again_count = 0
    counter = 0
    return frontier

def next_generation(problem, f, cf, frontier, total=0.0, n=0):
    """Calculates next generation"""
    global front_again_count
    for x in frontier:
        new = extrapolate(problem, frontier, x, f, cf)
        if compare(problem, new, x):
            if new not in frontier and problem.is_valid(problem, new):
                front_again_count += 1
                x.objectives = deepcopy(new.objectives)
                x.decisions  = deepcopy(new.decisions)
        
        #total += x.objectives[0] # need a way to early out for multiple objectives
        #n = len(x.objectives)
    #return total, n

def extrapolate(problem, frontier,one,f,cf):
    global counter
    cr = 0.5
    retries = 5
    
    # pick one and know which one
    out = deepcopy(one)
    counter += 1
    
    # pick three others
    two,three,four = threeOthers(frontier,one)
    changed = False
    
    #mutate the decisions of the three you picked (de/rand/1)
    for d in range(len(frontier[0].decisions)):
        x,y,z = two.decisions[d], three.decisions[d], four.decisions[d]
        if random() < cr:
            changed = True
            new     = x + f*(y - z)
            out.decisions[d]  = trim(new, problem.decisions[d]) # keep in range
        if not changed:
            rand = choice([two, three, four])
            out.decisions[d] = rand.decisions[d]
        out = problem.evaluate(out)
        if not problem.is_valid(problem, out) and retries > 0:
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
            x = choice(wholeset)
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
    