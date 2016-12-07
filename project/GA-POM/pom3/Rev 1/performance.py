#%matplotlib inline
# All the imports
from __future__ import print_function, division
from math import sqrt
from scipy.spatial import distance
import pom3_ga, sys, sim
import pickle

# TODO 1: Enter your unity ID here 
__author__ = "ahill6"

def normalize(problem, points):
  """
  Normalize all the objectives
  in each point and return them
  TODO 2: Normalization removes bias toward variables with larger values (level the playing field)
  """
  meta = problem.objectives
  all_objs = []
  for point in points:
    objs = []
    for i, o in enumerate(problem.evaluate(point)):
      low, high = meta[i].low, meta[i].high
      if high == low: 
          objs.append(0)
          continue
      else:
          objs.append((o - low)/(high-low))
      # TODO 3: Normalize 'o' between 'low' and 'high'; Then add the normalized value to 'objs'
    all_objs.append(objs)
  return all_objs
 
"""
Performing experiments for [5, 10, 50] generations.
"""
#problem = pom3_ga.POM3(3)
#pop_size = 10
#repeats = 10
#test_gens = [5, 10, 50]

def save_data(file_name, data):
  """
  Save 'data' to 'file_name.pkl'
  """
  with open(file_name + ".pkl", 'wb') as f:
    pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)
    
def load_data(file_name):
  """
  Retrieve data from 'file_name.pkl'
  """
  with open(file_name + ".pkl", 'rb') as f:
    return pickle.load(f)

def build(problem, pop_size, repeats, test_gens):
  """
  Repeat the experiment for 'repeats' number of repeats for each value in 'test_gens'
  """
  tests = {t: [] for t in test_gens}
  tests[0] = [] # For Initial Population
  for _ in range(repeats):
    init_population = pom3_ga.populate(problem, pop_size)
    pom3_ga.say(".")
    for gens in test_gens:
      tests[gens].append(normalize(problem, pom3_ga.ga(problem, init_population, retain_size=pop_size, gens=gens)[1]))
    tests[0].append(normalize(problem, init_population))
  print("\nCompleted")
  return tests

"""
Repeat Experiments
"""
# tests = build(problem, pop_size, repeats, test_gens)

"""
Save Experiment Data into a file
"""
# save_data("dump", tests)

"""
Load the experimented data from dump.
"""
#tests = load_data("dump")

def make_reference(problem, *fronts):
  """
  Make a reference set comparing all the fronts.
  Here the comparison we use is bdom. It can
  be altered to use cdom as well
  """
  retain_size = len(fronts[0])
  reference = []
  for front in fronts:
    reference+=front

  def bdom(one, two):
    """
    Return True if 'one' dominates 'two'
    else return False
    :param one - [pt1_obj1, pt1_obj2, pt1_obj3, pt1_obj4]
    :param two - [pt2_obj1, pt2_obj2, pt2_obj3, pt2_obj4]
    """
    dominates = False
    for i, obj in enumerate(problem.objectives):
      gt, lt = pom3_ga.gt, pom3_ga.lt
      better = lt if obj.do_minimize else gt
      if better(one[i], two[i]):
          dominates = True
      elif one[i] != two[i]:
          return False
      # TODO 4: Use the varaibles declared above to check if one dominates two
    return dominates
  
  def fitness(one, dom):
    return len([1 for another in reference if dom(one, another)])
  
  fitnesses = []
  for point in reference:
    fitnesses.append((fitness(point, bdom), point))
  reference = [tup[1] for tup in sorted(fitnesses, reverse=True)]
  return reference[:retain_size]
    
#make_reference(problem, tests[5][0], tests[10][0], tests[50][0])

def eucledian(one, two):
  """
  Compute Eucledian Distance between
  2 vectors. We assume the input vectors
  are normalized.
  :param one: Vector 1
  :param two: Vector 2
  :return:
  """
  # TODO 5: Code up the eucledian distance. https://en.wikipedia.org/wiki/Euclidean_distance
  return sum([(o-t)**2 for o, t in zip(one, two)])

