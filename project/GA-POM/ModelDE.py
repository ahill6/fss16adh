from copy import deepcopy
from random import choice, random
"""
Basic Differential Evolution implementation.
"""

def de(problem, initial_population):
    
    #set magic parameters
    rounds=100
    np=10*len(problem.decisions)
    #better = problem.better # not implemented
    f=0.75 # TODO - look up if the magic parameters are supposed to be set relative to the # of decisions or something (i.e. do these need to change)
    cf=0.3
    epsilon=0.01
    
    #generate initial population
    frontier = initial_population 
    
    #go
    for k in range(rounds):
        next_generation(problem, f, cf, frontier)
        #total, n = next_generation(problem, f, cf, frontier)
        """ABOVE - only setting equal to something if have an early-out condition
        implement some kind of early-out having to do with change from last generation?
        """
    front_again_count = 0
    counter = 0
    return frontier

def next_generation(problem, f, cf, frontier, total=0.0, n=0):
    """Calculates next generation"""
    global front_again_count
    for x in frontier:
        new = extrapolate(problem, frontier, x, f, cf)
        if compare(problem, new, x): # TODO - figure out where elitism works and whether I need to make a "better" in problem....
            if new not in frontier:
                front_again_count += 1
                x.objectives = deepcopy(new.objectives)
                x.decisions  = deepcopy(new.decisions)
        """The below items can be added again if an early-out thing is implemented"""
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
        out.objectives = problem.evaluate(problem, out) #TODO - will evaluate move to factory?
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
    