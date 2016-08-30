class Employee(object):
    """Represents an employee.
    
    Attributes:
      name: string
      age:  int 
      TODO - Replace age with birthdate and calculate age when desired
    """

    def __init__(self, name=None, age=None):
        self.suit = suit
        self.rank = rank

    def __str__(self): # according to online documentation, __repr__ is for machine-readable output, __str__ for human-readable
        """Returns a human-readable string representation."""
        return '%s is age %s' % (Employee.name,
                             Employee.age)

    def __lt__(self, other):
        """Compares this card to other, first by age, then name (as a tiebreaker).
        """
        
        t1 = self.age, self.name
        t2 = other.age, other.name
        return lt(t1, t2)  #figure out how exactly this code works

