import tkinter as tk
from tkinter import ttk, messagebox
from db import consultar, executar_comando
from form_pedido import abrir_form_pedido
from datetime import datetime
import traceback
from log_utils import registrar_acao  # NOVO

def registrar_erro(e):
    with open("erros.log", "a", encoding="utf-8") as f:
        f.write("\n" + "-" * 60 + "\n")
        f.write(traceback.format_exc())
    print("Erro registrado:", e)

class FramePedidos(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.pack(fill="both", expand=True)
        self.criar_widgets()
        self.carregar_pedidos()

    def criar_widgets(self):
        frame_busca = tk.Frame(self)
        frame_busca.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_busca, text="Buscar (cliente ou data):").pack(side="left", padx=(0, 5))
        self.entry_busca = tk.Entry(frame_busca, width=30)
        self.entry_busca.pack(side="left")
        tk.Button(frame_busca, text="🔍", command=self.buscar_pedidos).pack(side="left", padx=5)

        frame_tree = tk.Frame(self)
        frame_tree.pack(fill="both", expand=True, padx=10, pady=5)

        colunas = ("id", "cliente", "data", "total")
        self.tree = ttk.Treeview(frame_tree, columns=colunas, show="headings", height=12)
        self.tree.heading("id", text="ID")
        self.tree.heading("cliente", text="Cliente")
        self.tree.heading("data", text="Data")
        self.tree.heading("total", text="Total (R$)")
        self.tree.column("id", width=60, anchor="center")
        self.tree.column("cliente", width=200)
        self.tree.column("data", width=120, anchor="center")
        self.tree.column("total", width=100, anchor="e")
        self.tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(frame_tree, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        frame_botoes = tk.Frame(self)
        frame_botoes.pack(fill="x", pady=10)

        tk.Button(frame_botoes, text="Novo Pedido", width=15, command=self.novo_pedido).pack(side="left", padx=10)
        tk.Button(frame_botoes, text="Ver Itens", width=15, command=self.ver_itens).pack(side="left", padx=10)
        tk.Button(frame_botoes, text="Excluir", width=15, command=self.excluir_pedido).pack(side="left", padx=10)

    def carregar_pedidos(self, filtro=""):
        for i in self.tree.get_children():
            self.tree.delete(i)

        if filtro:
            sql = """
                SELECT p.id, c.nome, p.data, p.total
                FROM pedidos p
                JOIN clientes c ON c.id = p.cliente_id
                WHERE c.nome LIKE ? OR p.data LIKE ?
                ORDER BY p.data DESC
            """
            params = (f"%{filtro}%", f"%{filtro}%")
        else:
            sql = """
                SELECT p.id, c.nome, p.data, p.total
                FROM pedidos p
                JOIN clientes c ON c.id = p.cliente_id
                ORDER BY p.data DESC
            """
            params = ()

        try:
            pedidos = consultar(sql, params)
            for p in pedidos:
                self.tree.insert("", "end", values=(p[0], p[1], p[2], f"{p[3]:.2f}"))
        except Exception as e:
            registrar_erro(e)
            messagebox.showerror("Erro", "Falha ao carregar pedidos.")

    def buscar_pedidos(self):
        termo = self.entry_busca.get().strip()
        self.carregar_pedidos(termo)

    def novo_pedido(self):
        try:
            abrir_form_pedido(self.master)
            self.after(400, self.carregar_pedidos)
        except Exception as e:
            registrar_erro(e)
            messagebox.showerror("Erro", "Não foi possível abrir o formulário de pedido.")

    def ver_itens(self):
        selecionado = self.tree.focus()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione um pedido para visualizar os itens.")
            return

        valores = self.tree.item(selecionado, "values")
        pedido_id = valores[0]
        self.abrir_janela_itens(pedido_id, valores[1], valores[2])

    def abrir_janela_itens(self, pedido_id, cliente, data):
        itens = consultar(
            "SELECT produto, quantidade, preco_unit FROM itens_pedido WHERE pedido_id = ?",
            (pedido_id,)
        )

        janela = tk.Toplevel(self)
        janela.title(f"Itens do Pedido #{pedido_id} - {cliente}")
        janela.geometry("500x300")
        janela.grab_set()

        tk.Label(janela, text=f"Cliente: {cliente}", font=("Arial", 11, "bold")).pack(pady=5)
        tk.Label(janela, text=f"Data: {data}").pack(pady=5)

        cols = ("produto", "quantidade", "preco_unit", "subtotal")
        tree_itens = ttk.Treeview(janela, columns=cols, show="headings", height=10)
        for col in cols:
            tree_itens.heading(col, text=col.capitalize())
        tree_itens.column("produto", width=200)
        tree_itens.column("quantidade", width=80, anchor="center")
        tree_itens.column("preco_unit", width=80, anchor="e")
        tree_itens.column("subtotal", width=90, anchor="e")

        for item in itens:
            subtotal = float(item[1]) * float(item[2])
            tree_itens.insert("", "end", values=(item[0], item[1], f"{item[2]:.2f}", f"{subtotal:.2f}"))

        tree_itens.pack(fill="both", expand=True, padx=10, pady=10)

        ttk.Button(janela, text="Fechar", command=janela.destroy).pack(pady=10)

    def excluir_pedido(self):
        selecionado = self.tree.focus()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione um pedido para excluir.")
            return

        valores = self.tree.item(selecionado, "values")
        pedido_id, cliente, data = valores[0], valores[1], valores[2]

        if not messagebox.askyesno("Confirmação", f"Excluir o pedido #{pedido_id} de {cliente} ({data})?"):
            return

        try:
            executar_comando("DELETE FROM itens_pedido WHERE pedido_id = ?", (pedido_id,))
            executar_comando("DELETE FROM pedidos WHERE id = ?", (pedido_id,))
            registrar_acao("Excluir", "Pedido", f"ID: {pedido_id} Cliente: {cliente} Data: {data}")
            messagebox.showinfo("Sucesso", "Pedido excluído com sucesso.")
            self.carregar_pedidos()
        except Exception as e:
            registrar_erro(e)
            messagebox.showerror("Erro", "Falha ao excluir o pedido.")