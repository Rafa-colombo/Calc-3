import vpython
from vpython import *
import math
import time
import tkinter as tk


def simulacao():
    # Pegando os valores da interface
    razao = float(razao_entry.get())
    num_quicadas = int(quicadas_entry.get())
    altura_inicial = float(altura_entry.get())
    
    # Criando a cena 3D
    scene = canvas(width=900, height=700)
    scene.select()
    
    bola = sphere(pos=vector(-800, altura_inicial, 0), radius=1.5, color=color.white, make_trail=True)
    solo = box(pos=vector(bola.pos.x, -1.75, 0), size=vector(20, 5, 100), color=color.orange, make_trail=True)
    
    # Condições iniciais
    v0 = 50
    theta = 30 * pi / 180
    g = vector(0, -9.8, 0)
    
    if altura_inicial > 0:
        bola.v = vector(0, 0, 0)  # Começamos com a bola parada e ela cairá devido à gravidade
    else:
        bola.v = vector(v0 * cos(theta), v0 * sin(theta), 0)

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
    
    while quicadas < num_quicadas:

        if num_quicadas <= 10:
            rate(3000)
        elif 10 < num_quicadas <= 20:
            rate(8000)
        else:
            rate(20000)
        
        bola.v = bola.v + g * dt
        bola.pos = bola.pos + bola.v * dt
        t += dt
        
        solo.pos.x = bola.pos.x
        
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


    print(f"\nAltura inicial: {altura_inicial} metros")
    print(f"Razão: {razao}")
    print(f"Número de movimentos: {num_quicadas}")
    print(f"\nSoma geométrica das alturas: {soma_alturas:.2f} metros")
    print(f"Soma geométrica das distâncias: {soma_distancias:.2f} metros")

    # Atualizando a área de resultados no Tkinter
    resultado_texto.config(state=tk.NORMAL)  # Habilita edição no Text
    resultado_texto.delete(1.0, tk.END)  # Limpa os resultados anteriores
    resultado_texto.insert(tk.END, f"Altura inicial: {altura_inicial} metros\n")
    resultado_texto.insert(tk.END, f"Razão: {razao}\n")
    resultado_texto.insert(tk.END, f"Número de movimentos: {num_quicadas}\n\n")
    resultado_texto.insert(tk.END, f"Soma geométrica das alturas: {soma_alturas:.2f} metros\n")
    resultado_texto.insert(tk.END, f"Soma geométrica das distâncias: {soma_distancias:.2f} metros\n")
    resultado_texto.config(state=tk.DISABLED)  # Bloqueia edição do Text


# Criando a interface Tkinter
janela = tk.Tk()
janela.title("Simulação")

# Entradas
tk.Label(janela, text="Razão da Progressão Geométrica:").pack()
razao_entry = tk.Entry(janela)
razao_entry.pack()
razao_entry.insert(0, "1.2")

tk.Label(janela, text="Número de Movimentos:").pack()
quicadas_entry = tk.Entry(janela)
quicadas_entry.pack()
quicadas_entry.insert(0, "5")

tk.Label(janela, text="Altura Inicial:").pack()
altura_entry = tk.Entry(janela)
altura_entry.pack()
altura_entry.insert(0, "0")

# Botão para iniciar
botao = tk.Button(janela, text="Iniciar Simulação", command=simulacao)
botao.pack()

# Área de resultados 
tk.Label(janela, text="Resultados:").pack()
resultado_texto = tk.Text(janela, height=6, width=50)
resultado_texto.pack()
resultado_texto.config(state=tk.DISABLED)  # Deixa o Text como "somente leitura"

janela.mainloop()
