from vpython import *
import math
import time
import tkinter as tk
import numpy as np




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

Materiais_bolinha = {
    "Borracha": {"densidade": 1.1, "coef_restituicao": 0.925},         
    "Plástico (PVC)": {"densidade": 1.4, "coef_restituicao": 0.5},     
    "Madeira": {"densidade": 0.8, "coef_restituicao": 0.4},            
    "Gelo": {"densidade": 0.92, "coef_restituicao": 0.25},             
    "Cimento": {"densidade": 2.3, "coef_restituicao": 0.55},           
    "Ferro": {"densidade": 7.85, "coef_restituicao": 0.65},            
    "Aço": {"densidade": 7.85, "coef_restituicao": 0.85},              
    "Ósmio": {"densidade": 22.5, "coef_restituicao": 0.65}             
}


def simulacao_visual(var_planeta,var_bolinha,resultado_texto,razao_entry,altura_entry,v0_entry,usar_coef_material):

    planeta = var_planeta.get()
    index = list(Objetos_espaciais.keys()).index(planeta)
    gravidade = Objetos_espaciais[planeta]

    material = var_bolinha.get()
    propriedades_material = Materiais_bolinha[material]
    Densidade = Materiais_bolinha[material]["densidade"]
    if usar_coef_material:
        razao = propriedades_material["coef_restituicao"]
        print(f">>> Usando coef. do material: {razao}")
    else:
        # Pegando os valores da interface
        razao = float(razao_entry.get())
        print(f">>> Usando razão digitada: {razao}")


    altura_inicial = float(altura_entry.get())
    v0 = float(v0_entry.get())

    # Criando a cena 3D
    scene = canvas(title=f"Simulação {planeta}", width=700, height=300)
    scene.background = cores_background[index]
    scene.select()

    # Ajuste de centro da câmera
    scene.center = vector(0, altura_inicial / 2, 0)  
    
    bola = sphere(pos=vector(-1, altura_inicial, 0), radius=0.1, color=color.white, make_trail=True)
    solo = box(pos=vector(bola.pos.x, -0.05, 0), size=vector(0.1, 0.1, 0.1), color=color.orange, make_trail=True)
    
    # Condições iniciais
    theta = radians(45)   # Ângulo de lançamento
    g = vector(0, -gravidade, 0)
    t = 0
    dt = 0.001

    # Parametros de arrasto
    r   = bola.radius        # raio da bola [m]
    m   = ((4/3) * math.pi * math.pow(r, 3))*float(Densidade)      # Volume * Densidade
    eta = 1.81e-5            # viscosidade do ar [Pa·s]
    b   = 6 * math.pi * eta * r  # coeficiente de Stokes
    print(f"b: {b} N·s/m m: {m:.6f} kg v0: {v0} m/s Densidade: {Densidade:.6f} g/cm^3\n")

  
    bola.v = vector(v0 * math.cos(theta), v0 * math.sin(theta), 0)
    bola.pos = vector(0, altura_inicial, 0)  
    
    lista_alturas = []
    lista_distancias = []
    soma_alturas = 0
    soma_distancias = 0

    x0_t = bola.pos.x # pos init x
    y0_t = bola.pos.y # pos init y
    posicao_x_anterior = x0_t
    detectando_altura = True

    quicadas = 0
    
    lista_alturas.append(y0_t)
    time.sleep(2)
    while True:
        
        rate(750) 

        # Atualização da vel e posição da bola
        a_drag   = - (b/m) * bola.v       # vetor de aceleração de arrasto
        a_x = a_drag.x       # aceleração total em x
        a_y = g.y + a_drag.y # aceleração total em y
                 
        a_total = vector(a_x, a_y, 0) # aceleração total

        bola.v += a_total * dt
        bola.pos += bola.v * dt
        t += dt

        print(f"X(t) = {bola.pos.x:.2f} Y(t) = {bola.pos.y:.2f}; a total {a_total}; v total {bola.v}")
        
        solo.pos.x = bola.pos.x # Pos do solo

        # Tratar razão errada
        if razao < 0 or razao > 1:
            resultado_texto.config(state=tk.NORMAL)  
            resultado_texto.delete(1.0, tk.END)  # Limpa os resultados anteriores
            resultado_texto.insert(tk.END, f"Razão inserida não condiz com realidade({razao}).\nDigite novo valor.\n")
            if quicadas > 5: return
        
        # ----- DETECTAR ALTURA MÁXIMA -----
        if detectando_altura and bola.v.y < 0: # ao inves de verificar vel, ver quando vetor y troca de sinal
            h_max_quicada = bola.pos.y
            lista_alturas.append(h_max_quicada)
            soma_alturas += bola.pos.y
            detectando_altura = False

        # ----- VERIFICA COLISÃO COM SOLO -----
        if bola.pos.y <= solo.pos.y + bola.radius and bola.v.y < 0:

            bola.pos.y = solo.pos.y + bola.radius # reposicionar bolinha

            # Nova velocidade e energia reduzida 
            bola.v = vector(razao * bola.v.x, razao * -bola.v.y, 0)
            print(f"Vel pós razão: {bola.v}")

            quicadas += 1
            detectando_altura = True # Permite detectar prox altura

            # Salvar distância horizontal desde a última quicada
            distancia_quicada = abs(bola.pos.x - posicao_x_anterior)
            lista_distancias.append(distancia_quicada)
            soma_distancias += distancia_quicada
            posicao_x_anterior = bola.pos.x

            if len(lista_alturas) != 0:
                if len(lista_alturas) == 1: erro_a = abs(h_max_quicada - y0_t)
                else: erro_a = abs(h_max_quicada - lista_alturas[quicadas-1])

            print(f"Quicada {quicadas}: Altura = {h_max_quicada}") 
            print(f"Erro Relativo = {erro_a:.4f}")
            
            if erro_a < 1e-5:
                print("Erro relativo abaixo do limiar. Encerrando simulação.")
                break
            elif h_max_quicada < 0:
                print("Erro quicada com solo. Encerrando simulação.")
                break



    plot_exp(lista_alturas,lista_distancias)
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
        f"Arrasto b: {b:} N·s/m\nMassa: {m:.6f} kg\nv0: {v0:.6f} m/s"
    )
    resultado_texto.config(state=tk.DISABLED)  # Bloqueia edição do Text


