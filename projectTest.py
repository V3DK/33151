from math import *
from vpython import *
from heapq import nsmallest

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

ved = sphere(pos=vector(d * (0.97000436),-d * 0.24308753, 0),radius=minRad,color=color.rgb_to_hsv(brown))
tilden = sphere(pos=vector(0,0,0),radius=minRad,color=color.white)
chamy = sphere(pos=vector(-d * (0.97000436), d * 0.24308753, 0),radius=minRad * 1, color=color.yellow)

G = 6.67e-11

ved.mass = 1e23
tilden.mass = 1e23
chamy.mass = 1e23

p = 1.3
ved.speed = 50 * p
tilden.speed = 100 * p
chamy.speed = 50 * p

b = 258.25
v8x = 0.93240737 * b
v8y = 0.86473146 * b

ved.velocity = vector(v8x / 2, v8y / 2, 0)
ved.accel = vector(0, 0, 0)

tilden.velocity = vector(-v8x, -v8y, 0)
tilden.accel = vector(0, 0, 0)

chamy.velocity = vector(v8x / 2, v8y / 2, 0)
chamy.accel = vector(0, 0, 0)

ved.trail = curve(color=color.red) #,retain=250)
tilden.trail = curve(color=color.green) #,retain=250)
chamy.trail = curve(color=color.blue) #,retain=250)


ved.trail.append(pos = ved.pos)
tilden.trail.append(pos=tilden.pos)
chamy.trail.append(pos=chamy.pos)

#setup other variables
rTV = vector(0, 0, 0)
rTC = vector(0, 0, 0)
rCV = vector(0, 0, 0)
fTV = vector(0, 0, 0)
fTC = vector(0, 0, 0)
fCV = vector(0, 0, 0)
ved.force = vector(0, 0, 0)
tilden.force = vector(0, 0, 0)
chamy.force = vector(0, 0, 0)

def update():
    #update distances
    rTV = ved.pos - tilden.pos
    rTC = chamy.pos - tilden.pos
    rCV = ved.pos - chamy.pos
    fTV = ((-(G) * (tilden.mass * ved.mass)) * (1 / (mag2(rTV)))) * norm(rTV)
    fTC = ((-(G) * (tilden.mass * chamy.mass)) * (1 / (mag2(rTC)))) * norm(rTC)
    fCV = ((-(G) * (chamy.mass * ved.mass)) * (1 / (mag2(rCV)))) * norm(rCV)

    #update forces
    ved.force = fTV + fCV
    tilden.force = -(fTV + fTC)
    chamy.force = fTC - fCV

    #update accels
    ved.accel = ved.force / ved.mass
    tilden.accel = tilden.force / tilden.mass
    chamy.accel = chamy.force / chamy.mass

#center of mass initialization
CM = sphere(pos=vector(0,0,0),radius=minRad * 0.1, color=color.magenta)
CM.trail = curve(color=color.magenta) #,retain=250)

#update before while loop starts
update()


maxDT = 700
minDT = 10
stableRate = 200
maxRate = 750

TVInitDist = mag(ved.pos - tilden.pos)
TCInitDist = mag(chamy.pos - tilden.pos)
CVInitDist = mag(ved.pos - chamy.pos)

time = 0
dt = maxDT



#lines between
a1 = curve(color = color.white, retain = 2)
b1 = curve(color = color.white, retain = 2)
c1 = curve(color = color.white, retain = 2)
a2 = curve(color = color.white, retain = 2)
b2 = curve(color = color.white, retain = 2)
c2 = curve(color = color.white, retain = 2)

run = True
showLines = True

while run:
    #need these here...not sure why
    rTV = ved.pos - tilden.pos
    rTC = chamy.pos - tilden.pos
    rCV = ved.pos - chamy.pos

    #determining rate -> keep program running same "speed"
    newRate = stableRate * maxDT / dt
    if(newRate > maxRate):
        newRate = maxRate
    rate(newRate)

    #update lines

    if(showLines):
        a1.append(tilden.pos, chamy.pos)
        b1.append(ved.pos, tilden.pos)
        c1.append(ved.pos, chamy.pos)

        a2.append(tilden.pos, CM.pos)
        b2.append(ved.pos, CM.pos)
        c2.append(CM.pos, chamy.pos)

    #center of mass
    cOfM = ((ved.pos * ved.mass) + (chamy.pos * chamy.mass) + (tilden.pos * tilden.mass)) / (ved.mass + chamy.mass + tilden.mass)
    CM.pos = cOfM

    #stopping state -> end sim if any masses collide
    if ((mag(rTV) < minRad) or (mag(rTC) < minRad) or (mag(rCV) < minRad)):
        run = False



    #mark last position
    prev = ved.pos.y

    #update pos via verlet velocity
    ved.pos += (ved.velocity * dt) + ((0.5 * ved.accel) * (dt**2))
    chamy.pos += (chamy.velocity * dt) + ((0.5 * chamy.accel) * (dt**2))
    tilden.pos += (tilden.velocity * dt) + ((0.5 * tilden.accel) * (dt ** 2))

    #update accel and velocity
    vedAccelCurr = ved.accel
    chamyAccelCurr = chamy.accel
    tildenAccelCurr = tilden.accel

    update()

    ved.velocity += (vedAccelCurr + ved.accel) * (0.5 * dt)
    chamy.velocity += (chamyAccelCurr + chamy.accel) * (0.5 * dt)
    tilden.velocity += (tildenAccelCurr + tilden.accel) * (0.5 * dt)

    #trails
    ved.trail.append(pos = ved.pos)
    tilden.trail.append(pos=tilden.pos)
    chamy.trail.append(pos=chamy.pos)
    CM.trail.append(pos=CM.pos)



    #mark current position
    curr = ved.pos.y

    """ determine period
    if((curr != 0) and (prev != 0)):
        if((curr / abs(curr)) > (prev / abs(prev))):
            print(time / 86400, "days,", time, "seconds")

    """

    #determining dt based on dt
    avgDist = (mag(rTV) + mag(rTC) + mag(rCV)) * (1/3)
    TVCurrDist = mag(rTV)
    TCCurrDist = mag(rTC)
    CVCurrDist = mag(rCV)

    list = [TVCurrDist, TCCurrDist, CVCurrDist]

    minDist = nsmallest(1, list)


    dt = ceil(((minDist[0] / avgDist) * (maxDT - minDT)) + minDT)
    if(dt > maxDT):
        dt = maxDT

     # update for next iteration
    time += dt

    #c.clear()

    #print(dt)


