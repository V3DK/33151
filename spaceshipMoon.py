from math import *
from vpython import *
#
#  Define needed constants for the program
#
#  Initial speed of the space ship
ShipSpeed = 1.3e4
ShipMass  = 170
#
G=6.67E-11
# Radius of Earth and Moon
#1.7374e6
rad_earth = 6.3781e6
rad_moon  = 6.3781e6
# 7.34e22
EarthMass = 6e24
MoonMass  = 6e24
#
# Locate the Earth and moon along the x-axis.
#
eL = vector(0,0,0)
mL = vector(4.0e8,0,0)
#
#
# Set up the displays
#
scene2 = canvas(title='Voyage to the Moon',caption='Animated Display',width=800, height=400,
     center=0.5*mL, background=color.black)
#
earth = sphere(pos=eL, radius=rad_earth, color=color.blue)
moon  = sphere(pos=mL, radius=rad_moon, color=color.cyan)
#
earth.mass = EarthMass    
moon.mass  = MoonMass  
#
# Initialize the spaceship
# 50 km atmosphere
shiplocation=vector(earth.radius+50000,0,0)
#
ship = cylinder(pos=shiplocation, axis=vector(5e6,0,0),radius=2e6,color=color.red)
#
ship.mass  = ShipMass
ship.speed = ShipSpeed
yScale = 0
xScale = 1
#
ship.momentum = vector(xScale * ship.mass*ship.speed, yScale * ship.mass*ship.speed,0)
ship.trail = curve(color=color.white)
#
# Create graphic for the energy display.
#
energyplot = graph(title='Energy versus Position',xtitle='Ship Position',ytitle='Energy',xmin=0, xmax=moon.pos.x, ymin=-1.5e10,ymax=1.5e10)
#
drawKE = gcurve(color=color.cyan,label='Kinetic Energy')
drawPE = gcurve(color=color.blue,label='Potential Energy')
drawTE = gcurve(color=color.magenta,label='Total Energy')
drawW = gcurve(color=color.red,label='Incremental Work')
drawTW = gcurve(color=color.green,label='Total Work')

#
#
t= 0
dt= 10
#
#
runit=1
tW = 0;
prints = 0
while (runit==1):
#
    rate(1000)
#
# Calculate the total force on the ship, and then use this
# in Newton’s 2nd law.
#
  #  moonComp = (-G * (MoonMass) * (ShipMass) * (1 / mag2(moon.pos - ship.pos))) * (norm(moon.pos - ship.pos))
    moonComp = (G * (MoonMass) * (ShipMass) * (1 / mag2(moon.pos - ship.pos))) * (norm(moon.pos - ship.pos))

    earthComp = (G * (EarthMass) * (ShipMass) * (1 / mag2(earth.pos - ship.pos))) * (norm(earth.pos - ship.pos))

    ship.force = moonComp + earthComp
    ship.momentum += ship.force * dt
    ship.pos      += (ship.momentum / ShipMass) * dt
#
#append a piece to the end of the ship’s trail
#
    ship.trail.append(pos=ship.pos)

    KE = (mag(ship.momentum) ** 2) / (2 * ShipMass)
    PE = (-G * (EarthMass) * (ShipMass) * (1 / mag(earth.pos - ship.pos)))
    TE = KE + PE
    w = dot(ship.force, (ship.momentum / ShipMass) * dt)
    tW += w

    """
    KE = (mag(ship.momentum) ** 2) / (2 * ShipMass)
    PE = (-G * (MoonMass) * (ShipMass) * (1 / mag(moon.pos - ship.pos))) + (-G * (EarthMass) * (ShipMass) * (1 / mag(earth.pos - ship.pos)))
    TE = KE + PE
    w = dot(ship.force, (ship.momentum / ShipMass) * dt )
    #w = dot(ship.force, ship.pos - earth.pos)
    tW += w
    """



#
    drawKE.plot(pos=(ship.pos.x, KE))
    drawPE.plot(pos=(ship.pos.x,PE))
    drawTE.plot(pos=(ship.pos.x,TE))
    drawW.plot(pos=(ship.pos.x, w))
    drawTW.plot(pos=(ship.pos.x,tW))

#
    t=t+dt
#
# Check if we fell back to the earth or hit the moon:
#

    if (ship.pos.x > (moon.pos.x - 50000 - moon.radius)):
        if(prints == 1):
            print(ship.momentum / ship.mass, ship.pos.x)
        prints+=1

    if (mag(ship.pos-earth.pos) <= earth.radius ):
        print('Ship crashed back on the earth at time',t,'seconds')
        runit=0
    elif (mag(ship.pos-moon.pos) <= moon.radius/2 ):
        print('Ship crashed on the moon at time ',t,'seconds')
        runit=0

#
#                                                                       
print('All done.')
