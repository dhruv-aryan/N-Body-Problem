import random
import numpy as np
from vpython import *
scene = canvas() 

# Constants that we will need
n=10 # we can change n to any number
mass=600*1.9e27/n # to keep total mass constant
AU = 149.6e9
r = 2*AU # radius of circle
G=6.674e-11 # define the value of G

# acceleration of object a due to object b
def acc(a, b):
    rel_pos = b.pos - a.pos
    return G*b.mass * norm(rel_pos)/rel_pos.mag2

## Accelaration of a due to all the objects b intracting with it
def accnet (a, objlist):
    sum_acc = vector (0,0,0)
    for b in objlist:
        if (a!=b):
            sum_acc = sum_acc + acc(a, b)
    return sum_acc

#settings for animations
scene.background = color.black
scene.autoscale = 0
scene.range = 10*AU

objects=[] # creating a list of objects


# Putting markers on the positions of the bodies
for i in range(n):
    objects.append(sphere(pos=vector(r*np.sin(2*i*np.pi/n),r*np.cos(2*i*np.pi/n),0),velocity=vector(0,0,0),
        mass=mass, radius=0, color=color.yellow))

u =((r*accnet(objects[0], objects).mag))**(1/2) # using the positions to get initial velocity
print(u)

# Making the bodies that will interact
for i in range(n):
    objects[i]=sphere(pos=vector(r*np.sin(2*i*np.pi/n),r*np.cos(2*i*np.pi/n),0),velocity=vector(-u*np.cos(2*i*np.pi/n),u*np.sin(2*i*np.pi/n),0),
        mass=mass, radius=0.1*AU, color=color.magenta)

 
# adding attributes for their accelaration and orbits
for x in objects:
    x.acc = vector(0,0,0)
    x.track=curve (color = x.color)

# set total momentum of system to zero (centre of mass frame) 
sum=vector(0,0,0)
for x in objects:
    sum=sum+x.mass*x.velocity

delta=30.*60.*100 # setting the time step

# Solving the equations of motion using leap frog method

# Initialise leap-frog by finding the velocites at t=dt/2
for x in objects:
    x.velocity = x.velocity + totalacc(x, objects)*delta/2.0

# start leap-frog
while True:
    rate(100)
    for x in objects:
        #update the positions
        x.pos = x.pos + x.velocity*delta
        x.track.append(pos=x.pos)

        #update the velocities
        x.velocity = x.velocity + totalacc(x, objects)*delta

    scene.center = vector(0,0,0) # view centered on the centre of mass frame