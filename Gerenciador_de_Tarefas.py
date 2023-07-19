import tkinter as tk
from tkinter import messagebox as mb
import sqlite3
import datetime

conexão = sqlite3.connect('database.db')

cursor = conexão.cursor()

usuario_ativo = []

cursor.execute("""CREATE TABLE IF NOT EXISTS tarefas(
                Usuario varchar(50) NOT NULL,
                Tarefa varchar(50) NOT NULL,
                Descrição varchar(50),
                Data text,
                Prioridade int
                )""")

cursor.execute("""CREATE TABLE IF NOT EXISTS usuarios(
                Usuario varchar(50) NOT NULL PRIMARY KEY,
                Senha varchar(50) NOT NULL
               )""")



def login():

    def logar():
        usuario = usuario_entry.get()
        senha = senha_entry.get()

 
        cursor.execute("SELECT Usuario FROM usuarios WHERE Usuario=? AND Senha=?", (usuario, senha))
        checkUser = cursor.fetchone()
        
        try:
            if checkUser is not None:
                if len(usuario_ativo) > 0:
                    usuario_ativo.pop()
                    usuario_ativo.append(checkUser[0])
                else:
                    usuario_ativo.append(checkUser[0])

                usuario_ativo_replace = str(usuario_ativo[0])
                
                tarefas(usuario_ativo_replace)

            else:
                mb.showerror("ERRO", "USUARIO OU SENHA INCORRETOS")
                usuario_entry.delete(0, tk.END)
                senha_entry.delete(0, tk.END)

        except Exception as e:
            print(e)
            mb.showerror("ERRO", "OCORREU UM ERRO AO REALIZAR O LOGIN")


    janela_login = tk.Tk()

    janela_login.title("Login")

    base = 250
    altura = 275

    base_tela= janela_login.winfo_screenwidth()
    altura_tela = janela_login.winfo_screenheight()

    x = (base_tela/2) - (base/2)
    y = (altura_tela/2) - (altura/2)

    janela_login.geometry('%dx%d+%d+%d' % (base, altura, x, y))

    usuario_label = tk.Label(janela_login, text="Usuario", font=("Impact", 12))
    usuario_label.place(x=5, y=30)

    usuario_entry = tk.Entry(janela_login, font=("Arial", 12), width=26)
    usuario_entry.place(x=5, y=60)

    senha_label = tk.Label(janela_login, text="Senha", font=("Impact", 12))
    senha_label.place(x=5, y=100)

    senha_entry = tk.Entry(janela_login, font=("Arial", 12), width=26)
    senha_entry.place(x=5, y=130)

    entrar = tk.Button(janela_login, text="Entrar", command=logar, font=("Impact", 12), width=15)
    entrar.place(x=63, y=170)

    cadastro_button = tk.Button(janela_login, text="Cadastrar", font=("Times", 12), fg="blue", border=0, command=cadastro)
    cadastro_button.place(x=5, y=210)

    janela_login.mainloop()

def cadastro():

    def cadastrar():
        Usuario = usuario_entry.get()
        Senha = senha_entry.get()
        Confirmar_Senha = confirmar_senha_entry.get()

        if Senha == Confirmar_Senha:
            
            cursor.execute("INSERT INTO usuarios (Usuario, Senha) VALUES (?, ?)", (Usuario, Senha))

            conexão.commit()
            usuario_entry.delete(0, tk.END)
            senha_entry.delete(0, tk.END)
            confirmar_senha_entry.delete(0, tk.END)

            janela_cadastro.destroy()
        
        else:
            mb.showerror("ERRO", "AS SENHAS NÃO SÃO IGUAIS")

            usuario_entry.delete(0, tk.END)
            senha_entry.delete(0, tk.END)
            confirmar_senha_entry.delete(0, tk.END)

    janela_cadastro = tk.Tk()

    janela_cadastro.title("Cadastro")

    base = 250
    altura = 290

    base_tela= janela_cadastro.winfo_screenwidth()
    altura_tela = janela_cadastro.winfo_screenheight()

    x = (base_tela/2) - (base/2)
    y = (altura_tela/2) - (altura/2)

    janela_cadastro.geometry('%dx%d+%d+%d' % (base, altura, x, y))

    usuario_label = tk.Label(janela_cadastro, text="Usuario", font=("Impact", 12))
    usuario_label.place(x=5, y=30)

    usuario_entry = tk.Entry(janela_cadastro, font=("Arial", 12), width=26)
    usuario_entry.place(x=5, y=60)

    senha_label = tk.Label(janela_cadastro, text="Senha", font=("Impact", 12))
    senha_label.place(x=5, y=100)

    senha_entry = tk.Entry(janela_cadastro, font=("Arial", 12), width=26)
    senha_entry.place(x=5, y=130)

    confirmar_senha_label = tk.Label(janela_cadastro, text="Confirmar Senha", font=("Impact", 12))
    confirmar_senha_label.place(x=5, y=170)

    confirmar_senha_entry = tk.Entry(janela_cadastro, font=("Arial", 12), width=26)
    confirmar_senha_entry.place(x=5, y=200)

    entrar = tk.Button(janela_cadastro, text="Cadastro", command=cadastrar, font=("Impact", 12), width=15)
    entrar.place(x=63, y=240)

    janela_cadastro.mainloop()

