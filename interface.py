# interface.py
import customtkinter as ctk
from tkinter import messagebox
from interface_clientes import TelaClientes
from interface_veiculos import TelaVeiculos
from interface_locacao import TelaLocacao  # Importar a nova tela de Locação
from interface_assistente_virtual import TelaAssistenteVirtual

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class MenuPrincipal(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Locadora de Veículos - Menu Principal")
        self.geometry("400x300")
        self.resizable(False, False)

        self.label = ctk.CTkLabel(self, text="Sistema Locadora de Veículos", font=("Arial", 18))
        self.label.pack(pady=20)

        self.btn_clientes = ctk.CTkButton(self, text="Clientes", command=self.abrir_clientes)
        self.btn_clientes.pack(pady=8)

        self.btn_veiculos = ctk.CTkButton(self, text="Veículos", command=self.abrir_veiculos)
        self.btn_veiculos.pack(pady=8)

        self.btn_locacao = ctk.CTkButton(self, text="Locação", command=self.abrir_locacao)
        self.btn_locacao.pack(pady=8)
        
        self.btn_locacao = ctk.CTkButton(self, text="Assistente virtual", command=self.abrir_assistente_virtual)
        self.btn_locacao.pack(pady=8)

        self.btn_sair = ctk.CTkButton(self, text="Sair", fg_color="red", command=self.sair)
        self.btn_sair.pack(pady=8)

        # Variáveis para controlar janelas abertas
        self.tela_clientes = None
        self.tela_veiculos = None
        self.tela_locacao = None 
        self.tela_assistente_virtual = None 

    def abrir_clientes(self):
        if self.tela_clientes is None or not self.tela_clientes.winfo_exists():
            self.tela_clientes = TelaClientes(self)
            self.tela_clientes.grab_set()
        else:
            self.tela_clientes.focus()

    def abrir_veiculos(self):
        if self.tela_veiculos is None or not self.tela_veiculos.winfo_exists():
            self.tela_veiculos = TelaVeiculos(self)
            self.tela_veiculos.grab_set()
        else:
            self.tela_veiculos.focus()

    def abrir_locacao(self):
        if self.tela_locacao is None or not self.tela_locacao.winfo_exists():
            self.tela_locacao = TelaLocacao(self)
            self.tela_locacao.grab_set()
        else:
            self.tela_locacao.focus()
            
    def abrir_assistente_virtual(self):
        if self.tela_assistente_virtual is None  or not self.tela_assistente_virtual.winfo_exists():
            self.tela_assistente_virtual = TelaAssistenteVirtual(self)
            # self.tela_assistente_virtual.grab_set()
        else:
            self.tela_assistente_virtual.focus()

    def sair(self):
        self.destroy()
