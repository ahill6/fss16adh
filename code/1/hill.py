import random

def test4():
  "Did I pick a random number above .5?"
  a = random.random()
  return a
  
  
def test5():
  print "I'm a lumberjack, and I'm okay"
  print "I sleep all night and I work all day"
  #return 1
  
def repeat(f,n):
  for i in xrange(n):
    f()
    
def isbackward(a, b):
  if len(a) != len(b):
    return False
  index = 0
  while index < len(a):
    print index, a[index], b[-index]
    if a[index] != b[(len(b)-1)-index]:
      return False
    index+=1
  return True
  
  
  
  
  
