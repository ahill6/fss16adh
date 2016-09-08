import random

def birthday_freq(birthdays):
    """ My original implementation to solve the problem (and other related problems)"""
    d = dict()
    for b in birthdays:
        if b not in d:
            d[b] = 1
        else:
            d[b] += 1
    return d
    
def has_duplicates(birthdays):
    """ My dictionary method is not nearly as efficient as the author's solution, 
    so I implemented his as well"""
    tmp = birthdays[:]
    tmp.sort()
    for i in range(len(tmp)-1):
        if tmp[i] == tmp[i+1]:
            return True
    return False
    
def gen_rand_birthday(n):
    lst = []
    for i in range(n):
        lst += [random.randint(1,365)]
    return lst