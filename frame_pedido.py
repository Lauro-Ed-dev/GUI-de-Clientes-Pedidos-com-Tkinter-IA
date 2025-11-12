import tkinter as tk
from tkinter import ttk, messagebox
from db import consultar, executar_comando
from form_pedido import abrir_form_pedido
import traceback
from log_utils import registrar_acao
from estilo import ThemeManager, TITLE_FONT, SMALL_FONT, BG, TX, HI, TBG

def registrar_erro(e):
    with open("erros.log", "a", encoding="utf-8") as f:
        f.write("\n" + "-" * 60 + "\n")
        f.write(traceback.format_exc())
    print("Erro registrado:", e)

class FramePedidos(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, bg=BG(), **kwargs)
        self.pack(fill="both", expand=True)
        self._criar_widgets()
        self.carregar_pedidos()

    def _criar_widgets(self):
        top = tk.Frame(self, bg=BG())
        top.pack(fill="x", padx=10, pady=8)
        tk.Label(top, text="Pedidos", font=TITLE_FONT, bg=BG(), fg=TX()).pack(side="left")
        btn_novo = tk.Button(top, text="Novo Pedido", command=self.novo_pedido)
        ThemeManager.style_button(btn_novo)
        btn_novo.pack(side="right")

        busca = tk.Frame(self, bg=BG())
        busca.pack(fill="x", padx=10, pady=4)
        tk.Label(busca, text="Buscar (cliente ou data):", bg=BG(), fg=TX(), font=SMALL_FONT).pack(side="left", padx=(0,5))
        self.entry_busca = tk.Entry(busca, width=30)
        self.entry_busca.pack(side="left")
        btn_b = tk.Button(busca, text="🔍", command=self.buscar_pedidos)
        ThemeManager.style_button(btn_b)
        btn_b.pack(side="left", padx=6)

        tree_frame = tk.Frame(self, bg=BG())
        tree_frame.pack(fill="both", expand=True, padx=10, pady=6)
        cols = ("id", "cliente", "data", "total")
        self.tree = ttk.Treeview(tree_frame, columns=cols, show="headings", height=14)
        for c in cols:
            self.tree.heading(c, text=c.capitalize())
            self.tree.column(c, width=140 if c != "id" else 60, anchor="w")
        ThemeManager.style_treeview(self.tree)
        self.tree.pack(side="left", fill="both", expand=True)
        scroll = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scroll.set)
        scroll.pack(side="right", fill="y")

        btns = tk.Frame(self, bg=BG())
        btns.pack(fill="x", pady=10)
        for txt, cmd in [("Ver Itens", self.ver_itens), ("Excluir", self.excluir_pedido)]:
            b = tk.Button(btns, text=txt, command=cmd)
            ThemeManager.style_button(b)
            b.pack(side="left", padx=8)

        self.lbl_status = tk.Label(self, text="", bg=BG(), fg=HI(), font=SMALL_FONT)
        self.lbl_status.pack(pady=4)

    def carregar_pedidos(self, filtro=""):
        self.tree.delete(*self.tree.get_children())
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
            for i, p in enumerate(pedidos):
                self.tree.insert("", "end", values=(p[0], p[1], p[2], f"{p[3]:.2f}"),
                                 tags=("row", "odd" if i % 2 else "even"))
            self.tree.tag_configure("row", foreground=TX())
            self.tree.tag_configure("odd", background=TBG())
            self.tree.tag_configure("even", background=BG())
            self.lbl_status.config(text=f"{len(pedidos)} pedido(s).")
        except Exception as e:
            registrar_erro(e)
            self.lbl_status.config(text=f"Erro: {e}")

    def buscar_pedidos(self):
        termo = self.entry_busca.get().strip()
        self.carregar_pedidos(termo)

    def novo_pedido(self):
        try:
            abrir_form_pedido(self.master)
            self.after(400, self.carregar_pedidos)
        except Exception as e:
            registrar_erro(e)
            self.lbl_status.config(text=f"Erro ao abrir: {e}")

    def ver_itens(self):
        sel = self.tree.focus()
        if not sel:
            messagebox.showinfo("Atenção", "Selecione um pedido.")
            return
        valores = self.tree.item(sel, "values")
        pedido_id = valores[0]
        self._janela_itens(pedido_id, valores[1], valores[2])

    def _janela_itens(self, pedido_id, cliente, data):
        itens = consultar("SELECT produto, quantidade, preco_unit FROM itens_pedido WHERE pedido_id = ?", (pedido_id,))
        win = tk.Toplevel(self)
        win.title(f"Itens Pedido #{pedido_id}")
        win.configure(bg=BG())
        tk.Label(win, text=f"Cliente: {cliente}", font=("Arial", 12, "bold"), bg=BG(), fg=TX()).pack(pady=5)
        tk.Label(win, text=f"Data: {data}", bg=BG(), fg=TX()).pack(pady=5)

        cols = ("produto", "quantidade", "preco_unit", "subtotal")
        tree = ttk.Treeview(win, columns=cols, show="headings", height=12)
        for c in cols:
            tree.heading(c, text=c.capitalize())
            tree.column(c, width=150 if c != "produto" else 220)
        ThemeManager.style_treeview(tree)
        tree.pack(fill="both", expand=True, padx=10, pady=10)
        for item in itens:
            subtotal = float(item[1]) * float(item[2])
            tree.insert("", "end", values=(item[0], item[1], f"{item[2]:.2f}", f"{subtotal:.2f}"))

        btn_fechar = tk.Button(win, text="Fechar", command=win.destroy)
        ThemeManager.style_button(btn_fechar)
        btn_fechar.pack(pady=10)

    def excluir_pedido(self):
        sel = self.tree.focus()
        if not sel:
            messagebox.showinfo("Atenção", "Selecione um pedido.")
            return
        valores = self.tree.item(sel, "values")
        pedido_id, cliente, data = valores[0], valores[1], valores[2]
        if not messagebox.askyesno("Confirmação", f"Excluir pedido #{pedido_id}?"):
            return
        try:
            executar_comando("DELETE FROM itens_pedido WHERE pedido_id = ?", (pedido_id,))
            executar_comando("DELETE FROM pedidos WHERE id = ?", (pedido_id,))
            registrar_acao("Excluir", "Pedido", f"ID:{pedido_id} Cliente:{cliente} Data:{data}")
            self.carregar_pedidos()
        except Exception as e:
            registrar_erro(e)
            messagebox.showerror("Erro", f"Falha ao excluir: {e}")