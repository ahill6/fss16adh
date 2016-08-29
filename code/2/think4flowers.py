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

    angle = (a or 360.0 / petals)

    print(angle)

    for i in xrange(petals):
        make_one(turtle, radius, angle)
        lt(turtle, 360.0 / petals)


def sneak(turtle, offset):
    pu(turtle)
    fd(turtle, offset)
    pd(turtle)


std_size = 60.0
num_petals = 7

sneak(bob, -125)
make_flower(bob, num_petals, std_size)

sneak(bob, 125)
num_petals = 10
make_flower(bob, num_petals, std_size * num_petals / 10.0, 80.0)  # TODO how to correctly scale when the angle has been changed?
# The scaling on this one was changed manually to make it look the same size as the others (angle value from answers)


sneak(bob, 125)
num_petals = 20
make_flower(bob, num_petals, std_size * num_petals / 7.0)

bob.die()

wait_for_user()
