from maxwalksat import Problem
from copy import deepcopy
from random import choice, random, randint
import sys, numpy

def compare(problem, a, b):
    """Returns True if a better than b by whatever measure (<, >, bdom, cdom).
    Automatically selects bdom if numbers are not scalars or a list of length 1
    (cdom not yet implemented).
    """
    a1 = problem.evaluate(problem, a)
    b1 = problem.evaluate(problem, b)
    if isinstance(a1, (list, tuple)) and len(a1) == 1:
        a1 = a1[0]
    if isinstance(b1, (list, tuple)) and len(b1) == 1:
        b1 = b1[0]
    try:
        if isinstance(a1+0.0,float) and isinstance(b1+0.0,float):
            return better(a1,b1)
    except:
        return bdom(a1, b1)

def bdom(x, y):
    """multi objective"""
    betters = 0
    if len(x) != len(y):
        raise IndexError("Error, two items have different lengths",x,y)
    for obj in xrange(len(x)):
        if x[obj] < y[obj] : betters += 1 # need to generalize so it can also handle >
        elif x[obj] != y[obj]: return False
    return betters > 0


def greaterthan(a, b):  return a > b
def lessthan(a, b): return a < b
def wrap(num, dec):    
    low, high = dec.low, dec.high
    return low if low==high else low + ((num - low) % (high - low))
def cap(num, dec):  return max(dec.low, min(dec.high, num))

"""
def cdom(a, b):
    raise NotImplementedException()
"""

# eventually, these should be read from a file
better = lessthan
trim = cap

def generate_population(self, needed):
    """Generate an initial swarm population (no duplicates) with velocities initialized to very small values (.0001% of range).
    Because PSO best influences all particles, actual best in initial population is also returned"""
    retries = 10*needed
    seen = []
    vel0 = []
    best_tmp = None
    while len(seen) < needed and retries > 0:
        x = self.generate_one()
        if not best_tmp:
            best_tmp = deepcopy(x)
        if x not in seen:
            seen.append(x)
            vel0.append([random()*(y.high-y.low)/100000.0 for y in self.decisions])
            if compare(self, x, best_tmp):
                best_tmp = deepcopy(x)
        else:
            retries -= 1
    if retries <= 0:
        raise Exception("Pick three others failed.  Too many retries.")
            
    return seen, vel0, best_tmp
    
def pso(datafile):
    #import model
    problem = Problem(datafile)
    location = []
    velocity = []
    
    #method setup
    iterations=100
    np=30 # number of particles
    #better = problem.better # not currently implemented
    
    #generate initial population
    swarm, velocity, best = generate_population(problem, np)
    
    velocity = numpy.array(velocity)
    best.objectives = problem.evaluate(problem, best)
    
    """the magic parameters below have been selected as follows:
    k - per suggestion from class notes
    w,p - engineering judgment (i.e. experimentation, took best values)
    """
    k = .1
    w = 3.0
    p = 4.1

    #run pso
    for i in range(iterations):
        for k in range(len(swarm)):
            # move, update asynchronously
            #velocity[k] = k*(w*velocity[k] + p1*(numpy.subtract(best.decisions, swarm[k].decisions)) + p2*(numpy.subtract(best.decisions, swarm[k].decisions)))
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
                #per_best = deepcopy(swarm[k])
                best = deepcopy(swarm[k])
    
    return swarm
    #return best # alternative if you don't want 30 results printing

