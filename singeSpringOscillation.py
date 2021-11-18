from vpython import *
from math import *

#
# Initialize so spring properties. All units are assumed to be
# in MKS units.
#
spring_constant = 10 / 4
equil_length    = 1
initial_stretch = 0.1
bob_mass        = 0.01
#
# Set up the animation canvas where we display the mass on the spring.
#
scene2 = canvas(title='Mass on a Spring',caption='Animated Display',
     center=vector(equil_length,0,0), background=color.white)
#
# Set up the wall, spring and mass
#
wall   = box(pos=vector(0,0,0),size=vector(0.01,.2,.2),color=color.cyan)
bob  = box(pos=vector(0,0,0),size=vector(.05,.05,.05),color=color.red)
spring = helix(pos=wall.pos,axis=bob.pos-wall.pos,radius=0.01,thickness=.01,coils=10,color=color.green)
#
# equilibrium position of the end of the spring.
#
spring.equil = vector(equil_length,0,0)
bob.pos = wall.pos + spring.equil + vector(initial_stretch,0,0)
#
# Input Parameters needed in the program. Be sure to
# choose sensible values.
#
bob.mass  = bob_mass
bob.mom   = vector(0,0,0)
spring.ks = spring_constant
dt = 0.02
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
pCheat = (2 * pi) * ((bob.mass / spring.ks) ** 0.5)
print(pCheat)
pCheat *= 1.0

scale = 1.1
len = 15;

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
#    spring.force = -(spring_constant) * (bob.pos - spring.equil)

    spring.force = norm(bob.pos - spring.equil) * (-spring_constant * (mag(bob.pos - spring.equil) ** 3))

    bob.mom += spring.force * dt
    bob.pos += (bob.mom / bob_mass) * dt
#
# Plot the x-coordinate of the block as a function of time.
#
    spring.axis = bob.pos-wall.pos
    xblock = bob.pos.x - spring.equil.x + wall.pos.x
    drawit.plot(pos=(t,xblock))

    t = t + dt