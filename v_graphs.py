# Obtaining graphs for initial velocities
# The code below is not for creating simulations, it is only for obtaining graphs

import numpy as np
import matplotlib.pyplot as plt
from vpython import *
scene = canvas() 

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


#define the value of G
G=6.673e-11

def initialv(n):
    mass=600*1.9e27/n
    AU = 149.6e9      
    objects=[]
    r = 2*AU
    for i in range(n):
        objects.append(sphere(pos=vector(r*np.sin(2*i*np.pi/n),r*np.cos(2*i*np.pi/n),0),velocity=vector(0,0,0),
            mass=mass, radius=0, color=color.yellow))
    u =((r*accnet(objects[0], objects).mag))**(1/2)
    return(u)

n=10
initialv(n)
V=[initialv(i) for i in range(2,n+1)]
N=[i for i in range(2,n+1)]

def mainplot():
    plt.scatter(N, V)
    plt.xlabel("n")
    plt.ylabel("u (m/s)")
    plt.title("u vs n")
    plt.show()

def logplot():
    plt.scatter(np.log(np.log(N)), np.log(V))
    plt.xlabel("log(log n)")
    plt.ylabel("log u")
    plt.title("log u vs log(log n)")
    (m,c)=np.polyfit(np.log(np.log(N)), np.log(V), 1,)
    plt.plot(np.log(np.log(N)), [m*a +c for a in np.log(np.log(N))], '-r')
    print(m,c)
    print(np.exp(c))
    plt.show()

def nlarge():
    plt.scatter(N[800:1000], V[800:1000])
    plt.xlabel("n")
    plt.ylabel("u (m/s)")
    plt.title("u vs n for large values of n")
    plt.show()