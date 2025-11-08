import tkinter as tk
from tkinter import messagebox, scrolledtext
import os
from log_utils import LOG_FILE, limpar_log

class Historico(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Histórico de Ações")
        self.geometry("600x400")
        self.resizable(False, False)

        self.text = scrolledtext.ScrolledText(self, font=("Courier", 11), wrap=tk.NONE)
        self.text.pack(fill="both", expand=True, padx=8, pady=8)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=8)
        btn_limpar = tk.Button(btn_frame, text="Limpar Histórico", command=self.limpar_historico)
        btn_limpar.pack()

        self.carregar_historico()

    def carregar_historico(self):
        self.text.delete(1.0, tk.END)
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                conteudo = f.read()
                self.text.insert(tk.END, conteudo)
        else:
            self.text.insert(tk.END, "Nenhum evento registrado ainda.")

    def limpar_historico(self):
        if messagebox.askyesno("Limpar Histórico", "Confirma excluir todo o histórico?"):
            limpar_log()
            self.carregar_historico()
            messagebox.showinfo("Histórico", "Histórico limpo com sucesso!")