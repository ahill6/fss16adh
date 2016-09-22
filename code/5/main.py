#import localio
import sys, maxwalksat


"""
def tester(f):
    for item in f:
        if not eval(item):
            return False
    return True
"""
"""
def evaluate():
    print("1")
    sys.exit(0)
    objectives = [Objective("a**2 + (b-2)**2", "a**2 + (b-2)**2", do_minimize=True)]
    decisions = [Decision('a', -100, 100),Decision('b', -100, 100)]
    sol = [95, -10]
    print("here")
    y = []
    for i in xrange(len(decisions)):
        y.append(decisions[i].name)
    tmp = zip(y, sol)
    print("there")
    thismodule = sys.modules[__name__]
    
    for key, value in tmp:
        setattr(thismodule, key, value)
    print("almost")
    ener = []
    for obj in objectives:
        ener.append(eval(obj.func))
    sol = ener
    print("done")
    return sol
"""    
print("\n",maxwalksat.mws())