from __future__ import print_function
import random
from math import exp
import sys

def schaffer(x):
    return x**2 + (x-2)**2
    
def energy(x):
    min = 2.0
    max = 19210.0
    return (x - min) / (max - min)
    
def neighbor():
    return random.randint(-10000,10000)

def output(x): print(x, end="")

def P(current, next, heat):
    max = 199960004.0
    min = 2.0
    old = (current - min) / (max - min)
    new = (next - min) / (max - min)
    if heat != 0:
        return exp((old-new)/heat)
    """
    if heat != 0:
        return exp((current-next)/heat)
    else:
        print("heat = 0, divide by zero")
        print (current, next, heat)
        sys.exit()
    """
    
def run():
    kmax = 10000.0
    emin = 2
    current_state = random.randint(-10000,10000)
    #current_energy = energy(schaffer(current_state))
    current_energy = schaffer(current_state)
    best_state = current_state
    best_energy = current_energy
    k = 1
    
    # Run Simulated Annealer
    while (k < kmax and current_energy > emin):
        next_state = neighbor()
        #next_energy = energy(schaffer(next_state))
        next_energy = schaffer(next_state)
        if next_energy < best_energy:
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
    print("END")
    print(best_state)
    print(best_energy)
    #return best_state
            
            
def PCheck():
    kmax = 1000.0
    emin = 2
    current_state = random.randint(-10000,10000)
    #current_energy = energy(schaffer(current_state))
    current_energy = schaffer(current_state)
    best_state = current_state
    best_energy = current_energy
    k = 1
    
    # Run Simulated Annealer
    while (k < kmax and current_energy > emin):
        next_state = neighbor()
        #next_energy = energy(schaffer(next_state))
        next_energy = schaffer(next_state)
        P(current_energy, next_energy, k/kmax)
        k += 1

