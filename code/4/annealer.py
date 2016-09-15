from __future__ import print_function
import random, sys
from math import exp

def schaffer(x):
    return x**2 + (x-2)**2
    
def energy(f, x):
    return f(x) # scaling is not needed for the optimizer, but for the heat/probability calculation
    
def neighbor():
    return random.randint(-100, 100) # This value was semi-arbitrary, as chosen because it is 1% of domain

def output(x): print(x, end="")

def P(current, next, heat):
    max = 199960004.0 
    min = 2.0
    old = (current - min) / (max - min)
    new = (next - min) / (max - min)
    
    if heat != 0:
        return exp((old-new)/heat)
    else:
        print("heat = 0, divide by zero")
        print (current, next, heat)
        sys.exit()
        
def move(cur):
    return cur + neighbor()
    
def run():
    kmax = 1000.0
    emin = 3
    opt_func = schaffer
    current_state = random.randint(-10000,10000)
    current_energy = energy(opt_func, current_state)
    best_state = current_state
    best_energy = current_energy
    k = 1
    
    # Run Simulated Annealer
    while (k < kmax and current_energy > emin):
        next_state = move(current_state)
        next_energy = energy(opt_func, next_state)
        if next_energy < best_energy:
            current_state = next_state
            current_energy = next_energy
            best_state = next_state
            best_energy = next_energy
            output("!")
        elif next_energy < current_energy:
            current_state = next_state
            current_energy = next_energy
            output("+")
        elif P(current_energy, next_energy, k/kmax) < random.random():
            current_state = next_state
            current_energy = next_energy
            output("?")
        else:
            output(".")
        k += 1
        if k%25 == 0:
            print("\t", best_state, best_energy)
            
    print("\nEnded at", k)
    print("state \t", best_state)
    print("energy\t", best_energy)
    #return best_state