def printa_g(var_planeta,var_bolinha,resultado_texto,v0_entry):
    planeta = var_planeta.get()
    material = var_bolinha.get()
    Densidade = Materiais_bolinha[material]["densidade"]
    razao = Materiais_bolinha[material]["coef_restituicao"]
    gravidade = Objetos_espaciais[planeta]
    massa =((4/3) * math.pi * math.pow(0.2, 3))*float(Densidade)

    resultado_texto.config(state=tk.NORMAL)  # Habilita edição no Text
    resultado_texto.delete(1.0, tk.END)  # Limpa os resultados anteriores
    resultado_texto.insert(tk.END, f"Gravidade: {gravidade} \n"
        f"Planeta: {planeta} \n"
        f"Massa da bolinha: {massa:.3f} kg\nDensidade: {Densidade:.3f}"  
    )


def plot_exp(lista_alturas,lista_distancias):

    if not lista_alturas or len(lista_alturas) <= 3:
        print("Alturas insuficientes para plotagem.")
        return

    # Altura inicial (primeiro valor da lista)
    h_0 = lista_alturas[0]
    lista_distancias = [0] + lista_distancias

   
    grafico_a = graph(title='Valor de Altura (m) vs Quiques',
                    xtitle='Quiques', ytitle='Altura (m)',
                    width=500, height=300, background=color.white)


    curva_altura  = gcurve(graph=grafico_a,color=color.blue, label='Altura (m) vs Quiques')


    for i, h in enumerate(lista_alturas[1:]):
        if i == 1: print("Alturas fornecidas:",len(lista_alturas), lista_alturas)
        curva_altura.plot(i, h)

  
    grafico_b = graph(title='Valor de Distancia (m) vs Quiques',
                    xtitle='Quiques', ytitle='Distancia (m)',
                    width=500, height=300, background=color.white)

    curva_distancia  = gcurve(graph=grafico_b,color=color.red, label='Distancia (m) vs Quiques')

    for i, d in enumerate(lista_distancias[1:]):
        if i == 1: print("Distancias fornecidas:",len(lista_distancias), lista_distancias)
        curva_distancia.plot(i, d)