def sort_solutions(solutions):
  """
  Sort a list of list before computing spread
  """
  def sorter(lst):
    m = len(lst)
    weights = reversed([10 ** i for i in xrange(m)])
    return sum([element * weight for element, weight in zip(lst, weights)])
  return sorted(solutions, key=sorter)


def closest(one, many):
  min_dist = sys.maxint
  closest_point = None
  for this in many:
    dist = eucledian(this, one)
    if dist < min_dist:
      min_dist = dist
      closest_point = this
  return min_dist, closest_point

def spread(obtained, ideals):
  """
  Calculate the spread (a.k.a diversity)
  for a set of solutions
  """
  s_obtained = sort_solutions(obtained)
  s_ideals = sort_solutions(ideals)
  d_f = closest(s_ideals[0], s_obtained)[0]
  d_l = closest(s_ideals[-1], s_obtained)[0]
  n = len(s_ideals)
  distances = []
  for i in range(len(s_obtained)-1):
    distances.append(eucledian(s_obtained[i], s_obtained[i+1]))
  d_bar = sum(distances)/len(distances)
  # TODO 6: Compute the value of spread using the definition defined in the previous cell.
  delta = (d_f + d_l + sum([abs(x - d_bar) for x in distances]))/(d_f + d_l + (n-1)*d_bar)
  return delta


#ref = make_reference(problem, tests[5][0], tests[10][0], tests[50][0])

"""
print(spread(tests[5][0], ref))
print(spread(tests[10][0], ref))
print(spread(tests[50][0], ref))
"""

def igd(obtained, ideals):
  """
  Compute the IGD for a
  set of solutions
  :param obtained: Obtained pareto front
  :param ideals: Ideal pareto front
  :return:
  """
  # TODO 7: Compute the value of IGD using the definition defined in the previous cell.
  ## 2-0, 4-2, 5-1, 9-1
  return sum([closest(got, ideals)[0] for got in obtained])/len(obtained)

#ref = make_reference(problem, tests[5][0], tests[10][0], tests[50][0])

"""
print(igd(tests[5][0], ref))
print(igd(tests[10][0], ref))
print(igd(tests[50][0], ref))
"""

import sk
sk = reload(sk)

def format_for_sk(problem, data, measure):
  """
  Convert the experiment data into the format
  required for sk.py and computet the desired
  'measure' for all the data.
  """
  gens = data.keys()
  reps = len(data[gens[0]])
  measured = {gen:["gens_%d"%gen] for gen in gens}
  for i in range(reps):
    ref_args = [data[gen][i] for gen in gens]
    ref = make_reference(problem, *ref_args)
    for gen in gens:
      measured[gen].append(measure(data[gen][i], ref))
  return measured

def report(problem, tests, measure):
  measured = format_for_sk(problem, tests, measure).values()
  sk.rdivDemo(measured)

"""
print("*** IGD ***")
report(problem, tests, igd)
print("\n*** Spread ***")
report(problem, tests, spread)
"""
"""
problem = pom3_ga.POM3()
results = pom3_ga.runTest(problem)
print(results[0])
print("\n\n")
print(results[1])
"""

#a.run_sim()
#a.sim_with_signaling()
#a.variance_test(100)
methods = ['de', 'nsga2', 'pso', 'sampling']
companies = 3
# de still not working for some reason (just finishes with starting points in different order)
a, b = sim.optimize('sampling', companies)
sums = [0 for y in range(len(a[0].objectives))]
sums_final = [0 for y in range(len(b[0].objectives))]
count = 0

for x in range(len(a)):
  for y in range(len(a[x].objectives)):
    sums[y] += a[x].objectives[y]
    sums_final[y] += b[x].objectives[y]
    count += 1

for x in sums:
  x /= count
for y in sums_final:
  y /= count

print("\n")
print(sums)
print("\n")
print(sums_final)