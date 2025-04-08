from vpython import *
import time
import random

# Configuración inicial
scene = canvas(title="Simulación Estacionamiento", width=800, height=600)
scene.background = color.cyan
# Suelo
piso = box(pos=vector(0, -0.1, 0), size=vector(25, 0.1, 20), color=color.gray(0.5))

# Semáforo (inicia en verde)
poste = cylinder(pos=vector(7, -0.1, -8), axis=vector(0, 5, 0), radius=0.2, color=color.white)
caja = box(pos=vector(7, 4, -8), size=vector(1, 2, 1), color=color.black)
luz_roja = sphere(pos=vector(7, 4.5, -7.5), radius=0.2, color=color.gray(0.2))
luz_verde = sphere(pos=vector(7, 3.5, -7.5), radius=0.2, color=color.green)

# Barrera
poste = cylinder(pos=vector(1.5, 0.1, -9), axis=vector(0, 2.5, 0), radius=0.2, color=color.white)
pivot_barrera = vector(1.5, 1.5, -9)
barrera = box(pos=pivot_barrera + vector(0, 2, 0), size=vector(0.5, 5, 0.5), color=color.yellow)
barrera.rotation = 0  # Empieza arriba


# Crear árboles fuera del cuadro gris (suelo)
tronco1 = cylinder(pos=vector(random.uniform(-12, -15), 0, random.uniform(12, 15)), axis=vector(0, 3, 0), radius=0.3, color=color.red)
hoja1_1 = sphere(pos=tronco1.pos + vector(0, 3.5, 0), radius=1.2, color=color.green)
hoja1_2 = sphere(pos=tronco1.pos + vector(-0.7, 3.7, 0.5), radius=1, color=color.green)
hoja1_3 = sphere(pos=tronco1.pos + vector(0.7, 3.7, -0.5), radius=1, color=color.green)
hoja1_4 = sphere(pos=tronco1.pos + vector(0, 4.3, 0), radius=0.9, color=color.green)

tronco2 = cylinder(pos=vector(random.uniform(12, 15), 0, random.uniform(12, 15)), axis=vector(0, 3, 0), radius=0.3, color=color.red)
hoja2_1 = sphere(pos=tronco2.pos + vector(0, 3.5, 0), radius=1.2, color=color.green)
hoja2_2 = sphere(pos=tronco2.pos + vector(-0.7, 3.7, 0.5), radius=1, color=color.green)
hoja2_3 = sphere(pos=tronco2.pos + vector(0.7, 3.7, -0.5), radius=1, color=color.green)
hoja2_4 = sphere(pos=tronco2.pos + vector(0, 4.3, 0), radius=0.9, color=color.green)

tronco3 = cylinder(pos=vector(random.uniform(-12, -15), 0, random.uniform(-15, -12)), axis=vector(0, 3, 0), radius=0.3, color=color.red)
hoja3_1 = sphere(pos=tronco3.pos + vector(0, 3.5, 0), radius=1.2, color=color.green)
hoja3_2 = sphere(pos=tronco3.pos + vector(-0.7, 3.7, 0.5), radius=1, color=color.green)
hoja3_3 = sphere(pos=tronco3.pos + vector(0.7, 3.7, -0.5), radius=1, color=color.green)
hoja3_4 = sphere(pos=tronco3.pos + vector(0, 4.3, 0), radius=0.9, color=color.green)

tronco4 = cylinder(pos=vector(random.uniform(12, 15), 0, random.uniform(-15, -12)), axis=vector(0, 3, 0), radius=0.3, color=color.red)
hoja4_1 = sphere(pos=tronco4.pos + vector(0, 3.5, 0), radius=1.2, color=color.green)
hoja4_2 = sphere(pos=tronco4.pos + vector(-0.7, 3.7, 0.5), radius=1, color=color.green)
hoja4_3 = sphere(pos=tronco4.pos + vector(0.7, 3.7, -0.5), radius=1, color=color.green)
hoja4_4 = sphere(pos=tronco4.pos + vector(0, 4.3, 0), radius=0.9, color=color.green)

