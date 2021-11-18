from math import *
from vpython import *

#
# Distance from Sun to Earth: 149,597,870 km
# Mass of the Sun:     1.989e30 kg
# Radius of the Sun:    695.5e6 m
# Mass of the Earth:   5.972e24 kg
# Radius of the Earth   6.371e6 m
# Distance Sun-Earth    149.578 e9 m
# Length of a year      3.15 e7 seconds
#t
# Set constants
#EarthSunDist = 149597870000
EarthSunDist = 149597870000

SpeedEarth   = 2 * pi * EarthSunDist / 3.15e7
#
# Make the radius of each object large enough to see them
#

earth=sphere(pos=vector(EarthSunDist,0,0),radius=7e9,color=color.green)
sun=sphere(pos=vector(0,0,0),radius=7e9,color=color.yellow)
#
G = 6.67e-11
#
earth.mass = 5.792e24
sun.mass = 1.989e30
#
# We speed this up by 25% to make an eliiptical orbit.
#
earth.speed = 1 * SpeedEarth
earth.momentum = earth.mass*vector(0,earth.speed,0)
#
#  We will now define three points about which we will compute the angular momentum.
#  The first is the sun (force center), the second is inside the orbit and the third
#  is outside the orbit.
#
point1 = sun.pos
point2 = 0.5*(earth.pos-sun.pos)
point3 = 2.0*(earth.pos-sun.pos)
#
#  We now create some arrows that will show the force acting on the Earth, the
#  momentum of the Earth, and the angular momentum about each of the three points.
#
forcearrow = arrow(shaftwidth=3e9,color=color.red)
momentumarrow = arrow(pos=earth.pos, axis=earth.momentum, shaftwidth=3e9,color=color.green)
#
angmomarr1 = arrow(pos=point1,shaftwidth=3e9,color=color.cyan)
angmomarr2 = arrow(pos=point2,shaftwidth=3e9,color=color.magenta)
angmomarr3 = arrow(pos=point3,shaftwidth=3e9,color=color.orange)
#
#  We can also define an arrow for the RungeLenz Vector

rungearr = arrow(pos=point1,shaftwidth=3e9,color=color.blue)

# set the time step to be one day (in seconds)
#
earth.trail = curve(color=color.white) #,retain=250)
#
time = 0
dt = 3600*12
year = 3.15e7
#
# Make a graph of the magnitude of the momentum
# Move the mouse over the graph to explore its interactivity.
# Drag a rectangle in the graph to zoom. Examine the icons at the upper right.
# Click the "Reset axes" icon to restore. Drag along the bottom or left to pan.
#
s='<b>Length of Angular Momentum</b>'
graph(title=s, xtitle='Time', ytitle='Angular Momentum',xmin=0,xmax=6*year,
      ymax=15, ymin=-5)
#
drawit1 = gcurve(color=color.cyan, label='About Sun')
drawit2 = gcurve(color=color.magenta, label='Inside Orbit')
drawit3 = gcurve(color=color.orange, label='Outside Orbit')
drawit4 = gcurve(color=color.blue, label='runge')
#
# We will run until we have returned to the initial position. We will check by comparing the polar
# angle of the objct:
# earth.angle = atan2(earth.pos.y,earth,pos.x)
# earth.oldangle = earth.angle
#
while True:
    rate(200)
#
    time = time + dt
#
    r = earth.pos - sun.pos
    r2 = mag(r) ** 2
    r3 = mag(r) ** 3

    earth.force = ((-(G) * (sun.mass * earth.mass)) * (1 / (r2))) * norm(r)
    #earth.force = vector(0,0,0)
    earth.momentum += (earth.force * dt)
    earth.pos += (earth.momentum / earth.mass) * dt


#
# Compute the angular momentum about each point.
#
    earth.angmom1 = cross(r, earth.momentum)
    earth.angmom2 = cross(earth.pos - point2, earth.momentum)
    earth.angmom3 = cross(earth.pos - point3, earth.momentum)
#
# Compute the Runge Lenz vector.
#  * (earth.mass ** 2)(sun.mass)(G))

    z = (earth.mass ** 2) * sun.mass * G

    rungelenz = cross(earth.momentum, earth.angmom1) - z * norm(r)
#
    momentumarrow.pos = earth.pos
    momentumarrow.axis = earth.momentum*1e-19
#
# set the arrow direction and length for the three angular momentum vectors.
#
    angmomarr1.axis = earth.angmom1*3e-30
    angmomarr2.axis = earth.angmom2*3e-30
    angmomarr3.axis = earth.angmom3*3e-30
#
    rungearr.axis = rungelenz*3e-59
#
# Update the force vector.
#
    forcearrow.pos  = earth.pos
    forcearrow.axis = earth.force*1e-12
#
# add a point to the trail
#
    earth.trail.append(pos=earth.pos)
#
# Get the length and sign of the three angular momentum vectors for
# graphing.
#

    mom1 = mag(earth.angmom1) * (1e-40)
    if earth.angmom1.z < 0:
        mom1 = -mom1
    mom2 = mag(earth.angmom2)*1e-40
    if earth.angmom2.z < 0:
        mom2 = -mom2
    mom3 = mag(earth.angmom3)*1e-40
    if earth.angmom3.z < 0:
        mom3 = -mom3

    r4 = mag(rungelenz)*1e-40 * (1 / 2.5e29)
    if rungelenz.z < 0:
        r4 = -r4

# Add the three lengths to the graph
    drawit1.plot(pos=(time,mom1))
    drawit2.plot(pos=(time,mom2))
    drawit3.plot(pos=(time,mom3))
    drawit4.plot(pos=(time,r4))


