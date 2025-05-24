# interface_veiculos.py
import customtkinter as ctk
import tkinter as tk
from funcoes_veiculos import contar_veiculos_por_marca
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk, messagebox
from funcoes_veiculos import (
    cadastrar_veiculo,
    listar_veiculos,
    consultar_veiculo_por_modelo,
    editar_veiculo,
    excluir_veiculo,
)

class TelaVeiculos(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)

        self.title("Veículos")
        self.geometry("1000x700")
        self.resizable(False, False)

       
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        
        self.label = ctk.CTkLabel(self, text="Gerenciar Veículos", font=("Arial", 16))
        self.label.grid(row=0, column=0, pady=10, sticky="n")

       
        self.frame_superior = ctk.CTkFrame(self)
        self.frame_superior.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")
        self.frame_superior.grid_columnconfigure(0, weight=1)
        self.frame_superior.grid_columnconfigure(1, weight=1)
        self.frame_superior.grid_rowconfigure(0, weight=1)

        # Frame do formulário (esquerda)
        self.frame_form = ctk.CTkFrame(self.frame_superior)
        self.frame_form.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        # ID do veículo
        self.label_id = ctk.CTkLabel(self.frame_form, text="ID do Veículo:")
        self.label_id.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.entry_id = ctk.CTkEntry(self.frame_form)
        self.entry_id.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.entry_id.configure(state="disabled")

        # Modelo
        self.label_modelo = ctk.CTkLabel(self.frame_form, text="Modelo:")
        self.label_modelo.grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.entry_modelo = ctk.CTkEntry(self.frame_form)
        self.entry_modelo.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # Marca
        self.label_marca = ctk.CTkLabel(self.frame_form, text="Marca:")
        self.label_marca.grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.entry_marca = ctk.CTkEntry(self.frame_form)
        self.entry_marca.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        # Cor
        self.label_cor = ctk.CTkLabel(self.frame_form, text="Cor:")
        self.label_cor.grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.entry_cor = ctk.CTkEntry(self.frame_form)
        self.entry_cor.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        # Placa
        self.label_placa = ctk.CTkLabel(self.frame_form, text="Placa:")
        self.label_placa.grid(row=4, column=0, sticky="w", padx=5, pady=5)
        self.entry_placa = ctk.CTkEntry(self.frame_form)
        self.entry_placa.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

        # Tipo
        self.label_tipo = ctk.CTkLabel(self.frame_form, text="Tipo:")
        self.label_tipo.grid(row=5, column=0, sticky="w", padx=5, pady=5)
        self.combo_tipo = ttk.Combobox(self.frame_form, state="readonly", 
                                     values=["Sedan", "Hatch", "SUV", "Moto", "Van"])
        self.combo_tipo.grid(row=5, column=1, padx=5, pady=5, sticky="ew")
        self.combo_tipo.current(0)

        # Ano
        self.label_ano = ctk.CTkLabel(self.frame_form, text="Ano:")
        self.label_ano.grid(row=6, column=0, sticky="w", padx=5, pady=5)
        self.entry_ano = ctk.CTkEntry(self.frame_form)
        self.entry_ano.grid(row=6, column=1, padx=5, pady=5, sticky="ew")

        # Frame do gráfico (direita)
        self.frame_grafico = ctk.CTkFrame(self.frame_superior)
        self.frame_grafico.grid(row=0, column=1, padx=2, pady=2, sticky="nsew")
        self.criar_grafico()

        # Frame dos botões
        self.frame_botoes = ctk.CTkFrame(self)
        self.frame_botoes.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="ew")
        
        # Configurar o grid do frame_botoes para centralizar os botões
        self.frame_botoes.grid_columnconfigure(0, weight=1)
        self.frame_botoes.grid_columnconfigure(1, weight=1)
        self.frame_botoes.grid_columnconfigure(2, weight=1)
        self.frame_botoes.grid_columnconfigure(3, weight=1)
        self.frame_botoes.grid_columnconfigure(4, weight=1)  # Coluna extra para balancear


        # Botões linha 1
        self.btn_cadastrar = ctk.CTkButton(self.frame_botoes, text="Cadastrar", command=self.cadastrar)
        self.btn_cadastrar.grid(row=0, column=1, padx=5, pady=3)

        self.btn_consultar = ctk.CTkButton(self.frame_botoes, text="Consultar", command=self.consultar)
        self.btn_consultar.grid(row=0, column=2, padx=5, pady=3)

        self.btn_listar = ctk.CTkButton(self.frame_botoes, text="Listar", command=self.listar_veiculos)
        self.btn_listar.grid(row=0, column=3, padx=5, pady=3)

        self.btn_ocultar = ctk.CTkButton(self.frame_botoes, text="Ocultar", command=self.ocultar_tabela)
        self.btn_ocultar.grid(row=0, column=3, padx=5, pady=3)

        # Botões linha 2
        self.btn_editar = ctk.CTkButton(self.frame_botoes, text="Editar", command=self.editar)
        self.btn_editar.grid(row=1, column=1, padx=5, pady=3)

        self.btn_excluir = ctk.CTkButton(self.frame_botoes, text="Excluir", command=self.excluir)
        self.btn_excluir.grid(row=1, column=2, padx=5, pady=3)

        self.btn_limpar = ctk.CTkButton(self.frame_botoes, text="Limpar Campos", command=self.limpar_campos)
        self.btn_limpar.grid(row=1, column=3, padx=5, pady=3)

        self.btn_voltar = ctk.CTkButton(self.frame_botoes, text="Voltar", fg_color="red", command=self.destroy)
        self.btn_voltar.grid(row=1, column=3, padx=5, pady=3)

        # Frame da tabela
        self.frame_tabela = ctk.CTkFrame(self)
        self.frame_tabela.grid(row=3, column=0, padx=10, pady=(0, 10), sticky="nsew")
        self.frame_tabela.grid_rowconfigure(0, weight=1)
        self.frame_tabela.grid_columnconfigure(0, weight=1)

        # Treeview
        self.tree = ttk.Treeview(
            self.frame_tabela,
            columns=("ID", "Modelo", "Marca", "Cor", "Placa", "Tipo", "Ano"),
            show="headings"
        )
        self.tree.grid(row=0, column=0, sticky="nsew")

        # Configuração das colunas
        colunas = [
            ("ID", 50, "center"),
            ("Modelo", 150, "w"),
            ("Marca", 120, "w"),
            ("Cor", 100, "w"),
            ("Placa", 100, "w"),
            ("Tipo", 100, "w"),
            ("Ano", 80, "center")
        ]

        for col, width, anchor in colunas:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor=anchor)

        # Scrollbars
        self.scrollbar_vertical = ttk.Scrollbar(self.frame_tabela, orient="vertical", command=self.tree.yview)
        self.scrollbar_vertical.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=self.scrollbar_vertical.set)

        self.scrollbar_horizontal = ttk.Scrollbar(self.frame_tabela, orient="horizontal", command=self.tree.xview)
        self.scrollbar_horizontal.grid(row=1, column=0, sticky="ew")
        self.tree.configure(xscrollcommand=self.scrollbar_horizontal.set)

        # Eventos
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        # Carrega dados iniciais
        self.listar_veiculos()

    def criar_grafico(self):
        # Configura o estilo do matplotlib para combinar com o CustomTkinter
        plt.style.use('ggplot')  
        plt.rcParams['figure.facecolor'] = "#202020"  # Cor de fundo da figura
        
        plt.rcParams['axes.facecolor'] = "#252525"  # Cor de fundo dos eixos
        plt.rcParams['text.color'] = 'white'  # Cor do texto
        plt.rcParams['axes.labelcolor'] = 'white'  # Cor dos rótulos
        plt.rcParams['xtick.color'] = 'white'  # Cor dos ticks do eixo x
        plt.rcParams['ytick.color'] = 'white'  # Cor dos ticks do eixo y
    
        # Restante do método permanece igual...
        for widget in self.frame_grafico.winfo_children():
            widget.destroy()

        dados = contar_veiculos_por_marca()
    
        if not dados:
            label = ctk.CTkLabel(self.frame_grafico, text="Nenhum veículo cadastrado")
            label.pack(expand=True)
            return

        marcas = [item[0] for item in dados]
        quantidades = [item[1] for item in dados]

        fig, ax = plt.subplots(figsize=(5, 4.5))
        bars = ax.bar(marcas, quantidades, color='#1f6aa5')  # Azul do CustomTkinter
        ax.set_position([0.15, 0.2, 0.8, 0.7])
        plt.tight_layout(pad=3.0)
    
        # Configuração das cores do gráfico
        fig.patch.set_facecolor('#2b2b2b')  # Cor de fundo da figura
        ax.set_facecolor('#2b2b2b')  # Cor de fundo dos eixos
    
        # Adiciona os valores nas barras
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom', color='white')

        ax.set_title('Veículos por Marca', fontsize=10, color='white')
        ax.set_ylabel('Quantidade', fontsize=8, color='white')
        ax.tick_params(axis='x', rotation=45, labelsize=8, colors='white')
        ax.tick_params(axis='y', labelsize=8, colors='white')
        
    

        canvas = FigureCanvasTkAgg(fig, master=self.frame_grafico)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        """Cria o gráfico de barras com a distribuição de veículos por marca"""
        for widget in self.frame_grafico.winfo_children():
            widget.destroy()

        dados = contar_veiculos_por_marca()
        
        if not dados:
            label = ctk.CTkLabel(self.frame_grafico, text="Nenhum veículo cadastrado")
            label.pack(expand=True)
            return

        marcas = [item[0] for item in dados]
        quantidades = [item[1] for item in dados]

        fig, ax = plt.subplots(figsize=(5, 3.5))
        bars = ax.bar(marcas, quantidades, color='#1f6aa5')
        
        # Adiciona os valores nas barras
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}',
                    ha='center', va='bottom')

        ax.set_title('Veículos por Marca', fontsize=10)
        ax.set_ylabel('Quantidade', fontsize=8)
        ax.tick_params(axis='x', rotation=45, labelsize=8)
        ax.tick_params(axis='y', labelsize=8)
        
        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.frame_grafico)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def cadastrar(self):
        modelo = self.entry_modelo.get().strip()
        marca = self.entry_marca.get().strip()
        cor = self.entry_cor.get().strip()
        placa = self.entry_placa.get().strip()
        tipo = self.combo_tipo.get()
        ano = self.entry_ano.get().strip()

        if not modelo or not marca or not cor or not placa or not tipo or not ano:
            messagebox.showwarning("Aviso", "Por favor, preencha todos os campos.")
            return

        sucesso, mensagem = cadastrar_veiculo(modelo, marca, cor, placa, tipo, ano)

        if sucesso:
            messagebox.showinfo("Sucesso", mensagem)
            self.limpar_campos()
            self.listar_veiculos()
            self.criar_grafico()
        else:
            messagebox.showwarning("Aviso", mensagem)

    def consultar(self):
        modelo = self.entry_modelo.get().strip()
        if not modelo:
            messagebox.showwarning("Aviso", "Por favor, digite o modelo para consultar.")
            return
        
        self.ocultar_tabela()
        resultados = consultar_veiculo_por_modelo(modelo)
        
        if resultados:
            for veiculo in resultados:
                self.tree.insert("", "end", values=veiculo)
        else:
            messagebox.showinfo("Resultado", "Nenhum veículo encontrado com esse modelo.")

    def listar_veiculos(self):
        self.ocultar_tabela()
        for veiculo in listar_veiculos():
            self.tree.insert("", "end", values=veiculo)

    def ocultar_tabela(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

    def editar(self):
        id_veiculo = self.entry_id.get()
        if not id_veiculo:
            messagebox.showwarning("Aviso", "Selecione um veículo para editar.")
            return

        modelo = self.entry_modelo.get().strip()
        marca = self.entry_marca.get().strip()
        cor = self.entry_cor.get().strip()
        placa = self.entry_placa.get().strip()
        tipo = self.combo_tipo.get()
        ano = self.entry_ano.get().strip()

        if not modelo or not marca or not cor or not placa or not tipo or not ano:
            messagebox.showwarning("Aviso", "Por favor, preencha todos os campos.")
            return

        sucesso, mensagem = editar_veiculo(id_veiculo, modelo, marca, cor, placa, tipo, ano)

        if sucesso:
            messagebox.showinfo("Sucesso", mensagem)
            self.limpar_campos()
            self.listar_veiculos()
            self.criar_grafico()
        else:
            messagebox.showwarning("Aviso", mensagem)

    def excluir(self):
        id_veiculo = self.entry_id.get()
        if not id_veiculo:
            messagebox.showwarning("Aviso", "Selecione um veículo para excluir.")
            return

        confirm = messagebox.askyesno("Confirmar", "Tem certeza que deseja excluir este veículo?")
        if not confirm:
            return

        sucesso, mensagem = excluir_veiculo(id_veiculo)

        if sucesso:
            messagebox.showinfo("Sucesso", mensagem)
            self.limpar_campos()
            self.listar_veiculos()
            self.criar_grafico()
        else:
            messagebox.showwarning("Aviso", mensagem)

    def limpar_campos(self):
        self.entry_id.configure(state="normal")
        self.entry_id.delete(0, tk.END)
        self.entry_id.configure(state="disabled")
        self.entry_modelo.delete(0, tk.END)
        self.entry_marca.delete(0, tk.END)
        self.entry_cor.delete(0, tk.END)
        self.entry_placa.delete(0, tk.END)
        self.combo_tipo.current(0)
        self.entry_ano.delete(0, tk.END)

    def on_tree_select(self, event):
        selecionados = self.tree.selection()
        if selecionados:
            item = self.tree.item(selecionados[0])
            valores = item["values"]
            
            self.entry_id.configure(state="normal")
            self.entry_id.delete(0, tk.END)
            self.entry_id.insert(0, valores[0])
            self.entry_id.configure(state="disabled")

            self.entry_modelo.delete(0, tk.END)
            self.entry_modelo.insert(0, valores[1])

            self.entry_marca.delete(0, tk.END)
            self.entry_marca.insert(0, valores[2])

            self.entry_cor.delete(0, tk.END)
            self.entry_cor.insert(0, valores[3])

            self.entry_placa.delete(0, tk.END)
            self.entry_placa.insert(0, valores[4])

            self.combo_tipo.set(valores[5])

            self.entry_ano.delete(0, tk.END)
            self.entry_ano.insert(0, valores[6])