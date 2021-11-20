from math import *
from vpython import *
#0.4,0.2,0.6
brown = vector(0.4,0.2,0.6)

minRad = 2e6
d = 1e8

sunEarthDist = 1.49598e11
eSpeed = 29839.7170
mSpeed = 1022
earthMoonDist = 3.844e8

earthMass = 5.972e24
sunMass = 1.989e30
moonMass = 7.347673e22

ved = sphere(pos=vector(d,0,0),radius=minRad,color=color.rgb_to_hsv(brown))
tilden = sphere(pos=vector(-d,0,0),radius=minRad,color=color.white)
chamy = sphere(pos=vector(0,0,0),radius=minRad * 1, color=color.yellow)

G = 6.67e-11

ved.mass = 1e23
tilden.mass = 1e23
chamy.mass = 1e23

ved.speed = 100
tilden.speed = -100
chamy.speed = 0

ved.momentum = ved.mass*vector(0, ved.speed, 0)
tilden.momentum = tilden.mass*vector(0, tilden.speed, 0)
chamy.momentum = chamy.mass*vector(0, chamy.speed, 0)

ved.trail = curve(color=color.red) #,retain=250)
tilden.trail = curve(color=color.green) #,retain=250)
chamy.trail = curve(color=color.blue) #,retain=250)

ved.trail.append(pos = ved.pos)
tilden.trail.append(pos=tilden.pos)
chamy.trail.append(pos=chamy.pos)

time = 0
dt = 3600

run = True

while run:
    rate(100)
    time += dt

    rTV = ved.pos - tilden.pos
    rTC = chamy.pos - tilden.pos
    rCV = ved.pos - chamy.pos

    #if ((mag(rTV) < minRad) or (mag(rTC) < minRad) or (mag(rCV) < minRad)):
        #run = False

    fTV = ((-(G) * (tilden.mass * ved.mass)) * (1 / (mag2(rTV)))) * norm(rTV)
    fTC = ((-(G) * (tilden.mass * chamy.mass)) * (1 / (mag2(rTC)))) * norm(rTC)
    fCV = ((-(G) * (chamy.mass * ved.mass)) * (1 / (mag2(rCV)))) * norm(rCV)

    #"""
    ved.force = fTV + fCV
    tilden.force = -(fTV + fTC)
    chamy.force = fTC - fCV
    #"""

    """
    ved.force = fCV
    tilden.force = vector(0, 0, 0)
    chamy.force = -fCV
    #print(ved.force, tilden.force, chamy.force)
    """

    ved.momentum += ved.force * dt
    tilden.momentum += tilden.force * dt
    chamy.momentum += chamy.force * dt

    prev = tilden.pos.y - ved.pos.y


    ved.pos += (ved.momentum / ved.mass) * dt
    tilden.pos += (tilden.momentum / tilden.mass) * dt
    chamy.pos += (chamy.momentum / chamy.mass) * dt

   # print(ved.pos, tilden.pos, chamy.pos)

    ved.trail.append(pos = ved.pos)
    tilden.trail.append(pos=tilden.pos)
    chamy.trail.append(pos=chamy.pos)

    curr = tilden.pos.y - ved.pos.y

    #"""
    if((curr != 0) and (prev != 0)):
        if((curr / abs(curr)) > (prev / abs(prev))):
            print(time / 86400, "days,", time, "seconds")

    #"""

