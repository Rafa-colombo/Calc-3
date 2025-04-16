from vpython import *
import math
import time
import tkinter as tk


Objetos_espaciais = {
    "Terra": 9.81,
    "Marte": 3.71,
    "Júpiter": 24.79,
    "Vênus": 8.87,
    "Lua": 1.62
}

cores_background = [
    vector(0.07056, 0.33882, 0.6000),  # Azul (#1E90FF) - Terra
    vector(0.6000, 0.16236, 0.0000),  # Laranja avermelhado (#FF4500) - Marte
    vector(0.4941, 0.42354, 0.3294),  # Bege (#D2B48C) - Júpiter
    vector(0.6000, 0.50586, 0.0000),  # Dourado (#FFD700) - Vênus
    vector(0.5, 0.5, 0.5)   # Cinza (#C0C0C0) - Lua
]

Materiais_bolinha = { # g/cm^3 para calcular massa
    "Gelo": 0.92,
    "Argila seca": 1.6,
    "Cimento": 3.04,
    "Ferro ": 7.85,
    "Ósmio": 22.5
}

def simulacao_visual(var_planeta,var_bolinha,resultado_texto,razao_entry,altura_entry):

    planeta = var_planeta.get()
    index = list(Objetos_espaciais.keys()).index(planeta)
    gravidade = Objetos_espaciais[planeta]
    index2 = var_bolinha.get()
    Densidade = Materiais_bolinha[index2]

    # Pegando os valores da interface
    razao = float(razao_entry.get())
    if razao < 0 or razao > 1:
        print("")

    altura_inicial = float(altura_entry.get())

    # Criando a cena 3D
    scene = canvas(title=f"Simulação {planeta}", width=900, height=400)
    scene.background = cores_background[index]
    scene.select()
    
    bola = sphere(pos=vector(-15, altura_inicial, 0), radius=0.2, color=color.white, make_trail=True)
    solo = box(pos=vector(bola.pos.x, -1.75, 0), size=vector(0.1, 0.1, 0.1), color=color.orange, make_trail=True)
    
    # Condições iniciais
    theta = 30 * pi / 180
    g = vector(0, -gravidade, 0)

    # Parametros de arrasto
    r   = bola.radius        # raio da bola [m]
    m   = ((4/3) * math.pi * math.pow(r, 3))*float(Densidade)      # Volume * Densidade
    eta = 1.81e-5            # viscosidade do ar [Pa·s]
    b   = 6 * math.pi * eta * r  # coeficiente de Stokes
    
    
    if altura_inicial > 0:
        bola.v = vector(0, 0, 0)  # Solta a bola de altura n
        Energia_p = m * abs(g.y) * altura_inicial # Ep=m⋅g⋅h
        v0_init = math.sqrt((2*Energia_p)/m)
    else:
        v0_init = 10
        bola.v = vector(v0 * cos(theta), v0 * sin(theta), 0) # Lançamento da bola(sai do chao)
    print(f"\nb: {b} stokes m: {m} kg v0: {v0_init}\n")

    t = 0
    dt = 0.001
    
    soma_alturas = 0
    soma_distancias = 0
    
    if altura_inicial == 0:
        h_max_inicial = (v0 ** 2 * sin(theta) ** 2) / (2 * abs(g.y))
    else:
        h_max_inicial = altura_inicial  # Iniciamos com a altura fornecida
    soma_alturas += h_max_inicial
    
    quicadas = 0
    h_max_anterior = bola.pos.y
    
    v0 = v0_init
    while True:
        
        rate(750)
       
        if razao < 0 or razao > 1:
            resultado_texto.config(state=tk.NORMAL)  # Habilita edição no Text
            resultado_texto.delete(1.0, tk.END)  # Limpa os resultados anteriores
            resultado_texto.insert(tk.END, f"Razão inserida não condiz com realidade({razao}).\nDigite novo valor.\n")
            if quicadas > 5: return

        # Atualização da vel e posição da bola
        a_drag   = - (b/m) * bola.v       # vetor de aceleração de arrasto
        a_total  = g + a_drag             # aceleração total
        bola.v   = bola.v + a_total * dt
        bola.pos = bola.pos + bola.v * dt

        t += dt
        
        solo.pos.x = bola.pos.x #Pos do solo
        
        # Verificação colisão com solo
        if bola.pos.y <= solo.pos.y + bola.radius and bola.v.y < 0:
            quicadas += 1
            v0 *= razao
            bola.v = vector(v0 * cos(theta), v0 * sin(theta), 0)
            
            # Atualizar a altura máxima após colisão
            h_max_quicada = (v0 ** 2 * sin(theta) ** 2) / (2 * abs(g.y))
            soma_alturas += h_max_quicada
            
            #erro_relativo = abs(h_max_quicada - h_max_anterior) / abs(h_max_anterior)
            erro_absoluto = abs(h_max_quicada - h_max_anterior)

            print(f"Quicada {quicadas}: Altura = {h_max_quicada}, Erro Absoluto = {erro_absoluto:.4f}")
            if erro_absoluto < 1e-1: break

            h_max_anterior = h_max_quicada

            # Atualizar a distância acumulada
            distancia_acumulada = (bola.v.x * (2 * v0 * sin(theta) / abs(g.y)))
            soma_distancias += distancia_acumulada


    print(f"\nAltura inicial(1): {altura_inicial} metros")
    print(f"Razão(1): {razao}")
    print(f"Número de movimentos(1): {quicadas}")
    print(f"\nSoma geométrica das alturas(1): {soma_alturas:.2f} metros")
    print(f"Soma geométrica das distâncias(1): {soma_distancias:.2f} metros")

    # Atualizando a área de resultados no Tkinter
    resultado_texto.config(state=tk.NORMAL)  # Habilita edição no Text
    resultado_texto.delete(1.0, tk.END)  # Limpa os resultados anteriores
    resultado_texto.insert(tk.END, 
        f"Altura inicial(1): {altura_inicial} metros\n"
        f"Razão(1): {razao}\n"
        f"Número de movimentos(1): {quicadas-1}\n"
        f"--------------\n"
        f"Gravidade: {gravidade}\n"
        f"Planeta: {planeta}\n"
        f"Soma geométrica das alturas(1): {soma_alturas:.2f} metros\n"
        f"Soma geométrica das distâncias(1): {soma_distancias:.2f} metros\n"
        f"Arrasto b: {b:}\nMassa: {m:.6f}kg\nv0: {v0_init:.2f}m/s"
    )
    resultado_texto.config(state=tk.DISABLED)  # Bloqueia edição do Text


def printa_g(var_planeta,var_bolinha,resultado_texto):
    planeta = var_planeta.get()
    index = var_bolinha.get()
    Densidade = Materiais_bolinha[index]
    gravidade = Objetos_espaciais[planeta]
    massa =((4/3) * math.pi * math.pow(0.2, 3))*float(Densidade)

    resultado_texto.config(state=tk.NORMAL)  # Habilita edição no Text
    resultado_texto.delete(1.0, tk.END)  # Limpa os resultados anteriores
    resultado_texto.insert(tk.END, f"Gravidade: {gravidade} \n"
        f"Planeta: {planeta} \n"
        f"Massa da bolinha: {massa} kg\n"  
    )

