import vpython
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
def simulacao_visual():

    planeta = var_planeta.get()
    index = list(Objetos_espaciais.keys()).index(planeta)
    gravidade = Objetos_espaciais[planeta]

    # Pegando os valores da interface
    razao = float(razao_entry.get())
    if razao < 0 or razao > 1:
        resultado_texto.config(state=tk.NORMAL)  # Habilita edição no Text
        resultado_texto.delete(1.0, tk.END)  # Limpa os resultados anteriores
        resultado_texto.insert(tk.END, f"Razão inserida não condiz com realidade({razao}).\nDigite novo valor.\n")
        return

    altura_inicial = float(altura_entry.get())
    razao_nova = razao * 11.904

    # Criando a cena 3D
    scene = canvas(title=f"Simulação {planeta}", width=900, height=400)
    scene.background = cores_background[index]
    scene.select()
    
    bola = sphere(pos=vector(0, altura_inicial, 0), radius=0.2, color=color.white, make_trail=True)
    solo = box(pos=vector(bola.pos.x, -1.75, 0), size=vector(0.1, 0.1, 0.1), color=color.orange, make_trail=True)
    
    # Condições iniciais
    v0 = 10
    theta = 30 * pi / 180
    g = vector(0, -gravidade, 0)
    
    if altura_inicial > 0:
        bola.v = vector(0, 0, 0)  # Solta a bola de altura n
    else:
        bola.v = vector(v0 * cos(theta), v0 * sin(theta), 0) # Lançamento da bola(sai do chao)

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
    
    while True:
        
        rate(750)
        # Reposiciona a camera a cada quicada
        scene.camera.pos = vector(1 + quicadas*5/abs(g.y), 1, 1 - quicadas*0.8) 

        # Atualização da vel e posição da bola
        bola.v = bola.v + g * dt # v = v0 + g.t
        bola.pos = bola.pos + bola.v * dt # s = s0 + v.t
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
            if erro_absoluto < 1e-3: break

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
    resultado_texto.insert(tk.END, f"Altura inicial(1): {altura_inicial} metros\n")
    resultado_texto.insert(tk.END, f"Razão(1): {razao}\n")
    resultado_texto.insert(tk.END, f"Número de movimentos(1): {quicadas}\n--------------\n")
    resultado_texto.insert(tk.END, f"Gravidade: {gravidade}\n")
    resultado_texto.insert(tk.END, f"Planeta: {planeta} \n")
    resultado_texto.insert(tk.END, f"Soma geométrica das alturas(1): {soma_alturas:.2f} metros\n")
    resultado_texto.insert(tk.END, f"Soma geométrica das distâncias(1): {soma_distancias:.2f} metros\n")
    resultado_texto.config(state=tk.DISABLED)  # Bloqueia edição do Text


def printa_g():
    planeta = var_planeta.get()
    gravidade = Objetos_espaciais[planeta]

    resultado_texto.config(state=tk.NORMAL)  # Habilita edição no Text
    resultado_texto.delete(1.0, tk.END)  # Limpa os resultados anteriores
    resultado_texto.insert(tk.END, f"Gravidade: {gravidade} \n")
    resultado_texto.insert(tk.END, f"Planeta: {planeta} \n")


# Criando a interface Tkinter
janela = tk.Tk()
janela.title("Simulação")
janela.geometry("400x450") 

# Entradas
tk.Label(janela, text="Razão da Progressão Geométrica(Valor entre 0 e 1):").pack()
razao_entry = tk.Entry(janela)
razao_entry.pack()
razao_entry.insert(0, "0.5")

tk.Label(janela, text="Altura Inicial:").pack()
altura_entry = tk.Entry(janela)
altura_entry.pack()
altura_entry.insert(0, "5")

# Menu suspenso para selecionar o Planeta
tk.Label(janela, text="Selecione um objeto espacial:").pack()
var_planeta = tk.StringVar(value=list(Objetos_espaciais.keys())[0])
tk.OptionMenu(janela, var_planeta, *Objetos_espaciais).pack()

# Botões para iniciar as diferentes simulações
tk.Button(janela, text="Iniciar Simulação (Simples)", command=simulacao_visual).pack()
tk.Button(janela, text="Simulação (g)", command=printa_g).pack()

# Área de resultados 
tk.Label(janela, text="Resultados:").pack()
resultado_texto = tk.Text(janela, height=12, width=50)
resultado_texto.pack()
resultado_texto.config(state=tk.DISABLED) 

janela.mainloop()
