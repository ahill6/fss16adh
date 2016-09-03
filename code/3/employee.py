class Employee(object):
    """Represents an employee.
    
    Attributes:
      name: string
      age:  int 
      TODO - Replace age with birthdate and calculate age when desired
    """

    def __init__(self, name=None, age=None):
        self.name = name
        self.age = age

    def __repr__(self): 
        """Returns a string representation."""
        return '%s is age %s' % (self.name,
                             self.age)

    def __lt__(self, other):
        """Compares this card to other, first by age, then name (as a tiebreaker).
        """
        
        t1 = self.age, self.name
        t2 = other.age, other.name
        return cmp(t1, t2)  #figure out how exactly this code works

