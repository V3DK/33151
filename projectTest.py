from math import *
from vpython import *
#0.4,0.2,0.6
brown = vector(0.4,0.2,0.6)
ved = sphere(pos=vector(0,0,0),radius=1e8,color=color.rgb_to_hsv(brown))
tilden = sphere(pos=vector(-5e9,0,0),radius=1e8,color=color.white)
chamy = sphere(pos=vector(5e9,0,0),radius=1e8,color=color.yellow)

G = 6.67e-11

ved.mass = 5e24
tilden.mass = 5e24
chamy.mass = 5e24

s = 0.965
ved.speed = 0
tilden.speed = s * 3e2
chamy.speed = s * -3e2

ved.momentum = ved.mass*vector(0, ved.speed, 0)
tilden.momentum = tilden.mass*vector(0, tilden.speed, 0)
chamy.momentum = chamy.mass*vector(0, chamy.speed, 0)

ved.trail = curve(color=color.red) #,retain=250)
tilden.trail = curve(color=color.green) #,retain=250)
chamy.trail = curve(color=color.blue) #,retain=250)

time = 0
dt = 3600*12
while True:
    rate(500)
    time += dt

    rTV = ved.pos - tilden.pos
    rTC = chamy.pos - tilden.pos
    rCV = ved.pos - chamy.pos

    fTV = ((-(G) * (tilden.mass * ved.mass)) * (1 / (mag2(rTV)))) * norm(rTV)
    fTC = ((-(G) * (tilden.mass * chamy.mass)) * (1 / (mag2(rTC)))) * norm(rTC)
    fCV = ((-(G) * (chamy.mass * ved.mass)) * (1 / (mag2(rCV)))) * norm(rCV)



    ved.force = fTV + fCV
    tilden.force = -(fTV + fTC)
    chamy.force = fTC - fCV

    #print(ved.force, tilden.force, chamy.force)

    ved.momentum += ved.force * dt
    tilden.momentum += tilden.force * dt
    chamy.momentum += chamy.force * dt



    ved.pos += (ved.momentum / ved.mass) * dt
    tilden.pos += (tilden.momentum / tilden.mass) * dt
    chamy.pos += (chamy.momentum / chamy.mass) * dt

   # print(ved.pos, tilden.pos, chamy.pos)

    ved.trail.append(pos = ved.pos)
    tilden.trail.append(pos=tilden.pos)
    chamy.trail.append(pos=chamy.pos)

