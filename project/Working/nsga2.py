def ga(problem, inp_population=None, retain_size=10, gens=10, dom_func=cdom, verbose=False):
  #TODO - do the nsga domination function.
  population = [point.clone() for point in inp_population]
  
  for point in population:
    point.objectives = problem.evaluate(point)

  initial_population = [point.clone() for point in population]
  for _ in range(gens):
    if verbose: say(".")
    children = []
    for _ in range(retain_size):
      mom = random.choice(population)
      dad = random.choice(population)
      while mom == dad:
        dad = random.choice(population)
      child = mutate(problem, crossover(mom, dad))
      if problem.is_valid(child) and child not in population + children:
        children.append(child)
    population += children
    population = elitism(problem, population, retain_size, nsga_dom)
  if verbose: print("")
  return population