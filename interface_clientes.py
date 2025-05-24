# interface_clientes.py
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox
from funcoes_clientes import (
    cadastrar_cliente,
    listar_clientes,
    consultar_cliente_por_nome,
    editar_cliente,
    excluir_cliente,
)

class TelaClientes(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)

        self.title("Clientes")
        self.geometry("700x550")  # aumento para melhor acomodar 2 linhas de botões
        self.resizable(False, False)

        self.label = ctk.CTkLabel(self, text="Gerenciar Clientes", font=("Arial", 16))
        self.label.pack(pady=10)

        self.frame_form = ctk.CTkFrame(self)
        self.frame_form.pack(pady=10, padx=10, fill="x")

        self.label_id = ctk.CTkLabel(self.frame_form, text="ID do Cliente:")
        self.label_id.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.entry_id = ctk.CTkEntry(self.frame_form)
        self.entry_id.grid(row=0, column=1, padx=5, pady=5)
        self.entry_id.configure(state="disabled")

        self.label_nome = ctk.CTkLabel(self.frame_form, text="Nome:")
        self.label_nome.grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.entry_nome = ctk.CTkEntry(self.frame_form, width=300)
        self.entry_nome.grid(row=1, column=1, padx=5, pady=5)

        self.label_cpf = ctk.CTkLabel(self.frame_form, text="CPF:")
        self.label_cpf.grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.entry_cpf = ctk.CTkEntry(self.frame_form, width=300)
        self.entry_cpf.grid(row=2, column=1, padx=5, pady=5)

        self.label_telefone = ctk.CTkLabel(self.frame_form, text="Telefone:")
        self.label_telefone.grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.entry_telefone = ctk.CTkEntry(self.frame_form, width=300)
        self.entry_telefone.grid(row=3, column=1, padx=5, pady=5)

        self.label_email = ctk.CTkLabel(self.frame_form, text="E-mail:")
        self.label_email.grid(row=4, column=0, sticky="w", padx=5, pady=5)
        self.entry_email = ctk.CTkEntry(self.frame_form, width=300)
        self.entry_email.grid(row=4, column=1, padx=5, pady=5)

        self.frame_botoes = ctk.CTkFrame(self)
        self.frame_botoes.pack(pady=10, padx=10)

        # Linha 0 dos botões
        self.btn_cadastrar = ctk.CTkButton(self.frame_botoes, text="Cadastrar", command=self.cadastrar)
        self.btn_cadastrar.grid(row=0, column=0, padx=5, pady=3)

        self.btn_consultar = ctk.CTkButton(self.frame_botoes, text="Consultar", command=self.consultar)
        self.btn_consultar.grid(row=0, column=1, padx=5, pady=3)

        self.btn_listar = ctk.CTkButton(self.frame_botoes, text="Listar", command=self.listar_clientes)
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

        self.tree = ttk.Treeview(self, columns=("ID", "Nome", "CPF", "Telefone", "Email"), show="headings")
        for col in ("ID", "Nome", "CPF", "Telefone", "Email"):
            self.tree.heading(col, text=col)
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Nome", width=150)
        self.tree.column("CPF", width=100)
        self.tree.column("Telefone", width=100)
        self.tree.column("Email", width=180)
        self.tree.pack(padx=10, pady=10, fill="both", expand=True)

        self.scrollbar_vertical = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=self.scrollbar_vertical.set)
        self.scrollbar_vertical.pack(side="right", fill="y")

        self.scrollbar_horizontal = ttk.Scrollbar(self, orient="horizontal", command=self.tree.xview)
        self.tree.configure(xscroll=self.scrollbar_horizontal.set)
        self.scrollbar_horizontal.pack(side="bottom", fill="x")

        self.listar_clientes()  # Já carrega a lista ao abrir

        # Vincular evento de seleção para preencher os campos ao clicar na tabela
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

    def cadastrar(self):
        nome = self.entry_nome.get().strip()
        cpf = self.entry_cpf.get().strip()
        telefone = self.entry_telefone.get().strip()
        email = self.entry_email.get().strip()

        if not nome or not cpf or not telefone or not email:
            messagebox.showwarning("Aviso", "Por favor, preencha todos os campos.")
            return

        sucesso, mensagem = cadastrar_cliente(nome, cpf, telefone, email)

        if sucesso:
            messagebox.showinfo("Sucesso", mensagem)
            self.limpar_campos()
            self.listar_clientes()
        else:
            messagebox.showwarning("Aviso", mensagem)

    def consultar(self):
        nome = self.entry_nome.get().strip()
        if not nome:
            messagebox.showwarning("Aviso", "Por favor, digite o nome para consultar.")
            return
        resultados = consultar_cliente_por_nome(nome)
        self.ocultar_tabela()
        if resultados:
            for cliente in resultados:
                self.tree.insert("", "end", values=cliente)
        else:
            messagebox.showinfo("Resultado", "Nenhum cliente encontrado com esse nome.")

    def listar_clientes(self):
        print(self)
        self.ocultar_tabela()
        for cliente in listar_clientes():
            self.tree.insert("", "end", values=cliente)

    def ocultar_tabela(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

    def editar(self):
        id_cliente = self.entry_id.get()
        if not id_cliente:
            messagebox.showwarning("Aviso", "Selecione um cliente para editar (clicando na tabela).")
            return
        nome = self.entry_nome.get().strip()
        cpf = self.entry_cpf.get().strip()
        telefone = self.entry_telefone.get().strip()
        email = self.entry_email.get().strip()

        if not nome or not cpf or not telefone or not email:
            messagebox.showwarning("Aviso", "Por favor, preencha todos os campos para editar.")
            return

        sucesso, mensagem = editar_cliente(id_cliente, nome, cpf, telefone, email)

        if sucesso:
            messagebox.showinfo("Sucesso", mensagem)
            self.limpar_campos()
            self.listar_clientes()
        else:
            messagebox.showwarning("Aviso", mensagem)

    def excluir(self):
        id_cliente = self.entry_id.get()
        if not id_cliente:
            messagebox.showwarning("Aviso", "Selecione um cliente para excluir (clicando na tabela).")
            return

        confirm = messagebox.askyesno("Confirmar Exclusão", "Tem certeza que deseja excluir o cliente selecionado?")
        if not confirm:
            return

        sucesso, mensagem = excluir_cliente(id_cliente)

        if sucesso:
            messagebox.showinfo("Sucesso", mensagem)
            self.limpar_campos()
            self.listar_clientes()
        else:
            messagebox.showwarning("Aviso", mensagem)

    def limpar_campos(self):
        self.entry_id.configure(state="normal")
        self.entry_id.delete(0, tk.END)
        self.entry_id.configure(state="disabled")
        self.entry_nome.delete(0, tk.END)
        self.entry_cpf.delete(0, tk.END)
        self.entry_telefone.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
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

            self.entry_nome.delete(0, tk.END)
            self.entry_nome.insert(0, valores[1])

            self.entry_cpf.delete(0, tk.END)
            self.entry_cpf.insert(0, valores[2])

            self.entry_telefone.delete(0, tk.END)
            self.entry_telefone.insert(0, valores[3])

            self.entry_email.delete(0, tk.END)
            self.entry_email.insert(0, valores[4])
