class Employee(object):
    """Represents an employee.
    
    Attributes:
      name: string
      age:  int 
    """

    def __init__(self, name=None, age=None):
        self.name = name
        self.age = age

    def __repr__(self): 
        """Returns a string representation."""
        return '%s is age %s' % (self.name,
                             self.age)

    def __lt__(self, other):
        """Compares the ages of the two employees.
        """
        return self.age < other.age
