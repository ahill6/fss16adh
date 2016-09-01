from swampy.TurtleWorld import *
from polygon import arc

world = TurtleWorld()
bob = Turtle()
bob.delay = 0.00001


def make_one(turtle, radius, angle):
    arc(turtle, radius, angle)
    lt(turtle, 180 - angle)
    arc(turtle, radius, angle)
    lt(turtle, 180 - angle)


def make_flower(turtle, petals, radius, a=None):

    # This angle will give a flower with n petals and no overlap
    angle = (a or 360.0 / petals)

    for i in xrange(petals):
        make_one(turtle, radius, angle)
        lt(turtle, 360.0 / petals)


def sneak(turtle, offset):
    """This moves the turtle without drawing a line.  This was added after seeing the author's code,
    and that he intended all three to be printed on a single screen (I originally just ran it three
    times with three windows"""
    pu(turtle)
    fd(turtle, offset)
    pd(turtle)


std_size = 60.0  #chosen to match the author's size in his "answers"
num_petals = 7

sneak(bob, -125)
make_flower(bob, num_petals, std_size)

sneak(bob, 125)
num_petals = 10
# The scaling on this one was changed manually to make it look the same size as the others (angle value from answers)
# TODO - Come up with a formula for automatically changing the size when the angle is changed for overlap
make_flower(bob, num_petals, std_size * 7.0 / 10.0, 80.0)


sneak(bob, 125)
num_petals = 20
make_flower(bob, num_petals, std_size * num_petals / 7.0) # 7.0 is used because I set the 7-petal flower as the base case

bob.die()

wait_for_user()
