import vpython
from vpython import *
import math
import time

# Entrada de valores pelo console
razao = 1.2#float(input("Defina a razão da progressão geométrica: "))
num_quicadas = 10#int(input("Escolha o número de movimentos: "))
altura_inicial = 0#float(input("Defina a altura inicial da bola: "))

# Definições da cena
scene.background = color.black
scene.width = 800  # Largura 
scene.height = 600 # Altura

# Objetos
bola = sphere(pos=vector(-800, altura_inicial, 0), radius=1.5, color=color.white, make_trail=True)
solo = box(pos=vector(bola.pos.x, -1.75, 0), size=vector(20, 5, 100), color=color.orange, make_trail=True)

# Condições iniciais
v0 = 50
theta = 30 * pi / 180
g = vector(0, -10, 0)

# Se a altura inicial for maior que zero, ajustamos a velocidade inicial vertical
if altura_inicial > 0:
    bola.v = vector(0, 0, 0)  # Começamos com a bola parada e ela cairá devido à gravidade
else:
    bola.v = vector(v0 * cos(theta), v0 * sin(theta), 0)

t = 0
dt = 0.001

# Soma geométrica das alturas e distâncias
soma_alturas = 0
soma_distancias = 0

# Se a altura inicial for zero, calculamos a altura máxima normal; caso contrário, começamos da altura inicial
if altura_inicial == 0:
    h_max_inicial = (v0 ** 2 * sin(theta) ** 2) / (2 * abs(g.y))
else:
    h_max_inicial = altura_inicial  # Iniciamos com a altura fornecida
soma_alturas += h_max_inicial

# Contador de quicadas
quicadas = 0

# Equações do movimento
while quicadas < num_quicadas:
    
    if num_quicadas <= 10:
        rate(3000)
    elif 10 < num_quicadas <= 20:
        rate(8000)
    else:
        rate(20000)

    bola.v = bola.v + g * dt
    bola.pos = bola.pos + bola.v * dt
    t = t + dt

    solo.pos.x = bola.pos.x 

    # Se a bola atingir o solo e estiver caindo, ocorre uma quicada
    if bola.pos.y <= solo.pos.y + bola.radius and bola.v.y < 0:
        quicadas += 1
        v0 *= razao
        bola.v = vector(v0 * cos(theta), v0 * sin(theta), 0)

        # Atualizar a altura máxima após colisão
        h_max_quicada = (v0 ** 2 * sin(theta) ** 2) / (2 * abs(g.y))
        soma_alturas += h_max_quicada

        # Atualizar a distância acumulada
        distancia_acumulada = (bola.v.x * (2 * v0 * sin(theta) / abs(g.y)))
        soma_distancias += distancia_acumulada

# Exibir valores no terminal
print(f"\nAltura inicial: {altura_inicial} metros")
print(f"Razão: {razao}")
print(f"Número de movimentos: {num_quicadas}")
print(f"\nSoma geométrica das alturas: {soma_alturas:.2f} metros")
print(f"Soma geométrica das distâncias: {soma_distancias:.2f} metros")

# Manter a tela de exibição aberta por 10 segundos
while True:
    
    rate(10)
    time.sleep(10)
    break
