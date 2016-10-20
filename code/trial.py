import random
names = ["Culture", "Criticality", "Criticality Modifier", "Initial Known", 
         "Inter-Dependency", "Dynamism", "Size", "Plan", "Team Size"]
lows = [0.1, 0.82, 2, 0.40, 1, 1, 0, 0, 1]
highs = [0.9, 1.20, 10, 0.70, 100, 50, 4, 5, 44]
# TODO 2: Use names, lows and highs defined above to code up decision
# and objective metadata for POM3.
#decisions = [Problem(n,l,w) for n,l,w,i in enumerate(zip(names, lows, highs))]
#[sum(x) for x in zip(*C)]
#print([n,l,h for n,l,h in zip(names, lows, highs)])

#for n, l, h in zip(names, lows, highs):
#        decisions.append
"""
lst = ['a', 'b', 'c', 'd']
print(not not lst)

#300 variables, each binary

# 1) Open file
f = open('binaries.csv', 'w')
# 2) 300 times for a line, make random binaries with different distributions
for y in range(1000):
    for x in range(299):
        a = 1 if random.random() < 1/(x//20 + 2.0) else 0
        f.write(str(a) + ",")
    b = 1 if random.random() < .67 else 0    
    f.write(str(b) + "\n")
# 4) Close file
f.close()
"""
