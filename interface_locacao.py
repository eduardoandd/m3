import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from funcoes_locacao import (
    cadastrar_locacao,
    listar_locacoes,
    consultar_locacao_por_cliente,
    editar_locacao,
    atualizar_status_locacao
)
from funcoes_clientes import listar_clientes
from funcoes_veiculos import listar_veiculos

class TelaLocacao(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)

        self.title("Locações")
        self.geometry("800x620")
        self.resizable(False, False)

        self.label = ctk.CTkLabel(self, text="Gerenciar Locações", font=("Arial", 16))
        self.label.pack(pady=10)

        self.frame_form = ctk.CTkFrame(self)
        self.frame_form.pack(pady=10, padx=10, fill="x")

        self.label_id = ctk.CTkLabel(self.frame_form, text="ID da Locação:")
        self.label_id.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.entry_id = ctk.CTkEntry(self.frame_form)
        self.entry_id.grid(row=0, column=1, padx=5, pady=5)
        self.entry_id.configure(state="disabled")

        # ---------- CLIENTE ----------
        self.label_cliente = ctk.CTkLabel(self.frame_form, text="Cliente:")
        self.label_cliente.grid(row=1, column=0, sticky="w", padx=5, pady=5)

        clientes_raw = listar_clientes()
        self.cliente_map = {nome: id_ for id_, nome, *_ in clientes_raw}
        self.clientes = list(self.cliente_map.keys())

        self.combo_cliente = ttk.Combobox(self.frame_form, values=self.clientes, state="readonly", width=47)
        self.combo_cliente.grid(row=1, column=1, padx=5, pady=5)

        # ---------- VEICULO ----------
        self.label_veiculo = ctk.CTkLabel(self.frame_form, text="Veículo:")
        self.label_veiculo.grid(row=2, column=0, sticky="w", padx=5, pady=5)

        veiculos_raw = listar_veiculos()
        self.veiculo_map = {modelo: id_ for id_, modelo, *_ in veiculos_raw}
        self.veiculos = list(self.veiculo_map.keys())

        self.combo_veiculo = ttk.Combobox(self.frame_form, values=self.veiculos, state="readonly", width=47)
        self.combo_veiculo.grid(row=2, column=1, padx=5, pady=5)

        # ---------- DEMAIS CAMPOS ----------
        self.label_retirada = ctk.CTkLabel(self.frame_form, text="Data Retirada (DD/MM/AAAA):")
        self.label_retirada.grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.entry_retirada = ctk.CTkEntry(self.frame_form, width=300)
        self.entry_retirada.grid(row=3, column=1, padx=5, pady=5)

        self.label_devolucao = ctk.CTkLabel(self.frame_form, text="Data Devolução (DD/MM/AAAA):")
        self.label_devolucao.grid(row=4, column=0, sticky="w", padx=5, pady=5)
        self.entry_devolucao = ctk.CTkEntry(self.frame_form, width=300)
        self.entry_devolucao.grid(row=4, column=1, padx=5, pady=5)

        self.label_valor = ctk.CTkLabel(self.frame_form, text="Valor (R$):")
        self.label_valor.grid(row=5, column=0, sticky="w", padx=5, pady=5)
        self.entry_valor = ctk.CTkEntry(self.frame_form, width=300)
        self.entry_valor.grid(row=5, column=1, padx=5, pady=5)

        self.label_status = ctk.CTkLabel(self.frame_form, text="Status:")
        self.label_status.grid(row=6, column=0, sticky="w", padx=5, pady=5)
        self.combo_status = ttk.Combobox(self.frame_form, state="readonly",
                                         values=["Pendente", "Ativa", "Concluída", "Cancelada"])
        self.combo_status.grid(row=6, column=1, padx=5, pady=5)
        self.combo_status.current(0)

        # ---------- BOTÕES ----------
        self.frame_botoes = ctk.CTkFrame(self)
        self.frame_botoes.pack(pady=10, padx=10)

        self.btn_cadastrar = ctk.CTkButton(self.frame_botoes, text="Cadastrar", command=self.cadastrar)
        self.btn_cadastrar.grid(row=0, column=0, padx=5, pady=3)

        self.btn_consultar = ctk.CTkButton(self.frame_botoes, text="Consultar", command=self.consultar)
        self.btn_consultar.grid(row=0, column=1, padx=5, pady=3)

        self.btn_listar = ctk.CTkButton(self.frame_botoes, text="Listar", command=self.listar)
        self.btn_listar.grid(row=0, column=2, padx=5, pady=3)

        self.btn_ocultar = ctk.CTkButton(self.frame_botoes, text="Ocultar", command=self.ocultar_tabela)
        self.btn_ocultar.grid(row=0, column=3, padx=5, pady=3)

        self.btn_editar = ctk.CTkButton(self.frame_botoes, text="Editar Dados", command=self.editar)
        self.btn_editar.grid(row=1, column=0, padx=5, pady=3)

        self.btn_status = ctk.CTkButton(self.frame_botoes, text="Atualizar Status", command=self.atualizar_status)
        self.btn_status.grid(row=1, column=1, padx=5, pady=3)

        self.btn_limpar = ctk.CTkButton(self.frame_botoes, text="Limpar Campos", command=self.limpar_campos)
        self.btn_limpar.grid(row=1, column=2, padx=5, pady=3)

        self.btn_voltar = ctk.CTkButton(self.frame_botoes, text="Voltar", fg_color="red", command=self.destroy)
        self.btn_voltar.grid(row=1, column=3, padx=5, pady=3)

        # ---------- TREEVIEW ----------
        self.tree = ttk.Treeview(self, columns=("ID", "Cliente", "Veículo", "Retirada", "Devolução", "Valor", "Status"), show="headings")
        for col in ("ID", "Cliente", "Veículo", "Retirada", "Devolução", "Valor", "Status"):
            self.tree.heading(col, text=col)
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Cliente", width=150)
        self.tree.column("Veículo", width=150)
        self.tree.column("Retirada", width=100)
        self.tree.column("Devolução", width=100)
        self.tree.column("Valor", width=80, anchor="center")
        self.tree.column("Status", width=100, anchor="center")
        self.tree.pack(padx=10, pady=10, fill="both", expand=True)

        self.scroll_y = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=self.scroll_y.set)
        self.scroll_y.pack(side="right", fill="y")

        self.scroll_x = ttk.Scrollbar(self, orient="horizontal", command=self.tree.xview)
        self.tree.configure(xscroll=self.scroll_x.set)
        self.scroll_x.pack(side="bottom", fill="x")

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        self.listar()

    def validar_datas(self, *datas):
        for data in datas:
            try:
                datetime.strptime(data, "%d/%m/%Y")
            except ValueError:
                return False
        return True

    def cadastrar(self):
        nome_cliente = self.combo_cliente.get().strip()
        id_cliente = self.cliente_map.get(nome_cliente)

        modelo_veiculo = self.combo_veiculo.get().strip()
        id_veiculo = self.veiculo_map.get(modelo_veiculo)

        retirada = self.entry_retirada.get().strip()
        devolucao = self.entry_devolucao.get().strip()
        valor = self.entry_valor.get().strip()
        status = self.combo_status.get()

        if not id_cliente or not id_veiculo or not retirada or not devolucao or not valor:
            messagebox.showwarning("Aviso", "Preencha todos os campos.")
            return

        if not self.validar_datas(retirada, devolucao):
            messagebox.showwarning("Erro", "Insira datas válidas no formato DD/MM/AAAA.")
            return

        try:
            valor = float(valor.replace(",", "."))
        except ValueError:
            messagebox.showwarning("Erro", "O campo Valor deve ser numérico.")
            return

        sucesso, msg = cadastrar_locacao(id_cliente, id_veiculo, retirada, devolucao, valor, status)
        if sucesso:
            messagebox.showinfo("Sucesso", msg)
            self.limpar_campos()
            self.listar()
        else:
            messagebox.showwarning("Erro", msg)

    def consultar(self):
        nome_cliente = self.combo_cliente.get().strip()
        if not nome_cliente:
            messagebox.showwarning("Aviso", "Selecione o cliente para consultar.")
            return
        self.ocultar_tabela()
        resultados = consultar_locacao_por_cliente(nome_cliente)
        if resultados:
            for loc in resultados:
                self.tree.insert("", "end", values=loc)
        else:
            messagebox.showinfo("Resultado", "Nenhuma locação encontrada.")

    def listar(self):
        self.ocultar_tabela()
        for loc in listar_locacoes():
            self.tree.insert("", "end", values=loc)

    def ocultar_tabela(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

    def editar(self):
        id_loc = self.entry_id.get()
        if not id_loc:
            messagebox.showwarning("Aviso", "Selecione uma locação para editar.")
            return

        nome_cliente = self.combo_cliente.get().strip()
        id_cliente = self.cliente_map.get(nome_cliente)

        modelo_veiculo = self.combo_veiculo.get().strip()
        id_veiculo = self.veiculo_map.get(modelo_veiculo)

        retirada = self.entry_retirada.get().strip()
        devolucao = self.entry_devolucao.get().strip()
        valor = self.entry_valor.get().strip()
        status = self.combo_status.get()

        if not id_cliente or not id_veiculo or not retirada or not devolucao or not valor:
            messagebox.showwarning("Aviso", "Preencha todos os campos.")
            return

        if not self.validar_datas(retirada, devolucao):
            messagebox.showwarning("Erro", "Insira datas válidas no formato DD/MM/AAAA.")
            return

        try:
            valor = float(valor.replace(",", "."))
        except ValueError:
            messagebox.showwarning("Erro", "O campo Valor deve ser numérico.")
            return

        sucesso, msg = editar_locacao(id_loc, id_cliente, id_veiculo, retirada, devolucao, valor, status)
        if sucesso:
            messagebox.showinfo("Sucesso", msg)
            self.limpar_campos()
            self.listar()
        else:
            messagebox.showwarning("Erro", msg)

    def atualizar_status(self):
        id_loc = self.entry_id.get()
        status = self.combo_status.get()
        if not id_loc:
            messagebox.showwarning("Aviso", "Selecione uma locação na tabela.")
            return

        sucesso, msg = atualizar_status_locacao(id_loc, status)
        if sucesso:
            messagebox.showinfo("Sucesso", msg)
            self.limpar_campos()
            self.listar()
        else:
            messagebox.showwarning("Erro", msg)

    def limpar_campos(self):
        self.entry_id.configure(state="normal")
        self.entry_id.delete(0, tk.END)
        self.entry_id.configure(state="disabled")
        self.combo_cliente.set("")
        self.combo_veiculo.set("")
        self.entry_retirada.delete(0, tk.END)
        self.entry_devolucao.delete(0, tk.END)
        self.entry_valor.delete(0, tk.END)
        self.combo_status.current(0)
        self.ocultar_tabela()

    def on_tree_select(self, event):
        selecionado = self.tree.selection()
        if selecionado:
            dados = self.tree.item(selecionado[0])["values"]
            self.entry_id.configure(state="normal")
            self.entry_id.delete(0, tk.END)
            self.entry_id.insert(0, dados[0])
            self.entry_id.configure(state="disabled")

            # Preencher os comboboxes com base no nome/modelo
            self.combo_cliente.set(dados[1])
            self.combo_veiculo.set(dados[2])

            self.entry_retirada.delete(0, tk.END)
            self.entry_retirada.insert(0, dados[3])

            self.entry_devolucao.delete(0, tk.END)
            self.entry_devolucao.insert(0, dados[4])

            self.entry_valor.delete(0, tk.END)
            self.entry_valor.insert(0, str(dados[5]))

            self.combo_status.set(dados[6])
