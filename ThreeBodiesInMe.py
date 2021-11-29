from math import *
from vpython import *
from heapq import nsmallest

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#https://github.com/V3DK/33151/blob/master/projectTest.py

###############################
#		Constants
###############################
brown = vector(0.4,0.2,0.6)
minRad = 2.5e6
d = 1e8
v = 196.23773

G = 6.67e-11

###############################
#		Physics Function
###############################
def getDistances(ved,tilden,chamy):
    rTV = ved.pos - tilden.pos
    rTC = chamy.pos - tilden.pos
    rCV = ved.pos - chamy.pos
    return (rTV,rTC,rCV)

def updateForces(ved,tilden,chamy):
    fTV = calculateForce(ved,tilden)
    fTC = calculateForce(chamy,tilden)
    fCV = calculateForce(ved,chamy)

    #update forces
    ved.force = fTV + fCV
    tilden.force = -(fTV + fTC)
    chamy.force = fTC - fCV

    #update accels
    ved.accel = ved.force / ved.mass
    tilden.accel = tilden.force / tilden.mass
    chamy.accel = chamy.force / chamy.mass

    return (fTV, fTC, fCV)

def calculateForce(object1,object2): #force on object2 from object1
    d = object1.pos-object2.pos
    F = ((-(G) * (object1.mass*object2.mass)) * (1 / (mag2(d)))) * norm(d)
    return F

def getCenterOfMass(*args):
    RM = [0,0,0]
    TM = 0
    for object in args:
        r = (object.pos.x,object.pos.y,object.pos.z)
        m = object.mass

        for index in range(len(r)):
            RM[index] += r[index]*m
        TM += m
    CM = vector(*RM)/TM
    return CM

def vectorToTuple(pos):
    x,y,z = pos.x,pos.y,pos.z
    return (x,y,z)

def isCollision(*args):
    for index in range(len(args)):
        mainObject = args[index]
        mainRadius = mainObject.radius
        objectsToCheck =  args[:index]+args[index+1:]
        for object in objectsToCheck:
            objectRadius = object.radius
            D = objectRadius+mainRadius
            if dist(vectorToTuple(mainObject.pos),vectorToTuple(object.pos)) <= D:
                return True
    return False

def updateAll(*args, **kwargs):
    if 'dt' in kwargs:
        dt = kwargs['dt']
    else:
        raise Exception('Must Have A dt. Use "dt="')
    for object in args:
        object.momentum += object.force*dt
        object.pos += (object.momentum/object.mass)*dt
        object.trail.append(pos=object.pos)

def getPotentialEnergy(*args):
    GPEs = []
    for index in range(len(args)):
        mainObject = args[index]
        objectsToCheck =  args[:index]+args[index+1:]
        for object in objectsToCheck:
            GPEs.append(calculateGravitationalPotentialEnergy(mainObject,object))
    return GPEs

def getKineticEnergy(*args):
    KEs = []
    for object in args:
        KEs.append(calculateKineticEnergy(object))
    return KEs

def calculateGravitationalPotentialEnergy(object1,object2):
    d = object1.pos-object2.pos
    GPE = (-(G) * (object1.mass*object2.mass)) * (1 / (mag(d)))
    return GPE

def calculateKineticEnergy(object):
    speed = mag(object.momentum/object.mass)
    KE = .5*object.mass*(speed**2)
    return KE


###############################
#		Test Functions
###############################

def testGetCenterOfMass():
    print('Testing getCenterOfMass()...',end='')
    ved = sphere(radius=minRad,color=color.rgb_to_hsv(brown))
    tilden = sphere(radius=minRad,color=color.white)
    chamy = sphere(radius=minRad * 1, color=color.yellow)

    #TEST1
    ved.pos = vector(1,0,0)
    chamy.pos = vector(0,1,1)
    tilden.pos = vector(-1,-1,-1)

    ved.mass = 1
    chamy.mass = 1
    tilden.mass = 1
    assert(getCenterOfMass(ved,tilden,chamy)==vector(0,0,0))
    assert(getCenterOfMass(ved,tilden) == vector(0,-.5,-.5))
    print('Passed!')

# testGetCenterOfMass()

###############################
#		Initial States
###############################
vedInitialPos 	 = vector(0, -d, 0)
tildenInitialPos = vector(0.8660254038 * d,0.5 * d,0)
chamyInitialPos  = vector(-0.8660254038 * d,0.5 * d,0)

