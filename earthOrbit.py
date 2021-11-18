from math import *
from vpython import *
#
# Needed Constants
# in m, m/s
sun_earth_distance = 149597870000
speed_of_earth = 29839.717

#
# Set up te displays
#
scene2 = canvas(title='Earth orbiting the Sun', caption='Animated Display',
                center=vector(0, 0, 0), background=color.black)
#
# Make the radius of each object large enough to see them
# earth: 1e9, sun: 5e9
earth = sphere(pos=vector(sun_earth_distance, 0, 0), radius=1e9, color=color.green)

sun = sphere(pos=vector(0, 0, 0), radius=5e9, color=color.yellow)
#
G = 6.67e-11
#
earth.mass = 5.972e24
sun.mass = 1.989e30
#
#
pct = 1
earth.momentum = earth.mass * vector(0, pct * speed_of_earth, 0)
sun.momentum = sun.mass * vector(0, 0, 0)
#
# Create a trail for the earth, and vectors for the force on the earth.
# scale should be a number that lets us see the force arrow on the plot.
#
earth.trail = curve(color=color.blue)
earth.trail.append(pos=earth.pos)
#


earth.point = arrow(pos=earth.pos, color=earth.color, axis=-norm(earth.pos))
scale = 3e-12

earth.p = arrow(pos=earth.pos, color=color.red, axis=norm(earth.momentum))
scale2 = 6e-19

#
# Initial time is 0, and the time step is twelve hours
#
time = 0
dt = 1 * 3600
#
# We will initially run for one year
# time < (3.15e7)

# earth.pos.equals(vector(sun_earth_distance,0,0))
while (time < (3.15e7)):
    # angle = diff_angle(earth.pos, vector(sun_earth_distance,0,0))

    # if((time > (3.15e7 / (150))) and (abs(angle) < 0.001) ):
    #   print(time/(3600*24))

    rate(100)

    time += dt

    r = earth.pos - sun.pos
    r2 = mag(r) ** 2
    #
    #  Compute the force on the earth using our force function.
    #
    earth.force = ((-(G * sun_earth_distance) * (sun.mass * earth.mass)) * (1 / (r2))) * norm(r)
    # earth.force = vector(-10, 0, 0)
    #
    #  Update the momentum and position of the Earth
    #
    earth.momentum += (earth.force * dt)
    earth.pos += (earth.momentum / earth.mass) * dt
    #
    #   Update the Earth's Momentum arrow
    #
    earth.trail.append(pos=earth.pos)
    earth.point.pos = earth.pos
    earth.point.axis = earth.force * scale

    earth.p.pos = earth.pos
    earth.p.axis = earth.momentum * scale2

#

days = time / (3600 * 24)
print('days', days)