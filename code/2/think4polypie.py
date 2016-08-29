"""Add some type of "I wrote this, thanks to XX"
Mention that I didn't think it was necessary to draw them all on the same graph until looking at the answer key,
so sneak and the print to file part were added later."""

from swampy.TurtleWorld import *
from polygon import polygon
from math import cos, radians
# TODO clean up code, see if things can be improved, add documentation
world = TurtleWorld()
bob = Turtle()
bob.delay = 0.0001

def polygon_pie(turtle, num_sides, side_length):
    """Creates a pie-sliced polygon by first reusing the polygon method from polygon, then filling in the interior"""
    polygon(bob, num_sides, side_length)
    polypie_interior(bob, num_sides, side_length)

def polypie_interior(turtle, num_sides, side_length):
    """Fills in the interior radii of a polygon"""
    interior_degrees = 180* (num_sides-2)
    angle = interior_degrees/num_sides

    interior_length = (.5*side_length)/(cos(radians(.5*angle)))


    lt(turtle, .5*angle)
    fd(turtle, interior_length)

    for i in xrange(num_sides-1):
        lt(turtle, angle)
        fd(turtle, interior_length)
        lt(turtle, 180)
        fd(turtle, interior_length)

    pu(turtle)
    lt(turtle, angle)
    fd(turtle, interior_length)
    lt(turtle, 180-.5*angle)
    pd(turtle)


def sneak(turtle, offset):
    pu(turtle)
    fd(turtle, offset)
    pd(turtle)


std_size = 200.0

sneak(bob, -125) # The offset amount is chosen to match the value of std_size
polygon_pie(bob, 5, std_size/5.0)

sneak(bob, 125)
polygon_pie(bob, 6, std_size/6.0)

sneak(bob, 125)
polygon_pie(bob, 7, std_size/7.0)

bob.die()

wait_for_user()