vedInitialVel 	 = vector(v,0,0)
tildenInitialVel = vector(-0.5 * v, 0.8660254038 * v, 0)
chamyInitialVel  = vector(-0.5 * v, -0.8660254038 * v, 0)

vedMass 		 = 1e23
tildenMass 		 = 1e23
chamyMass		 = 1e23

###############################
#		Setup View
###############################
ved = sphere(pos=vedInitialPos,radius=minRad,color=color.rgb_to_hsv(brown))
tilden = sphere(pos=tildenInitialPos,radius=minRad,color=color.white)
chamy = sphere(pos=chamyInitialPos,radius=minRad * 1, color=color.yellow)

ved.mass = vedMass
tilden.mass = tildenMass
chamy.mass = chamyMass

ved.momentum = vedInitialVel*vedMass
tilden.momentum = tildenInitialVel*tildenMass
chamy.momentum = chamyInitialVel*chamyMass

#	SETUP TRAILS
ved.trail = curve(color=color.red) #,retain=250)
tilden.trail = curve(color=color.green) #,retain=250)
chamy.trail = curve(color=color.blue) #,retain=250)

ved.trail.append(pos=ved.pos)
tilden.trail.append(pos=tilden.pos)
chamy.trail.append(pos=chamy.pos)

#center of mass initialization
CM = sphere(pos=getCenterOfMass(ved,tilden,chamy),radius=minRad * 0.1, color=color.magenta)
CM.trail = curve(color=color.magenta) #,retain=250)

#Lines between
a1 = curve(color = color.gray(0.5), retain = 2)
b1 = curve(color = color.gray(0.5), retain = 2)
c1 = curve(color = color.gray(0.5), retain = 2)
a2 = curve(color = color.gray(0.5), retain = 2)
b2 = curve(color = color.gray(0.5), retain = 2)
c2 = curve(color = color.gray(0.5), retain = 2)

###############################
#		Setup Graphing
###############################
graph(title='<b>Energies Graph</b>', xtitle='Time', ytitle='Energy',width=500, height=300)
#xmax=5.0, ymax=10e-4, ymin=-10e-4,x=0, y=500,
gKE = gcurve(color=color.red, label='KE')
gPE = gcurve(color=color.blue, label='PE')
gTE = gcurve(color=color.green, label='TE')

t = []
graphedPE = []
graphedKE = []
graphedTE = []

###############################
#		      LOOP
###############################
#Rate and Time
maxDT = 800
minDT = 10
stableRate = 200
maxRate = 500
dt = maxDT

time = -dt
while not isCollision(ved,tilden,chamy):
    try:
        time+=dt

        fTV, fTC, fCV = updateForces(ved,tilden,chamy)
        updateAll(ved,tilden,chamy,dt=dt)
        CM.pos = getCenterOfMass(ved,tilden,chamy)
        CM.trail.append(pos=CM.pos)

        PE = sum(getPotentialEnergy(ved,tilden,chamy))
        KE = sum(getKineticEnergy(ved,tilden,chamy))
        TE = PE+KE
        # print(KE,PE,TE)

        t.append(time)
        graphedPE.append(PE)
        graphedKE.append(KE)
        graphedTE.append(TE)

        gPE.plot(pos=(time,PE))
        gKE.plot(pos=(time,KE))
        gTE.plot(pos=(time,TE))


        #update lines
        if(True):
            a1.append(tilden.pos, chamy.pos)
            b1.append(ved.pos, tilden.pos)
            c1.append(ved.pos, chamy.pos)

            a2.append(tilden.pos, CM.pos)
            b2.append(ved.pos, CM.pos)
            c2.append(CM.pos, chamy.pos)

        #determining rate -> keep program running same "speed"
        newRate = stableRate * maxDT / dt
        #if(newRate > maxRate):
        #    newRate = maxRate
        rate(newRate)

        rTV,rTC,rCV = getDistances(ved,tilden,chamy)
        #determining dt based on dt
        avgDist = (mag(rTV) + mag(rTC) + mag(rCV)) * (1/3)
        distances = [rTV,rTC,rCV]
        minDist = mag(min(distances,key=lambda x:mag(x)))
        dt = ceil(((minDist / avgDist) * (maxDT - minDT)) + minDT)

        if(dt > maxDT):
            dt = maxDT
    except: break

plt.plot(t,graphedPE,color='b',label="PE")
plt.plot(t,graphedKE,color='r',label="KE")
plt.plot(t,graphedTE,color='g',label="TE")
plt.legend()
plt.show()