def tarefas(usuario):

    usuativo = str(usuario)

    janela_tarefas = tk.Toplevel()

    janela_tarefas.title("Tarefas")

    base = 400
    altura = 400

    base_tela = janela_tarefas.winfo_screenwidth()
    altura_tela = janela_tarefas.winfo_screenheight()

    x = (base_tela/2) - (base/2)
    y = (altura_tela/2) - (altura/2)

    janela_tarefas.geometry('%dx%d+%d+%d' % (base, altura, x, y))

    def limpar():
        for checkbox in check_box_list:
            if checkbox[0].get() == 1:
                checkbox[1].destroy()
                tarefa = checkbox[2]
                cursor.execute("DELETE FROM tarefas WHERE Tarefa =?", (tarefa,))
        conexão.commit()
        check_box_list[:] = []
    
    canvas = tk.Canvas(janela_tarefas)
    canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    scrollbar = tk.Scrollbar(janela_tarefas, command=canvas.yview)
    scrollbar.pack(side=tk.LEFT, fill=tk.Y)

    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=frame, anchor="n")

    tk.Label(frame, text="Tarefas", font=("Impact", 25)).pack()

    tk.Button(frame, text="Adicionar Tarefa", command=lambda: [janela_tarefas.destroy(), criar(usuario)]).pack()

    tk.Button(frame, text="Apagar Concluidas", command=limpar).pack()

    tk.Button(frame, text="Sair", command=janela_tarefas.destroy).pack(side=tk.BOTTOM)

    cursor.execute(f"SELECT * FROM tarefas WHERE Usuario='{usuativo}' ORDER BY Prioridade DESC, Data ASC")
    Tarefas = cursor.fetchall()

    check_box_list = []

    for i in Tarefas:
        tarefa = i[0]
        Status = tk.IntVar()
        data_formatada = datetime.datetime.strptime(i[3], "%Y-%m-%d").strftime("%d/%m/%Y")
        checkbox = (Status, tk.Checkbutton(frame, text=f"Tarefa: {i[1]} \n Descrição: {i[2]} \n Data: {data_formatada} \n Prioridade: {i[4]}", offvalue=0, onvalue=1, variable=Status), tarefa)
        checkbox[1].pack(fill=tk.X)
        check_box_list.append(checkbox)

    canvas.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("w"))

    janela_tarefas.mainloop()

def criar(usuario_tarefa):
    def confirmar():
        var_nome = entry_nome.get()

        if var_nome.strip() == "":

            mb.showerror("ERRO", "A TAREFA PRECISA DE UM NOME")
        
        else:
            try: 
                data = datetime.date(var_ano.get(), var_meses.get(), var_dias.get())
                data_iso = data.isoformat()

                cursor.execute("INSERT INTO tarefas VALUES (:Usuario, :Nome, :Descrição, :Data, :Prioridade)", 
                                {
                                    'Usuario': usuario_tarefa,
                                    'Nome': entry_nome.get(),
                                    'Descrição': entry_descrição.get(),
                                    'Data': data_iso,
                                    'Prioridade': var_prioridade.get()
                                })
                conexão.commit()
                entry_nome.delete(0, tk.END)
                entry_descrição.delete(0, tk.END)
                var_dias.set(lista_dias[0])
                var_meses.set(lista_meses[0])
                var_prioridade.set(nvl_prioridade[0])
            
            except:
                mb.showerror("ERRO", "ESSA DATA NÃO É VALIDA")
    
    janela_criar = tk.Tk()
    janela_criar.title("Criar Tarefa")

    base = 500
    altura = 190

    base_tela= janela_criar.winfo_screenwidth()
    altura_tela = janela_criar.winfo_screenheight()

    x = (base_tela/2) - (base/2)
    y = (altura_tela/2) - (altura/2)

    lista_meses = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    lista_dias = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]
    lista_ano = [2023, 2024, 2025, 2026, 2027, 2028, 2029]

    nvl_prioridade = [1, 2, 3, 4, 5]

    janela_criar.geometry('%dx%d+%d+%d' % (base, altura, x, y))

    txt_nome = tk.Label(janela_criar, text="Nome *")
    txt_nome.place(x=0, y=0)

    entry_nome = tk.Entry(janela_criar, width=65)
    entry_nome.place(x=70, y=3)

    txt_descrição = tk.Label(janela_criar, text="Descrição")
    txt_descrição.place(x=0, y=30)

    entry_descrição = tk.Entry(janela_criar, width=65)
    entry_descrição.place(x=70, y=33)

    txt_data = tk.Label(janela_criar, text="Data")
    txt_data.place(x=0, y=65)

    var_dias = tk.IntVar(janela_criar)
    var_dias.set(lista_dias[0])

    menu_dia = tk.OptionMenu(janela_criar, var_dias, *lista_dias)
    menu_dia.place(x=70, y=60)

    var_meses = tk.IntVar(janela_criar)
    var_meses.set(lista_meses[0])

    menu_mes = tk.OptionMenu(janela_criar, var_meses, *lista_meses)
    menu_mes.place(x=130, y=60)

    var_ano = tk.IntVar(janela_criar)
    var_ano.set(lista_ano[0])

    menu_ano = tk.OptionMenu(janela_criar, var_ano, *lista_ano)
    menu_ano.place(x=190, y=60)

    txt_prioridade = tk.Label(janela_criar, text="Prioridade *")
    txt_prioridade.place(x=0, y=100)

    var_prioridade = tk.IntVar(janela_criar)
    var_prioridade.set(nvl_prioridade[0])

    menu_prioridade = tk.OptionMenu(janela_criar, var_prioridade, *nvl_prioridade)
    menu_prioridade.place(x=70, y=95)

    txt_aviso = tk.Label(janela_criar, text="* - Obrigatório")
    txt_aviso.place(x=5, y=130)

    botão_confirmar = tk.Button(janela_criar, text="Confirmar", command=lambda: [confirmar(), janela_criar.destroy(), tarefas(usuario_tarefa)])
    botão_confirmar.place(x=0, y=160)

    janela_criar.mainloop()


login()