import random
r   = random.random
isa = isinstance

class Model:
  def state(self):
    """To create a state vector, we create 
    one slot for each name in 'have'."""
    tmp=self.have()
    for k,v in tmp.has().items():
      v.name = k
    return tmp 
    
  def run(self,dt=1,tmax=30):
    """For time up to 'tmax', increment 't' 
       by 'dt' and 'step' the model."""
    print("running")
    t,b4 = 0, o()
    keep = []    ## 1
    state = self.state()
    for k,a in state.items(): 
      b4[k] = a.init
    keys  = sorted(state.keys(),  ## 3
                   key=lambda z: state[z].rank())
    keep = [["t"] +  keys,
            [0] + b4.asList(keys)]
    while t < tmax:
      now = b4.copy()
      self.step(dt,t,b4,now)
      for k in state.keys(): 
        now[k] = state[k].restrain(now[k]) ## 4
      keep += [[t] + now.asList(keys)] ## 2
      t += dt
      b4 = now
    return keep
    
class o:
  """Emulate Javascript's uber simple objects.
  Note my convention: I use "`i`" not "`this`."""
  def has(self)             : return self.__dict__
  def keys(self)            : return self.has().keys()
  def items(self)           : return self.has().items()
  def __init__(self,**d)    : self.has().update(d)
  def __setitem__(self,k,v) : self.has()[k] = v
  def __getitem__(self,k)   : return self.has()[k]
  def __repr__(self)        : return 'o'+str(self.has())
  def copy(self): 
      j = o()
      for k in self.has(): j[k] = self[k]
      return j
      
  def asList(self,keys=[]):
    keys = keys or self.keys()
    return [self[k] for k in keys]
    
class Diapers(Model):

  def have(self):
    return o(C = S(100), D = S(0),
             q = F(0),  r = F(8), s = F(0))

  def step(self,dt,t,u,v):
    def saturday(x): return int(x) % 7 == 6
    v.C +=  dt*(u.q - u.r)
    v.D +=  dt*(u.r - u.s)
    v.q  =  70  if saturday(t) else 0 
    v.s  =  u.D if saturday(t) else 0
    if t == 27: # special case (the day i forget)
      v.s = 0
          
class ProductFight(Model):
  def __init__(self, filename):
    self.competitors = 1
    self.allfeatures = set('abcdefghijklmnop')
    print("Starting ProductFight")
    
  def have(self):
    return o(myFeatures = S(self.initializeFeatures(2)), theirFeatures = S(self.initializeFeatures(2)), 
              TTM = A(0), cost = S(0),
              workNewFeatures = F(1),  workExistingFeatures = F(1), haste = F(0), signaling = F(0), ttmCost = F(0.5), 
              workExistingTTM = F(0.5), workNewTTM = F(0.5), theirFeaturesCost = F(0.5), newFeatCost = F(0.5))
  
  def initializeFeatures(self, n):
    featureset = random.sample(self.allfeatures, n)
    return featureset
    
  def step(self,dt,t,u,v):
    #u where it is starting this timestep
    #v where it is after this timestep
    v.myFeatures = dt*(u.workNewFeatures) # maybe change this a bit, add random
    v.theirFeatures = dt*(u.workExistingFeatures) # likewise, change and jiggle (less)
    v.cost = dt*(u.newFeatCost + u.theirFeaturesCost - u.ttmCost)
    
    v.TTM = dt*(u.workExistingTTM + u.workNewTTM + u.haste)
    
      
class Has:
  def __init__(self,init,lo=0,hi=100):
    self.init,self.lo,self.hi = init,lo,hi
    
  def restrain(self,x):
    return max(self.lo, 
               min(self.hi, x))
  
  def rank(self): 
    "Trick to sort together columns of the same type."
    return 0
  
  def __repr__(self):
    return str(dict(what=self.__class__.__name__,
                name= self.name,init= self.init,
                 lo  = self.lo,  hi  = self.hi))

class Flow(Has) :
  def rank(self): return 3
class Stock(Has):
  def rank(self): return 1
class Aux(Has)  :
  def rank(self): return 2

S,A,F = Stock, Aux, Flow  

def printm(matrix,less=True):
   """Print a list of list, only showing changes
   in each column (if less is True)."""
   def ditto(m,mark="."):
     def worker(lst):
       out = []
       for i,now in enumerate(lst):
         before = old.get(i,None) # get old it if exists
         out += [mark if before == now else now]
         old[i] = now # next time, 'now' is the 'old' value
       return out # the lst with ditto marks inserted
     old = {}
     return [worker(row) for row in m]
   matrix = ditto(matrix) if less else matrix
   s = [[str(e) for e in row] for row in matrix]
   lens = [max(map(len, col)) for col in zip(*s)]
   fmt = ' | '.join('{{:{}}}'.format(x) for x in lens)
   for row in [fmt.format(*row) for row in s]:
      print(row)
      
      
def _diapers1():
  #d = Diapers()
  #printm(d.run())
  f = ProductFight('fil')
  printm(f.run())
  

_diapers1()