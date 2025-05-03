from function import *
import tkinter as tk

# Criando a interface Tkinter
janela = tk.Tk()
janela.title("Simulação")
janela.geometry("400x500")

# Entradas
tk.Label(janela, text="Razão da Progressão Geométrica (Valor entre 0 e 1):").pack(pady=5)
razao_entry = tk.Entry(janela)
razao_entry.pack()
razao_entry.insert(0, "0.5")

tk.Label(janela, text="Altura Inicial:").pack(pady=5)
altura_entry = tk.Entry(janela)
altura_entry.pack()
altura_entry.insert(0, "5")

tk.Label(janela, text="v0 (força de lançamento): ").pack(pady=5)
v0_entry = tk.Entry(janela)
v0_entry.pack()
v0_entry.insert(0, "10")

# Frame para menus suspensos (lado a lado)
frame_menus = tk.Frame(janela)
frame_menus.pack(pady=10)

# Variável para armazenar o estado da checkbox
usar_coef_material = tk.BooleanVar(value=False)  # Começa desmarcada
checkbox = tk.Checkbutton(janela, text="Usar coeficiente do material", variable=usar_coef_material)
checkbox.pack()

# Menu Planeta
tk.Label(frame_menus, text="Planeta:").pack(side=tk.LEFT, padx=5)
var_planeta = tk.StringVar(value=list(Objetos_espaciais.keys())[0])
tk.OptionMenu(frame_menus, var_planeta, *Objetos_espaciais).pack(side=tk.LEFT, padx=5)

# Menu Bolinha
tk.Label(frame_menus, text="Material:").pack(side=tk.LEFT, padx=5)
var_bolinha = tk.StringVar(value=list(Materiais_bolinha.keys())[0])
tk.OptionMenu(frame_menus, var_bolinha, *Materiais_bolinha).pack(side=tk.LEFT, padx=5)

# Frame para os botões (lado a lado)
frame_botoes = tk.Frame(janela)
frame_botoes.pack(pady=10)

tk.Button(frame_botoes, text="Iniciar Simulação (Simples)", 
        command=lambda: simulacao_visual(var_planeta,var_bolinha,resultado_texto,razao_entry,altura_entry,v0_entry,usar_coef_material.get())
        ).pack(side=tk.LEFT, padx=10)
tk.Button(frame_botoes, text="Simulação (g)", 
        command=lambda: printa_g(var_planeta, var_bolinha, resultado_texto, v0_entry)
        ).pack(side=tk.LEFT, padx=10)

# Área de resultados
tk.Label(janela, text="Resultados:").pack(pady=5)
resultado_texto = tk.Text(janela, height=12, width=60)
resultado_texto.pack()
resultado_texto.config(state=tk.DISABLED)

janela.mainloop()
