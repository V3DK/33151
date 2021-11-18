from math import *
from vpython import *

#
# Set program constants
#
BobMass = 0.02
SpringConstant = 0.7
#0.02, 2 * ((SpringConstant * BobMass) ** 0.5)
DampingBeta = 0.03


graphType = 1
tMax = 25
InitialStretch = 0.2
EquilLength = 1
ExpectedPeriod = 2 * pi * sqrt(BobMass / SpringConstant)
#
scene2 = canvas(title='Damped Oscillator', caption='Animated Display',
                center=vector(0.50, 0, 0), background=color.white)
#
bob = sphere(pos=vector(0, 0, 0), radius=0.05, color=color.red)
wall = box(pos=vector(0, 0, 0), size=vector(0.05, .1, .1), color=color.blue)
spring = helix(pos=wall.pos, axis=bob.pos - wall.pos, radius=0.01, thickness=.004, coils=10, color=color.green)
#
# equilibrium position of the end of the spring.
#
length = vector(EquilLength, 0, 0)
stretch = vector(InitialStretch, 0, 0)
#
# Set the initial position of the bob
#
bob.pos = wall.pos + length + stretch
bob.mom = vector(0, 0, 0)
#
# Input Parameters needed in the program. Be sure to
# choose sensible values.
#
bob.mass = BobMass
spring.ks = SpringConstant
beta = DampingBeta

#
print('Damped Mass on a Spring')
#
# Time step and total elapsed time
#
dt = 0.005
t = 0.0
#
# Used to look for zero crossings to measure the period.
#
told = 0.0
xold = bob.pos.x
#
# Setup a graph window to plot things in
#
s = '<b>Mass and Spring: Graph</b>'
#
# Move the mouse over the graph to explore its interactivity.
# Drag a rectangle in the graph to zoom. Examine the icons at the upper right.
# Click the "Reset axes" icon to restore. Drag along the bottom or left to pan.
#

if(graphType):
    graph(title=s, xtitle='Time', ytitle='Energy', xmax=tMax, ymax=0.3, ymin=-0.3, x=0, y=500, width=750, height=450)
else:
    graph(title=s, xtitle='Time', ytitle='Energy', xmax=tMax, ymax=0.0145, ymin=0.0135, x=0, y=500, width=750, height=450)

#
drawit = gcurve(color=color.cyan, label='Position')
ke = gcurve(color=color.red, label='Kinetic Energy')
pe = gcurve(color=color.blue, label='Potential Energy')
te = gcurve(color=color.green, label='Total Energy')

#
#
while (t < tMax):
    rate(1000)
    t += dt
    #
    #    spring.stretch = block.pos-wall.pos
    #
    #drivingForce = vector(-0.1, 0 ,0)
    dampingForce = (-beta * (bob.mom / bob.mass))

    f0 = 1 * 0.15 * spring.ks * InitialStretch
    wd = 1 * 1 * sqrt(spring.ks / bob.mass)
    drivingForce = vector(-f0 * cos(t * wd), 0, 0)
    spring.force = (-(spring.ks) * (bob.pos - length))  + dampingForce + drivingForce

    bob.mom += spring.force * dt
    bob.pos += (bob.mom / bob.mass) * dt
    spring.axis = bob.pos - wall.pos
    #
    # Check for a zero crossing
    #
    xnew = bob.pos.x - wall.pos.x - length.x
    if xnew * xold <= 0:
        period = 2 * (t - told)
        if told != 0:
            scene2.caption = ('Expected period is: ', ExpectedPeriod, ' . Actual period is: ', period, '.')
        told = t
    xold = xnew
    #
    # Plot the x-coordinate of the block as a function of time.
    #
    xbob = bob.pos.x - length.x + wall.pos.x
    drawit.plot(pos=(t, xbob))

    kinEn = mag2(bob.mom) * (1 / (2 * bob.mass))
    ke.plot(pos=(t, kinEn))

    potEn = 0.5 * (spring.ks) * mag2(bob.pos - length)
    pe.plot(pos=(t, potEn))

    totEn = kinEn + potEn
    te.plot(pos=(t, totEn))

#
print("Expected Period (sec)", ExpectedPeriod)
print("Actual Period   (sec)", period)
print('All Done')