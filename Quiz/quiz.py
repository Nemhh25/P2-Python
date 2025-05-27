import random
import tkinter as tk 
from tkinter import messagebox, ttk

# Variáveis globais
perguntas = []
temas = set()
perguntas_quiz = []
respostas_usuario = []
acertos = 0
pergunta_atual = 0
tema_selecionado = ""
qtd_perguntas = 0

# Função para carregar as perguntas do arquivo
def carregar_perguntas(arquivo): 
    global perguntas, temas # Carrega as perguntas do arquivo
    arquivo = open(arquivo, 'r', encoding='utf-8') # Abre o arquivo de perguntas
    linhas = arquivo.readlines() # Lê todas as linhas do arquivo
    arquivo.close()
    
    for linha in linhas:
        partes = linha.strip().split('|')
        if len(partes) >= 7:
            pergunta = {
                'texto': partes[0],
                'tema': partes[1],
                'resposta_correta': int(partes[2]),
                'opcoes': [partes[3], partes[4], partes[5], partes[6]]
            }
            perguntas.append(pergunta)
            temas.add(partes[1])

# Função para confirmar saída do quiz
def confirmar_saida(main):
    resposta = messagebox.askyesno("Sair", "Deseja realmente sair do quiz?")
    if resposta:
        main.destroy()

# Função que define como será a tela inicial
def tela_inicial(main):
    limpar_tela(main)
    
    tk.Label(main, text="Quiz Simplificado", font=('Arial', 20)).pack(pady=20)
    
    # Combobox para selecionar tema
    tk.Label(main, text="Escolha o tema:", font=('Arial', 12)).pack()
    combo_temas = ttk.Combobox(main, values=sorted(temas), font=('Arial', 12))
    combo_temas.pack(pady=10)
    
    # Spinbox para número de perguntas
    tk.Label(main, text="Número de perguntas:", font=('Arial', 12)).pack()
    spin_qtd = tk.Spinbox(main, from_=5, to=20, font=('Arial', 12))
    spin_qtd.pack(pady=10)
    
    # Frame para os botões
    frame_botoes = tk.Frame(main)
    frame_botoes.pack(pady=20)
    
    # Botão Iniciar
    tk.Button(frame_botoes, text="Iniciar Quiz", 
             command=lambda: iniciar_quiz(main, combo_temas.get(), spin_qtd.get()),
             font=('Arial', 12), bg='green', fg='white').pack(side=tk.LEFT, padx=10)
    
    # Botão Sair
    tk.Button(frame_botoes, text="Sair", 
             command=lambda: confirmar_saida(main),
             font=('Arial', 12), bg='red', fg='white').pack(side=tk.LEFT, padx=10)

# Função para limpar a tela
def limpar_tela(main):
    for widget in main.winfo_children(): # Limpa todos os widgets da tela
        widget.destroy()

# Função para iniciar o quiz com o tema e quantidade de perguntas selecionados
def iniciar_quiz(main, tema, qtd):
    global tema_selecionado, qtd_perguntas, perguntas_quiz, pergunta_atual, respostas_usuario, acertos
    
    tema_selecionado = tema
    qtd_perguntas = int(qtd)
    
    perguntas_tema = [p for p in perguntas if p['tema'] == tema_selecionado]
    perguntas_quiz = random.sample(perguntas_tema, min(qtd_perguntas, len(perguntas_tema)))
    pergunta_atual = 0
    respostas_usuario = []
    acertos = 0
    
    mostrar_pergunta(main)

def mostrar_pergunta(main):
    global pergunta_atual, acertos
    limpar_tela(main)
    
    if pergunta_atual >= len(perguntas_quiz):
        mostrar_resultado(main)
        return
    
    pergunta = perguntas_quiz[pergunta_atual]
    
    tk.Label(main, text=f"Pergunta {pergunta_atual+1}/{len(perguntas_quiz)}", 
            font=('Arial', 12)).pack(pady=10)
    
    tk.Label(main, text=pergunta['texto'], font=('Arial', 12), wraplength=550).pack(pady=10)
    
    var_resposta = tk.IntVar()
    
    for i, opcao in enumerate(pergunta['opcoes'], 1):
        tk.Radiobutton(main, text=opcao, variable=var_resposta, 
                      value=i, font=('Arial', 11)).pack(anchor='w', padx=50)
    
    tk.Button(main, text="Próxima" if pergunta_atual < len(perguntas_quiz)-1 else "Finalizar",
             command=lambda: verificar_resposta(main, var_resposta.get()), 
             font=('Arial', 12), bg='blue', fg='white').pack(pady=20)

def verificar_resposta(main, resposta):
    global pergunta_atual, acertos
    
    if not resposta:
        messagebox.showwarning("Aviso", "Selecione uma resposta!")
        return
    
    respostas_usuario.append(resposta)
    
    pergunta = perguntas_quiz[pergunta_atual]
    if resposta == pergunta['resposta_correta']:
        acertos += 1
    
    pergunta_atual += 1
    mostrar_pergunta(main)

def mostrar_resultado(main):
    limpar_tela(main)
    
    tk.Label(main, text="Resultado Final", font=('Arial', 20)).pack(pady=20)
    tk.Label(main, text=f"Você acertou {acertos} de {len(perguntas_quiz)}!", 
            font=('Arial', 14)).pack(pady=10)
    
    # Frame com scroll para os resultados
    frame = tk.Frame(main)
    frame.pack(fill=tk.BOTH, expand=True) 
    
    canvas = tk.Canvas(frame) 
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)
    
    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    # Detalhes das perguntas
    for i, pergunta in enumerate(perguntas_quiz):
        frame_perg = tk.Frame(scrollable_frame, bd=1, relief=tk.GROOVE)
        frame_perg.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(frame_perg, text=f"Pergunta {i+1}: {pergunta['texto']}", 
                font=('Arial', 11), wraplength=500, justify='left').pack(anchor='w')
        
        resposta = respostas_usuario[i]
        correta = pergunta['resposta_correta']
        cor = "green" if resposta == correta else "red"
        
        tk.Label(frame_perg, text=f"Sua resposta: {resposta} ({pergunta['opcoes'][resposta-1]})",
                font=('Arial', 10), fg=cor).pack(anchor='w')
        
        tk.Label(frame_perg, text=f"Resposta correta: {correta} ({pergunta['opcoes'][correta-1]})",
                font=('Arial', 10)).pack(anchor='w')
    
    # Frame para os botões
    frame_botoes = tk.Frame(main)
    frame_botoes.pack(pady=20)
    
    tk.Button(frame_botoes, text="Jogar Novamente", command=lambda: tela_inicial(main),
             font=('Arial', 12), bg='green', fg='white').pack(side=tk.LEFT, padx=10)
    
    tk.Button(frame_botoes, text="Sair", command=lambda: confirmar_saida(main),
             font=('Arial', 12), bg='red', fg='white').pack(side=tk.LEFT, padx=10)

def iniciar_interface():
    main = tk.Tk()
    main.title("Quiz Simplificado")
    
    # Carrega as perguntas e inicia a interface
    carregar_perguntas('QUIZ.TXT')
    tela_inicial(main)
    main.mainloop()

iniciar_interface()