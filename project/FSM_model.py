import random

def shuffle(lst):
    """
    Shuffle a list and return it.
    """
    random.shuffle(lst)
    return lst

class O(object):
    """
    Basic Class which every other class inherits
    IS THIS NEEDED AT ALL????
    """
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    
    def __repr__(self):
        return self.__class__.__name__ + kv(self.__dict__)
        
        
class Company(O):
  """A representation of a single company.
  """
  def update_flows(self, new_decs):
    self.flows = SOMETHING(self.decisions, self.flows, new_decs)
    
  def update_stocks(self):
    self.stocks = SOMETHING-ELSE(self.decisions, )
    
  def step():
    asdfd
    
class Class_Factory():
  
  def update_companies(self):
    """Update stocks and 'flows' for all companies
    """
    for k in shuffle(self.companies):
      self.update_company(k)
    
    cross_update(self)
  
  def signaling(self):
    for k in self.companies:
      if k.signal:
        for j in self.companies:
          if k != j:
            # somehow update j.belief[k]
        
  def update_company(company):
    """Updates all variables that are dependent solely on the company itself
    """
    # update flows
    company.update_flows(new_decisions)
    
    #update stocks
    company.update_stocks()
    
  def cross_update(self):
    """Update the variables of each company that have dependencies in other companies
    """
    def validate_ttms(self):
      for k in self.companies:
        for j in self.companies:
          # make company.belief[itself] just be true ttm???
          #1) decide whether to believe them (probabilistically)
          #if random.random()*k.credulity < 0.75 
          #2) if guess right, set belief, else
          #3) if guess wrong, randomly pick lower or higher
    
    def update_product_coverage(self, comp1, comp2):
      val = features[comp1] - features[comp2]
      features_lacking_score = 0
      for x in val:
        features_lacking_score += feature_value[x]
        
      self.product_coverage[comp1][comp2] = features_lacking_score
      
      
      
    def feature_coverage(self):
      for k in self.companies:
        for j in self.companies:
          # this is more than needed, can do both a - b and b - a in the same update...how to do this only half the time???
          update_product_coverage(k, j)
    
  def model_step(self):
    for k in shuffle(self.companies):
      k.step()
    
    changed = self.signaling()
    
    if changed:
      for k in shuffle(self.companies):
        k.step()