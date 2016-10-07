def flip(a):
    return not a
def dont(a):
    return a
g = dont

def better(a, b):
    return g(a<b)


print(better(1,4))