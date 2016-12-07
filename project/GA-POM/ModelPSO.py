from maxwalksat import Problem
from copy import deepcopy
from random import choice, random, randint
import sys, numpy

def wrap(num, dec):    
    low, high = dec.low, dec.high
    return low if low==high else low + ((num - low) % (high - low))
def cap(num, dec):  return max(dec.low, min(dec.high, num))

def generate_velocity(problem, needed):
    """Generate initial swarm velocities with very small values (< .0001% of range).
    """
    return [[random()*(y.high-y.low)/100000.0 for y in problem.decisions] for k in range(needed)]
    
def pso(problem, initial_population, iterations=100, trim=cap):
    location = []
    velocity = []
    swarm = deepcopy(initial_population)
    #generate initial population
    velocity = generate_velocity(problem, len(swarm))
    best = elitism(problem, swarm, 1, cdom)
    
    velocity = numpy.array(velocity)
    best.objectives = problem.evaluate(problem, best)
    
    """the magic parameters below have been selected as follows:
    k - per suggestion from class notes
    w,p - engineering judgment (i.e. experimentation, took best values)
    """
    k = .1
    w = 3.0
    p = 4.1  # see if these need to be changed (based on problem size/number of decisions??)

    #run pso
    for i in range(iterations):
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
                best = deepcopy(swarm[k])
    
    return swarm

