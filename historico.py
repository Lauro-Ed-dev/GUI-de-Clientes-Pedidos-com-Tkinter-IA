import tkinter as tk
from tkinter import scrolledtext, messagebox
import os
from log_utils import LOG_FILE, limpar_log
from estilo import ThemeManager, TITLE_FONT, SMALL_FONT, BG, TX, HI

class Historico(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master, bg=BG())
        self.pack(fill="both", expand=True)
        self._criar_ui()
        self.carregar_historico()

    def _criar_ui(self):
        tk.Label(self, text="Histórico de Ações", font=TITLE_FONT, bg=BG(), fg=TX()).pack(pady=10)

        self.text = scrolledtext.ScrolledText(self, font=("Courier", 11), wrap=tk.NONE,
                                              bg=ThemeManager.get("TEXT_BG"),
                                              fg=TX(), insertbackground=TX())
        self.text.pack(fill="both", expand=True, padx=12, pady=8)

        btn_frame = tk.Frame(self, bg=BG())
        btn_frame.pack(pady=8)

        self.btn_limpar = tk.Button(btn_frame, text="Limpar Histórico", command=self.limpar_historico)
        ThemeManager.style_button(self.btn_limpar)
        self.btn_recarregar = tk.Button(btn_frame, text="Recarregar", command=self.carregar_historico)
        ThemeManager.style_button(self.btn_recarregar)
        self.btn_limpar.pack(side="left", padx=6)
        self.btn_recarregar.pack(side="left", padx=6)

        self.lbl_info = tk.Label(self, text="", font=SMALL_FONT, bg=BG(), fg=HI())
        self.lbl_info.pack(pady=4)

    def carregar_historico(self):
        self.text.delete("1.0", tk.END)
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                content = f.read()
                self.text.insert(tk.END, content if content else "Nenhum evento registrado.")
            self.lbl_info.config(text="Histórico carregado.")
        else:
            self.text.insert(tk.END, "Arquivo de histórico não encontrado.")
            self.lbl_info.config(text="Arquivo ausente.")

    def limpar_historico(self):
        if not messagebox.askyesno("Confirmação", "Limpar todo o histórico?"):
            return
        limpar_log()
        self.carregar_historico()
        self.lbl_info.config(text="Histórico limpo.")