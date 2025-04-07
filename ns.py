from vpython import *
import time
import random

# Configuración inicial
scene = canvas(title="Simulación Estacionamiento", width=800, height=600)

# Suelo
piso = box(pos=vector(0, -0.1, 0), size=vector(25, 0.1, 20), color=color.gray(0.5))

# Semáforo
poste = cylinder(pos=vector(7, -0.1, -8), axis=vector(0, 5, 0), radius=0.2, color=color.white)
caja = box(pos=vector(7, 4, -8), size=vector(1, 2, 1), color=color.black)
luz_roja = sphere(pos=vector(7, 4.5, -7.5), radius=0.2, color=color.gray(0.2))
luz_verde = sphere(pos=vector(7, 3.5, -7.5), radius=0.2, color=color.green)

# Barrera
base_barrera = vector(1.5, 0.1, -9)
pivot_barrera = vector(base_barrera.x, base_barrera.y, base_barrera.z)
barrera = box(pos=pivot_barrera + vector(0, 2, 0), size=vector(0.15, 4, 0.15), color=color.yellow)
barrera.rotation = 0

# Espacios de estacionamiento
espacios = [vector(0, 0.25, 6 - i*4) for i in range(4)]
ocupados = [False] * 4

# Carros estáticos
def crear_carro_estatico(pos, color_carro=color.blue):
    cuerpo = box(pos=pos, size=vector(2, 1, 4), color=color_carro)
    cylinder(pos=pos + vector(-1, -0.5, -1.2), axis=vector(0, 0.6, 0), radius=0.3, color=color.gray(0.5))
    cylinder(pos=pos + vector(-1, -0.5, 1.2), axis=vector(0, 0.6, 0), radius=0.3, color=color.gray(0.5))  
    cylinder(pos=pos + vector(1, -0.5, -1.2), axis=vector(0, 0.6, 0), radius=0.3, color=color.gray(0.5))  
    cylinder(pos=pos + vector(1, -0.5, 1.2), axis=vector(0, 0.6, 0), radius=0.3, color=color.gray(0.5))  

# Colocar carros estáticos
for z in [9, 4, -2, -8]:
    crear_carro_estatico(vector(-6, 0.5, z), color_carro=vector(random.random(), random.random(), random.random()))
    crear_carro_estatico(vector(-9, 0.5, z), color_carro=vector(random.random(), random.random(), random.random()))
    crear_carro_estatico(vector(9, 0.5, z), color_carro=vector(random.random(), random.random(), random.random()))
    crear_carro_estatico(vector(12, 0.5, z), color_carro=vector(random.random(), random.random(), random.random()))

# Carros móviles
colores_carros = [color.red, color.green, color.blue, color.orange, color.cyan]
indice_color = 0

def crear_carro(pos_inicial):
    global indice_color
    color_actual = colores_carros[indice_color % len(colores_carros)]
    indice_color += 1

    cuerpo = box(pos=pos_inicial, size=vector(2.4, 1.2, 4.8), color=color_actual)
    llantas = []
    for dx in [-1.2, 1.2]:
        for dz in [-1.4, 1.4]:
            pos_llanta = cuerpo.pos + vector(dx, -0.6, dz)
            llanta = cylinder(pos=pos_llanta, axis=vector(0, 0.6, 0), radius=0.4, color=color.black)
            llantas.append(llanta)
    return {'obj': cuerpo, 'llantas': llantas, 'estado': 'esperando', 'objetivo': None, 'tiempo': 0, 'paso_barrera': False, 'giro_realizado': False}

carros = []
nuevo_carro_timer = 0
max_carros = 1

# Semáforo automático
verde_duracion = 7
rojo_duracion = 3
ultimo_cambio = time.time()
estado_semaforo = 'verde'

