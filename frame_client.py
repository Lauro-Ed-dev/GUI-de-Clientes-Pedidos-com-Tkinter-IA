import tkinter as tk
from tkinter import ttk, messagebox
from db import consultar, executar_comando
from form_client import abrir_form_cliente
from log_utils import registrar_acao
from estilo import *

class FrameClientes(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, bg=BG_COLOR, **kwargs)
        self.pack(fill="both", expand=True)
        self.criar_widgets()
        self.carregar_clientes()

    def criar_widgets(self):
        frame_top = tk.Frame(self, bg=BG_COLOR)
        frame_top.pack(fill="x", padx=10, pady=8)
        tk.Label(frame_top, text="Clientes", font=TITLE_FONT, bg=BG_COLOR, fg=MENU_COLOR).pack(side="left")
        btn = tk.Button(frame_top, text="Novo Cliente", command=self.novo_cliente)
        btn_style(btn)
        btn.pack(side="right")

        frame_busca = tk.Frame(self, bg=BG_COLOR)
        frame_busca.pack(fill="x", padx=10, pady=2)
        tk.Label(frame_busca, text="Buscar:", font=SMALL_FONT, bg=BG_COLOR).pack(side="left", padx=(0, 5))
        self.entry_busca = tk.Entry(frame_busca, width=30)
        self.entry_busca.pack(side="left", padx=(0, 5))
        btn_b = tk.Button(frame_busca, text="🔍", command=self.buscar_clientes)
        btn_style(btn_b)
        btn_b.pack(side="left")

        frame_tree = tk.Frame(self, bg=BG_COLOR)
        frame_tree.pack(fill="both", expand=True, padx=10, pady=5)
        colunas = ("id", "nome", "email", "telefone")
        self.tree = ttk.Treeview(frame_tree, columns=colunas, show="headings", height=15)
        for c in colunas:
            self.tree.heading(c, text=c.capitalize())
            self.tree.column(c, width=120 if c!="id" else 50)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar = ttk.Scrollbar(frame_tree, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        frame_botoes = tk.Frame(self, bg=BG_COLOR)
        frame_botoes.pack(fill="x", pady=12)
        for t, cmd in [
            ("Editar", self.editar_cliente), 
            ("Excluir", self.excluir_cliente)
        ]:
            btn = tk.Button(frame_botoes, text=t, command=cmd)
            btn_style(btn)
            btn.pack(side="left", padx=10)

    def carregar_clientes(self, filtro=""):
        for item in self.tree.get_children():
            self.tree.delete(item)
        if filtro:
            sql = "SELECT id, nome, email, telefone FROM clientes WHERE nome LIKE ? OR email LIKE ? ORDER BY nome"
            params = (f"%{filtro}%", f"%{filtro}%")
        else:
            sql = "SELECT id, nome, email, telefone FROM clientes ORDER BY nome"
            params = ()
        clientes = consultar(sql, params)
        for c in clientes:
            self.tree.insert("", "end", values=c)

    def buscar_clientes(self):
        termo = self.entry_busca.get().strip()
        self.carregar_clientes(termo)

    def novo_cliente(self):
        abrir_form_cliente(self.master)
        self.after(300, self.carregar_clientes)

    def editar_cliente(self):
        selecionado = self.tree.focus()
        if not selecionado:
            messagebox.showinfo("Atenção", "Selecione um cliente para editar.")
            return
        valores = self.tree.item(selecionado, "values")
        cliente = {
            "id": valores[0],
            "nome": valores[1],
            "email": valores[2],
            "telefone": valores[3],
        }
        abrir_form_cliente(self.master, cliente)
        self.after(300, self.carregar_clientes)

    def excluir_cliente(self):
        selecionado = self.tree.focus()
        if not selecionado:
            messagebox.showinfo("Atenção", "Selecione um cliente para excluir.")
            return
        valores = self.tree.item(selecionado, "values")
        cliente_id = valores[0]
        if not messagebox.askyesno("Confirmação", f"Deseja excluir o cliente '{valores[1]}'?"):
            return
        sucesso = executar_comando("DELETE FROM clientes WHERE id = ?", (cliente_id,))
        if sucesso:
            registrar_acao("Excluir", "Cliente", f"ID: {cliente_id} Nome: {valores[1]}")
            self.carregar_clientes()