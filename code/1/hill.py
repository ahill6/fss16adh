def printname():
  print("Andrew Hill")

"""
def repeat(f,n):
  for i in xrange(n):
    f()
"""

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

  
  
  