tronco5 = cylinder(pos=vector(random.uniform(-18, -25), 0, random.uniform(-8, 8)), axis=vector(0, 3, 0), radius=0.3, color=color.red)
hoja5_1 = sphere(pos=tronco5.pos + vector(0, 3.5, 0), radius=1.2, color=color.green)
hoja5_2 = sphere(pos=tronco5.pos + vector(-0.7, 3.7, 0.5), radius=1, color=color.green)
hoja5_3 = sphere(pos=tronco5.pos + vector(0.7, 3.7, -0.5), radius=1, color=color.green)
hoja5_4 = sphere(pos=tronco5.pos + vector(0, 4.3, 0), radius=0.9, color=color.green)

tronco6 = cylinder(pos=vector(random.uniform(18, 25), 0, random.uniform(-8, 8)), axis=vector(0, 3, 0), radius=0.3, color=color.red)
hoja6_1 = sphere(pos=tronco6.pos + vector(0, 3.5, 0), radius=1.2, color=color.green)
hoja6_2 = sphere(pos=tronco6.pos + vector(-0.7, 3.7, 0.5), radius=1, color=color.green)
hoja6_3 = sphere(pos=tronco6.pos + vector(0.7, 3.7, -0.5), radius=1, color=color.green)
hoja6_4 = sphere(pos=tronco6.pos + vector(0, 4.3, 0), radius=0.9, color=color.green)

# Espacios de estacionamiento
espacios = [vector(0, 0.25, 6 - i*4) for i in range(4)]  # Aumenté la distancia entre espacios
ocupados = [False] * 4

# Carros estáticos en las orillas (2 filas a cada lado, al lado, no detrás)
def crear_carro_estatico(pos, color_carro=color.blue):
    cuerpo = box(pos=pos, size=vector(2, 1, 4), color=color_carro)
    cylinder(pos=pos + vector(-1, -0.5, -1.2), axis=vector(0, 0.6, 0), radius=0.3, color=color.gray(0.5))  
    cylinder(pos=pos + vector(-1, -0.5, 1.2), axis=vector(0, 0.6, 0), radius=0.3, color=color.gray(0.5))  
    cylinder(pos=pos + vector(1, -0.5, -1.2), axis=vector(0, 0.6, 0), radius=0.3, color=color.gray(0.5))  
    cylinder(pos=pos + vector(1, -0.5, 1.2), axis=vector(0, 0.6, 0), radius=0.3, color=color.gray(0.5))  

# Crear carros estáticos
crear_carro_estatico(vector(-6, 0.5, 9), color.yellow)
crear_carro_estatico(vector(-6, 0.5, 4), color.red)
crear_carro_estatico(vector(-6, 0.5, -2), color.cyan)
crear_carro_estatico(vector(-6, 0.5, -8), color.blue)
crear_carro_estatico(vector(-9, 0.5, 9), color.green)
crear_carro_estatico(vector(-9, 0.5, 4), color.white)
crear_carro_estatico(vector(-9, 0.5, -2), color.yellow)
crear_carro_estatico(vector(-9, 0.5, -8), color.red)
crear_carro_estatico(vector(9, 0.5, 9), color.cyan)
crear_carro_estatico(vector(9, 0.5, 4), color.red)
crear_carro_estatico(vector(9, 0.5, -2), color.green)
crear_carro_estatico(vector(9, 0.5, -8), color.white)
crear_carro_estatico(vector(12, 0.5, 9), color.yellow)
crear_carro_estatico(vector(12, 0.5, 4), color.blue)
crear_carro_estatico(vector(12, 0.5, -2), color.cyan)
crear_carro_estatico(vector(12, 0.5, -8), color.green)

# Carros móviles
def crear_carro(pos_inicial):
    color_carro = vector(random.random(), random.random(), random.random())  # Color aleatorio
    cuerpo = box(pos=pos_inicial, size=vector(2.4, 1.2, 4.8), color=color_carro)  
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
            if barrera.rotation <= 0:  # La barrera está bajada (cerrada)
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

    # Bajar la barrera si hay un carro esperando
    if carros and carros[0]['estado'] == 'esperando' and estado_semaforo == 'verde':
        if barrera.rotation > 0:
            barrera.rotate(angle=radians(-3), axis=vector(0, 0, 1), origin=pivot_barrera)
            barrera.rotation -= 3

    # Subir la barrera si el carro ya pasó
    if barrera.rotation < 90 and (not carros or carros[0]['obj'].pos.z > -5):
        barrera.rotate(angle=radians(3), axis=vector(0, 0, 1), origin=pivot_barrera)
        barrera.rotation += 3