def actualizar_semaforo():
    global estado_semaforo, ultimo_cambio
    ahora = time.time()
    if estado_semaforo == 'verde' and ahora - ultimo_cambio > verde_duracion:
        estado_semaforo = 'rojo'
        ultimo_cambio = ahora
    elif estado_semaforo == 'rojo' and ahora - ultimo_cambio > rojo_duracion:
        estado_semaforo = 'verde'
        ultimo_cambio = ahora

    if estado_semaforo == 'verde':
        luz_verde.color = color.green
        luz_roja.color = color.gray(0.2)
    else:
        luz_roja.color = color.red
        luz_verde.color = color.gray(0.2)

# Movimiento de carros
def mover_carros():
    for carro in list(carros):
        obj = carro['obj']
        llantas = carro['llantas']

        if carro['estado'] == 'esperando':
            if barrera.rotation >= 85:
                obj.pos.z += 0.1
                for l in llantas:
                    l.pos.z += 0.1
                    l.rotate(angle=0.2, axis=vector(1, 0, 0), origin=l.pos)

                if obj.pos.z > -7 and not carro['paso_barrera']:
                    carro['paso_barrera'] = True

            if carro['paso_barrera'] and obj.pos.z > -5:
                for i in range(4):
                    if not ocupados[i]:
                        ocupados[i] = True
                        carro['objetivo'] = espacios[i]
                        carro['estado'] = 'estacionando'
                        break

        elif carro['estado'] == 'estacionando':
            destino = carro['objetivo']
            if abs(obj.pos.z - destino.z) > 0.1:
                obj.pos.z += 0.1
                for l in llantas:
                    l.pos.z += 0.1
                    l.rotate(angle=0.2, axis=vector(1, 0, 0), origin=l.pos)
            else:
                carro['estado'] = 'estacionado'
                carro['tiempo'] = 0

        elif carro['estado'] == 'estacionado':
            carro['tiempo'] += 1
            if carro['tiempo'] > 200:
                carro['estado'] = 'salida_lateral'

        elif carro['estado'] == 'salida_lateral':
            if not carro['giro_realizado']:
                obj.rotate(angle=radians(90), axis=vector(0, 1, 0), origin=obj.pos)
                for l in llantas:
                    l.rotate(angle=radians(90), axis=vector(0, 1, 0), origin=l.pos)
                carro['giro_realizado'] = True

            if obj.pos.x < 5:
                obj.pos.x += 0.1
                for l in llantas:
                    l.pos.x += 0.1
            else:
                carro['estado'] = 'regreso_a_posicion'

        elif carro['estado'] == 'regreso_a_posicion':
            obj.rotate(angle=radians(-90), axis=vector(0, 1, 0), origin=obj.pos)
            for l in llantas:
                l.rotate(angle=radians(-90), axis=vector(0, 1, 0), origin=l.pos)
            carro['estado'] = 'salida_final'

        elif carro['estado'] == 'salida_final':
            if obj.pos.z < 10:
                obj.pos.z += 0.1
                for l in llantas:
                    l.pos.z += 0.1
            else:
                carros.remove(carro)
                for i in range(4):
                    if carro['objetivo'] == espacios[i]:
                        ocupados[i] = False
                        break

# Bucle principal
while True:
    rate(60)
    actualizar_semaforo()
    mover_carros()

    nuevo_carro_timer += 1
    if nuevo_carro_timer > 300 and len(carros) < max_carros and estado_semaforo == 'verde':
        carros.append(crear_carro(vector(0, 0.25, -12)))
        nuevo_carro_timer = 0

    # Subir la barrera
    if carros and carros[0]['estado'] == 'esperando' and estado_semaforo == 'verde':
        if barrera.rotation < 90:
            barrera.rotate(angle=radians(3), axis=vector(0, 0, 1), origin=pivot_barrera)
            barrera.rotation += 3

    # Bajar la barrera
    if barrera.rotation > 0 and (not carros or carros[0]['obj'].pos.z > -5):
        barrera.rotate(angle=radians(-3), axis=vector(0, 0, 1), origin=pivot_barrera)
        barrera.rotation -= 3

