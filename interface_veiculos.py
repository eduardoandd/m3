# interface_veiculos.py
import customtkinter as ctk
import tkinter as tk
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
        self.geometry("750x600")  # tamanho maior para mais campos
        self.resizable(False, False)

        self.label = ctk.CTkLabel(self, text="Gerenciar Veículos", font=("Arial", 16))
        self.label.pack(pady=10)

        self.frame_form = ctk.CTkFrame(self)
        self.frame_form.pack(pady=10, padx=10, fill="x")

        # ID do veículo (desabilitado para edição)
        self.label_id = ctk.CTkLabel(self.frame_form, text="ID do Veículo:")
        self.label_id.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.entry_id = ctk.CTkEntry(self.frame_form)
        self.entry_id.grid(row=0, column=1, padx=5, pady=5)
        self.entry_id.configure(state="disabled")

        # Modelo
        self.label_modelo = ctk.CTkLabel(self.frame_form, text="Modelo:")
        self.label_modelo.grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.entry_modelo = ctk.CTkEntry(self.frame_form, width=300)
        self.entry_modelo.grid(row=1, column=1, padx=5, pady=5)

        # Marca
        self.label_marca = ctk.CTkLabel(self.frame_form, text="Marca:")
        self.label_marca.grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.entry_marca = ctk.CTkEntry(self.frame_form, width=300)
        self.entry_marca.grid(row=2, column=1, padx=5, pady=5)

        # Cor
        self.label_cor = ctk.CTkLabel(self.frame_form, text="Cor:")
        self.label_cor.grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.entry_cor = ctk.CTkEntry(self.frame_form, width=300)
        self.entry_cor.grid(row=3, column=1, padx=5, pady=5)

        # Placa
        self.label_placa = ctk.CTkLabel(self.frame_form, text="Placa:")
        self.label_placa.grid(row=4, column=0, sticky="w", padx=5, pady=5)
        self.entry_placa = ctk.CTkEntry(self.frame_form, width=300)
        self.entry_placa.grid(row=4, column=1, padx=5, pady=5)

        # Tipo - Combobox com opções
        self.label_tipo = ctk.CTkLabel(self.frame_form, text="Tipo:")
        self.label_tipo.grid(row=5, column=0, sticky="w", padx=5, pady=5)
        self.combo_tipo = ttk.Combobox(self.frame_form, state="readonly", values=["Sedan", "Hatch", "SUV", "Moto", "Van"])
        self.combo_tipo.grid(row=5, column=1, padx=5, pady=5)
        self.combo_tipo.current(0)  # seleciona a primeira opção por padrão

        # Ano
        self.label_ano = ctk.CTkLabel(self.frame_form, text="Ano:")
        self.label_ano.grid(row=6, column=0, sticky="w", padx=5, pady=5)
        self.entry_ano = ctk.CTkEntry(self.frame_form, width=300)
        self.entry_ano.grid(row=6, column=1, padx=5, pady=5)

        self.frame_botoes = ctk.CTkFrame(self)
        self.frame_botoes.pack(pady=10, padx=10)

        # Linha 0 dos botões
        self.btn_cadastrar = ctk.CTkButton(self.frame_botoes, text="Cadastrar", command=self.cadastrar)
        self.btn_cadastrar.grid(row=0, column=0, padx=5, pady=3)

        self.btn_consultar = ctk.CTkButton(self.frame_botoes, text="Consultar", command=self.consultar)
        self.btn_consultar.grid(row=0, column=1, padx=5, pady=3)

        self.btn_listar = ctk.CTkButton(self.frame_botoes, text="Listar", command=self.listar_veiculos)
        self.btn_listar.grid(row=0, column=2, padx=5, pady=3)

        self.btn_ocultar = ctk.CTkButton(self.frame_botoes, text="Ocultar", command=self.ocultar_tabela)
        self.btn_ocultar.grid(row=0, column=3, padx=5, pady=3)

        # Linha 1 dos botões
        self.btn_editar = ctk.CTkButton(self.frame_botoes, text="Editar", command=self.editar)
        self.btn_editar.grid(row=1, column=0, padx=5, pady=3)

        self.btn_excluir = ctk.CTkButton(self.frame_botoes, text="Excluir", command=self.excluir)
        self.btn_excluir.grid(row=1, column=1, padx=5, pady=3)

        self.btn_limpar = ctk.CTkButton(self.frame_botoes, text="Limpar Campos", command=self.limpar_campos)
        self.btn_limpar.grid(row=1, column=2, padx=5, pady=3)

        self.btn_voltar = ctk.CTkButton(self.frame_botoes, text="Voltar", fg_color="red", command=self.destroy)
        self.btn_voltar.grid(row=1, column=3, padx=5, pady=3)

        # Treeview para listar os veículos
        self.tree = ttk.Treeview(
            self,
            columns=("ID", "Modelo", "Marca", "Cor", "Placa", "Tipo", "Ano"),
            show="headings"
        )
        for col in ("ID", "Modelo", "Marca", "Cor", "Placa", "Tipo", "Ano"):
            self.tree.heading(col, text=col)
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Modelo", width=150)
        self.tree.column("Marca", width=120)
        self.tree.column("Cor", width=100)
        self.tree.column("Placa", width=100)
        self.tree.column("Tipo", width=100)
        self.tree.column("Ano", width=80, anchor="center")
        self.tree.pack(padx=10, pady=10, fill="both", expand=True)

        # Scrollbars verticais e horizontais para a treeview
        self.scrollbar_vertical = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=self.scrollbar_vertical.set)
        self.scrollbar_vertical.pack(side="right", fill="y")

        self.scrollbar_horizontal = ttk.Scrollbar(self, orient="horizontal", command=self.tree.xview)
        self.tree.configure(xscroll=self.scrollbar_horizontal.set)
        self.scrollbar_horizontal.pack(side="bottom", fill="x")

        self.listar_veiculos()  # Carrega a lista ao abrir

        # Evento para preencher os campos ao clicar na tabela
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

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
        else:
            messagebox.showwarning("Aviso", mensagem)

    def consultar(self):
        modelo = self.entry_modelo.get().strip()
        if not modelo:
            messagebox.showwarning("Aviso", "Por favor, digite o modelo para consultar.")
            return
        resultados = consultar_veiculo_por_modelo(modelo)
        self.ocultar_tabela()
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
            messagebox.showwarning("Aviso", "Selecione um veículo para editar (clicando na tabela).")
            return
        modelo = self.entry_modelo.get().strip()
        marca = self.entry_marca.get().strip()
        cor = self.entry_cor.get().strip()
        placa = self.entry_placa.get().strip()
        tipo = self.combo_tipo.get()
        ano = self.entry_ano.get().strip()

        if not modelo or not marca or not cor or not placa or not tipo or not ano:
            messagebox.showwarning("Aviso", "Por favor, preencha todos os campos para editar.")
            return

        sucesso, mensagem = editar_veiculo(id_veiculo, modelo, marca, cor, placa, tipo, ano)

        if sucesso:
            messagebox.showinfo("Sucesso", mensagem)
            self.limpar_campos()
            self.listar_veiculos()
        else:
            messagebox.showwarning("Aviso", mensagem)

    def excluir(self):
        id_veiculo = self.entry_id.get()
        if not id_veiculo:
            messagebox.showwarning("Aviso", "Selecione um veículo para excluir (clicando na tabela).")
            return

        confirm = messagebox.askyesno("Confirmar Exclusão", "Tem certeza que deseja excluir o veículo selecionado?")
        if not confirm:
            return

        sucesso, mensagem = excluir_veiculo(id_veiculo)

        if sucesso:
            messagebox.showinfo("Sucesso", mensagem)
            self.limpar_campos()
            self.listar_veiculos()
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
        self.ocultar_tabela()

    def on_tree_select(self, event):
        selecionados = self.tree.selection()
        if selecionados:
            item = self.tree.item(selecionados[0])
            valores = item["values"]
            # Preenche os campos com os dados selecionados
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
