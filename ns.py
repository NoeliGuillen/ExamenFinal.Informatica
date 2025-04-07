from vpython import *
import time

# Escena
scene = canvas(title="Simulación Estacionamiento con Semáforo", width=800, height=600)

# Suelo
piso = box(pos=vector(0, -0.1, 0), size=vector(20, 0.1, 20), color=color.gray(0.5))

# Semáforo
poste = cylinder(pos=vector(7, -0.1, -8), axis=vector(0, 5, 0), radius=0.2, color=color.white)
caja = box(pos=vector(7, 4, -8), size=vector(1, 2, 1), color=color.black)
luz_roja = sphere(pos=vector(7, 4.5, -7.5), radius=0.2, color=color.gray(0.2))
luz_verde = sphere(pos=vector(7, 3.5, -7.5), radius=0.2, color=color.green)

# Semáforo independiente (inicia en verde)
semaforo_estado = "verde"
ultimo_cambio = time.time()
verde_duracion = 13
rojo_duracion = 8

# Barrera (grande y amarilla)
base_barrera = vector(-1.5, 0.1, -9)
barrera = box(pos=base_barrera + vector(0, 1.5, 0), size=vector(0.2, 3, 0.2), color=color.yellow)
barrera.rotation = 0

# Espacios de estacionamiento
espacios = [vector(0, 0.25, 6 - i*3) for i in range(4)]
ocupados = [False] * 4

# Crear carro
def crear_carro(pos_inicial):
    cuerpo = box(pos=pos_inicial, size=vector(1, 0.5, 2), color=color.cyan)
    llantas = []
    for dx in [-0.5, 0.5]:
        for dz in [-0.6, 0.6]:
            pos_llanta = cuerpo.pos + vector(dx, -0.25, dz)
            llanta = cylinder(pos=pos_llanta, axis=vector(0, 0.3, 0), radius=0.25, color=color.black)
            llantas.append(llanta)
    return {'obj': cuerpo, 'llantas': llantas, 'estado': 'esperando', 'objetivo': None, 'tiempo': 0, 'paso_barrera': False, 'giro_realizado': False}

# Carros
carros = []
nuevo_carro_timer = 0
max_carros = 1

# Mover carros
def mover_carros():
    for carro in list(carros):
        obj = carro['obj']
        llantas = carro['llantas']
        velocidad = 0.08

        if carro['estado'] == 'esperando':
            # SOLO si el semáforo está en VERDE
            if semaforo_estado == "verde" and barrera.rotation >= 85:
                obj.pos.z += velocidad
                for l in llantas:
                    l.pos.z += velocidad
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
                obj.pos.z += velocidad
                for l in llantas:
                    l.pos.z += velocidad
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
                obj.pos.x += velocidad
                for l in llantas:
                    l.pos.x += velocidad
            else:
                carro['estado'] = 'regreso_a_posicion'

        elif carro['estado'] == 'regreso_a_posicion':
            obj.rotate(angle=radians(-90), axis=vector(0, 1, 0), origin=obj.pos)
            for l in llantas:
                l.rotate(angle=radians(-90), axis=vector(0, 1, 0), origin=l.pos)
            carro['estado'] = 'salida_final'

        elif carro['estado'] == 'salida_final':
            if obj.pos.z < 10:
                obj.pos.z += velocidad
                for l in llantas:
                    l.pos.z += velocidad
            else:
                carros.remove(carro)
                for i in range(4):
                    if carro['objetivo'] == espacios[i]:
                        ocupados[i] = False
                        break

# Bucle principal
while True:
    rate(60)

    # ⏱ Control del semáforo independiente
    ahora = time.time()
    if semaforo_estado == "verde" and ahora - ultimo_cambio >= verde_duracion:
        semaforo_estado = "rojo"
        ultimo_cambio = ahora
        luz_verde.color = color.gray(0.2)
        luz_roja.color = color.red
    elif semaforo_estado == "rojo" and ahora - ultimo_cambio >= rojo_duracion:
        semaforo_estado = "verde"
        ultimo_cambio = ahora
        luz_roja.color = color.gray(0.2)
        luz_verde.color = color.green

    # Crear nuevos carros
    nuevo_carro_timer += 1
    if nuevo_carro_timer > 300 and len(carros) < max_carros:
        carros.append(crear_carro(vector(0, 0.25, -12)))
        nuevo_carro_timer = 0

    # Mover los carros
    mover_carros()

    # Barrera automática
    if carros and carros[0]['estado'] == 'esperando' and semaforo_estado == "verde":
        if barrera.rotation < 90:
            barrera.rotate(angle=radians(3), axis=vector(0, 0, 1), origin=base_barrera)
            barrera.rotation += 3
    elif barrera.rotation > 0 and (not carros or carros[0]['obj'].pos.z > -5):
        barrera.rotate(angle=radians(-3), axis=vector(0, 0, 1), origin=base_barrera)
        barrera.rotation -= 3

