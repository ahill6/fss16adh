from maxwalksat import Problem
from copy import deepcopy
from random import choice, random
"""
1) import model (including setting all variables, constraints, objectives, bounds, et al.)
2) make the DE basic operation
3) 
TODO - figure out how to find the "difference" between non-numeric values
TODO - make a general <, >, <=, >=, bdom, cdom thing (i.e. set one variable/pass in "better w.r.t WHAT")
"""

def greaterthan(a, b):  return a > b
def lessthan(a, b): return a < b
def wrap(num, dec):    
    low, high = dec.low, dec.high
    return low if low==high else low + ((num - low) % (high - low))
def cap(num, dec):  return max(dec.low, min(dec.high, num))
"""
def bdom(a, b):
    adf
def cdom(a, b):
    adfasd
"""
better = lessthan
trim = cap

def diffevolve(datafile):
    #import model
    problem = Problem(datafile)
    max=100
    np=10*len(problem.decisions)
    #better = problem.better # this assumes there is a single objective fitness function...which there better be or how are you evaluating things....?
    f=0.75
    cf=0.3
    epsilon=0.01
    
    #generate initial population
    frontier = [problem.generate_one() for _ in range(np)] 
    
    #go
    for k in range(max):
        total, n = next_generation(problem, f, cf, frontier)
        print(total, n)
        if total/n > (1-epsilon): # need to change this to allow bdom/cdom
            return frontier
        #ideally put some type of intermediate output here
    return frontier

def next_generation(problem, f, cf, frontier, total=0.0, n=0):
    for x in frontier:
        s   = problem.evaluate(problem, x)
        new = extrapolate(problem, frontier, x, f, cf)
        if better(new.objectives, s):
            x.objectives = deepcopy(new.objectives)
            x.decisions  = deepcopy(new.decisions)
        total += x.objectives[0] # this would need to change if >1 objective
        n     += 1
    return total, n

def extrapolate(problem, frontier,one,f,cf):
    cr = 0.5
    # make a copy of what you have, pick one and know which one
    out = deepcopy(one)
    
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
        # I do problem.evaluate for this, but didn't pass in problem.
        out.objectives = problem.evaluate(problem, out) # remember to score it
    return out

def threeOthers(wholeset, leaveout): # figure out how to generalize this so it works whether or not you want some left out (this in fact only works if you want exactly one left out)
    """
    if 3 < len(wholeset) - len(leaveout):
        raise Error("Fewer than three elements")
    """
    def oneOther():
        x = leaveout
        while x in seen:
            x = choice(wholeset)
        seen.append(x)
        return x
    seen = [leaveout]
    a = oneOther()
    b = oneOther()
    c = oneOther()
    return a, b, c
    