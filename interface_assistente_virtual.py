import customtkinter as ctk
import tkinter as tk
from google import genai
from google.genai import types
from config import config


class TelaAssistenteVirtual(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        
        

        self.title("Assistente Virtual")
        self.geometry("500x500")
        self.resizable(False, False)

        self.label = ctk.CTkLabel(self, text="Assistente Virtual", font=("Arial", 16))
        self.label.pack(pady=10)

        # Área de exibição do chat com scroll
        self.chat_frame = ctk.CTkScrollableFrame(self, width=460, height=350)
        self.chat_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # Frame para entrada e botão
        self.frame_input = ctk.CTkFrame(self)
        self.frame_input.pack(padx=10, pady=10, fill="x")

        self.entry_mensagem = ctk.CTkEntry(self.frame_input, width=350, placeholder_text="Digite sua mensagem...")
        self.entry_mensagem.pack(side="left", padx=(0, 5), pady=5)

        self.btn_enviar = ctk.CTkButton(self.frame_input, text="Enviar", command=self.enviar_mensagem)
        self.btn_enviar.pack(side="left")

        self.btn_voltar = ctk.CTkButton(self, text="Voltar", fg_color="red", command=self.destroy)
        self.btn_voltar.pack(pady=10)

    def enviar_mensagem(self):
        mensagem = self.entry_mensagem.get().strip()
        if mensagem:
            # Exibe a mensagem do usuário
            self.adicionar_mensagem("Você", mensagem)
            self.entry_mensagem.delete(0, tk.END)

            # Gera uma resposta do assistente
            resposta = self.gerar_resposta(mensagem)
            self.adicionar_mensagem("Assistente", resposta)

    def adicionar_mensagem(self, remetente, mensagem):
        if remetente == "Você":
            bg_color = "#0078D7"  # Azul
            anchor = "e"
            justify = "right"
        else:
            bg_color = "#FFA500"  # Laranja
            anchor = "w"
            justify = "left"

        # Criar um frame para alinhar o balão
        msg_frame = ctk.CTkFrame(self.chat_frame, fg_color="transparent")
        msg_frame.pack(fill="x", pady=5, padx=5)

        # Criar o balão sem width fixo, só com wraplength
        balao = ctk.CTkLabel(
            msg_frame,
            text=mensagem,
            fg_color=bg_color,
            text_color="white",
            corner_radius=10,
            anchor=anchor,
            justify=justify,
            wraplength=280,  # Define quebra automática de linha se for muito longo
            padx=10,
            pady=5
        )

        # Alinhamento à direita ou esquerda
        if remetente == "Você":
            balao.pack(anchor="e")
        else:
            balao.pack(anchor="w")

        # Atualiza o scroll para sempre mostrar a última mensagem
        self.chat_frame.update_idletasks()
        self.chat_frame._parent_canvas.yview_moveto(1)

    def gerar_resposta(self, mensagem_usuario):
        self.entry_mensagem.delete(0, tk.END)
        client = genai.Client(api_key="AIzaSyDv7Z-hKue-fjjdsjL8Qn_jKIUymJ96T9I")

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            config=types.GenerateContentConfig(system_instruction=config),
            contents=mensagem_usuario,
        )

        return response.text
        

        
