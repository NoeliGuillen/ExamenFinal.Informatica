from vpython import *
import math

titulo=canvas(title="Estacionamiento")

piso=box(pos=vector(0,-0.5,0),size=vector(20,0.1,20),color=color.gray(0.5))
#carros
azul= box(pos=vector(0, 0.5, 5), size=vector(1, .5, 1), color=color.red)
azul= box(pos=vector(0, 0, 5), size=vector(1, 0.5, 2), color=color.blue)
azul1 = cylinder(pos=vector(-.6, 0, 4.5), axis=vector(0, 1.2, 0), radius=.2, color=color.gray(0.5))
azul2= cylinder(pos=vector(-.6, 0, 5.3), axis=vector(0, 1.2, 0), radius=.2, color=color.gray(0.5))

verde= box(pos=vector(0, 0.5, 0), size=vector(1, .5, 1), color=color.blue)
verde= box(pos=vector(0, 0, 0), size=vector(1, 0.5, 2), color=color.blue)
verde1 = cylinder(pos=vector(-.6, 0, -.5), axis=vector(0, 1.2, 0), radius=.2, color=color.gray(0.5))
verde2 = cylinder(pos=vector(-.6, 0, .3), axis=vector(0, 1.2, 0), radius=.2, color=color.gray(0.5))

#semaforo
sema = cylinder(pos=vector(4, -0.5, -5), axis=vector(0, 5, 0), radius=.3, color=color.white)
semaf=box(pos=vector(4, 4, -5), size=vector(3, 1, 1), color=color.blue)
rojo=sphere(pos=vector(4,3.5,-4.6),radius=.26,size=vector(2,1,1),color=color.red)
verde=sphere(pos=vector(4,4.7,-4.6),radius=.26,size=vector(2,1,1),color=color.green)

while True:
    rate(40)  
    
    
    azul1.rotate(angle=180, axis=vector(1, 1, 1))
    azul2.rotate(angle=180, axis=vector(1, 1, 1))
    verde1.rotate(angle=180, axis=vector(1, 1, 1))
    verde2.rotate(angle=180, axis=vector(1, 1, 1))
    tiempo4+= 0.1  
