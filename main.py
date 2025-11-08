import tkinter as tk
from tkinter import ttk, messagebox

from frame_client import FrameClientes
from frame_pedido import FramePedidos
from dashboard import Dashboard
from relatorios import Relatorios
from historico import Historico
from estilo import *

class AppPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("💼 Sistema de Clientes e Pedidos")
        self.geometry("1000x660")
        self.configure(bg=BG_COLOR)
        self.protocol("WM_DELETE_WINDOW", self.confirmar_saida)
        self.criar_interface()
        self.show_frame("boas_vindas")

    def criar_interface(self):
        self.menu_frame = tk.Frame(self, bg=MENU_COLOR, width=180)
        self.menu_frame.pack(side="left", fill="y")

        self.main_frame = tk.Frame(self, bg=BG_COLOR)
        self.main_frame.pack(side="right", fill="both", expand=True)

        btns_info = [
            ("👥 Clientes", lambda: self.show_frame("clientes")),
            ("🧾 Pedidos", lambda: self.show_frame("pedidos")),
            ("📊 Dashboard", lambda: self.show_frame("dashboard")),
            ("📈 Relatórios", lambda: self.show_frame("relatorios")),
            ("📝 Histórico", lambda: self.show_frame("historico")),
            ("❌ Sair", self.confirmar_saida),
        ]

        self.menu_btns = []
        for idx, (label, cmd) in enumerate(btns_info):
            btn = tk.Button(self.menu_frame, text=label, command=cmd)
            menu_btn_style(btn)
            btn.pack(fill="x", pady=(14 if idx==0 else 0, 6))
            self.menu_btns.append(btn)

    def show_frame(self, secao):
        for w in self.main_frame.winfo_children():
            w.destroy()
        if secao == "boas_vindas":
            self.frame_boas_vindas()
        elif secao == "clientes":
            FrameClientes(self.main_frame)
        elif secao == "pedidos":
            FramePedidos(self.main_frame)
        elif secao == "dashboard":
            Dashboard(self.main_frame)
        elif secao == "relatorios":
            Relatorios(self.main_frame)
        elif secao == "historico":
            Historico(self.main_frame)

    def frame_boas_vindas(self):
        frame = tk.Frame(self.main_frame, bg=BG_COLOR)
        frame.pack(expand=True)
        tk.Label(
            frame, text="Bem-vindo!", font=("Arial", 24, "bold"), bg=BG_COLOR, fg=TEXT_COLOR
        ).pack(pady=40)
        tk.Label(
            frame, text="Use o menu lateral para navegar pelas funções.",
            bg=BG_COLOR, fg=BTN_ACTIVE_COLOR, font=("Arial", 16)
        ).pack(pady=10)

    def confirmar_saida(self):
        if messagebox.askyesno("Sair", "Tem certeza que deseja fechar o sistema?"):
            self.destroy()

if __name__ == "__main__":
    app = AppPrincipal()
    app.mainloop()