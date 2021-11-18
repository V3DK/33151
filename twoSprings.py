from vpython import *
from math import *

#
# Initialize so spring properties. All units are assumed to be
# in MKS units.
#
spring_constantL = 10
spring_constantR = 10
equil_length    = 0.5


#amplitude
initial_stretch = 0.2
bob_mass        = 0.01
#
# Set up the animation canvas where we display the mass on the spring.
#
scene2 = canvas(title='Mass on a Spring',caption='Animated Display',
     center=vector(equil_length,0,0), background=color.white)
#
# Set up the wallLeft, spring and mass
#

wallLeft = box(pos=vector(0,0,0),size=vector(0.01,.2,.2),color=color.cyan)
wallRight = box(pos=vector(2 * equil_length,0,0),size=vector(0.01,.2,.2),color=color.cyan)
bob  = box(pos=vector(0,0,0),size=vector(.05,.05,.05),color=color.red)
springLeft = helix(pos=wallLeft.pos,axis=bob.pos-wallLeft.pos,radius=0.01,thickness=.01,coils=10,color=color.green)
springRight = helix(pos=wallRight.pos,axis=bob.pos-wallRight.pos,radius=0.01,thickness=.01,coils=10,color=color.green)

#
# equilibrium position of the end of the spring.
#
springLeft.equil = vector(equil_length,0,0)
springRight.equil = vector(equil_length,0,0)
bob.pos = wallLeft.pos + springLeft.equil + vector(initial_stretch,0,0)
#
# Input Parameters needed in the program. Be sure to
# choose sensible values.
#
bob.mass  = bob_mass
bob.mom   = vector(0,0,0)
springLeft.ks = spring_constantL
springRight.ks = spring_constantR
dt = 0.005
t  = 0.0

#
scene.autoscale = 0           # Turn off auto scaling
#
# Setup a graph window to plot things in
# Move the mouse over the graph to explore its interactivity.
# Drag a rectangle in the graph to zoom. Examine the icons at the upper right.
# Click the "Reset axes" icon to restore. Drag along the bottom or left to pan.
#
s='<b>Mass and Spring: Graph</b>'
#
#pCheat = (2 * pi) * ((bob.mass / springLeft.ks) ** 0.5)
#print(pCheat)
#pCheat *= 1.0

scale = 1.1
len = 0.5;

graph(title=s, xtitle='Time', ytitle='Displacement',xmax= len, ymax = initial_stretch * scale, ymin = -(initial_stretch * scale), x=0, y=500, width=500, height=300)
#
# Set up the curve to plot information on the graph.
#
drawit = gcurve(color=color.cyan, label='Position')
#
#t < scale * pCheat
while(t < len):
    rate(100)
#
#
#    spring.force = -(spring_constantL) * (bob.pos - spring.equil)

    springLeft.force = norm(bob.pos - springLeft.equil) * (-spring_constantL * (mag(bob.pos - springLeft.equil) ** 1))
    springRight.force = norm(bob.pos - springRight.equil) * (-spring_constantR * (mag(bob.pos - springRight.equil) ** 1))

    bob.mom += (springLeft.force * dt) + (springRight.force * dt)
    bob.pos += (bob.mom / bob_mass) * dt
#
# Plot the x-coordinate of the block as a function of time.
#
    springLeft.axis = bob.pos-wallLeft.pos
    springRight.axis = bob.pos-wallRight.pos
    xblock = bob.pos.x - springLeft.equil.x + wallLeft.pos.x
    drawit.plot(pos=(t, xblock))

    t = t + dt