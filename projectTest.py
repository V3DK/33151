from math import *
from vpython import *
#0.4,0.2,0.6
brown = vector(0.4,0.2,0.6)

minRad = 1e6
d = 1e8

sunEarthDist = 1.49598e11
eSpeed = 29839.7170
mSpeed = 1022
earthMoonDist = 3.844e8

earthMass = 5.972e24
sunMass = 1.989e30
moonMass = 7.347673e22

ved = sphere(pos=vector(sunEarthDist,0,0),radius=minRad,color=color.rgb_to_hsv(brown))
tilden = sphere(pos=vector(-d,0,0),radius=minRad,color=color.white)
chamy = sphere(pos=vector(0,0,0),radius=minRad * 1, color=color.yellow)

G = 6.67e-11

ved.mass = earthMass
tilden.mass = 1e23
chamy.mass = sunMass

p = 1
ved.speed = eSpeed * p
tilden.speed = -p * 100 * 0
chamy.speed = 0

ved.velocity = vector(0, ved.speed, 0)
ved.accel = vector(0, 0, 0)

tilden.velocity = vector(0, tilden.speed, 0)
tilden.accel = vector(0, 0, 0)

chamy.velocity = vector(0, chamy.speed, 0)
chamy.accel = vector(0, 0, 0)

ved.trail = curve(color=color.red) #,retain=250)
tilden.trail = curve(color=color.green) #,retain=250)
chamy.trail = curve(color=color.blue) #,retain=250)

ved.trail.append(pos = ved.pos)
tilden.trail.append(pos=tilden.pos)
chamy.trail.append(pos=chamy.pos)



rTV = ved.pos - tilden.pos
rTC = chamy.pos - tilden.pos
rCV = ved.pos - chamy.pos
fTV = ((-(G) * (tilden.mass * ved.mass)) * (1 / (mag2(rTV)))) * norm(rTV)
fTC = ((-(G) * (tilden.mass * chamy.mass)) * (1 / (mag2(rTC)))) * norm(rTC)
fCV = ((-(G) * (chamy.mass * ved.mass)) * (1 / (mag2(rCV)))) * norm(rCV)
ved.force = fCV
# tilden.force = vector(0, 0, 0)
chamy.force = -fCV

def update():
    rTV = ved.pos - tilden.pos
    rTC = chamy.pos - tilden.pos
    rCV = ved.pos - chamy.pos
    fTV = ((-(G) * (tilden.mass * ved.mass)) * (1 / (mag2(rTV)))) * norm(rTV)
    fTC = ((-(G) * (tilden.mass * chamy.mass)) * (1 / (mag2(rTC)))) * norm(rTC)
    fCV = ((-(G) * (chamy.mass * ved.mass)) * (1 / (mag2(rCV)))) * norm(rCV)
    ved.force = fCV
    # tilden.force = vector(0, 0, 0)
    chamy.force = -fCV
    ved.accel = ved.force / ved.mass
    #tilden.accel = tilden.force / tilden.mass
    chamy.accel = chamy.force / chamy.mass

time = 0
dt = 3600

run = True

while run:
    rate(500)

    #mark last position
    prev = ved.pos.y

    #update pos via verlet velocity
    ved.pos += (ved.velocity * dt) + ((0.5 * ved.accel) * (dt**2))
    chamy.pos += (chamy.velocity * dt) + ((0.5 * chamy.accel) * (dt**2))

    # update accel and velocity
    vedAccelCurr = ved.accel
    chamyAccelCurr = chamy.accel

    update()

    ved.velocity += (vedAccelCurr + ved.accel) * (0.5 * dt)
    chamy.velocity += (chamyAccelCurr + chamy.accel) * (0.5 * dt)

    #trails
    ved.trail.append(pos = ved.pos)
    tilden.trail.append(pos=tilden.pos)
    chamy.trail.append(pos=chamy.pos)

    #mark current position
    curr = ved.pos.y

    #"""
    if((curr != 0) and (prev != 0)):
        if((curr / abs(curr)) > (prev / abs(prev))):
            print(time / 86400, "days,", time, "seconds")

    #"""

     # update for next iteration
    time += dt

