import tkinter as tk
from tkinter import ttk, messagebox
from db import consultar, executar_comando
from form_client import abrir_form_cliente

# --------------------------------------------------------
# Classe do Frame de Listagem de Clientes
# --------------------------------------------------------
class FrameClientes(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.pack(fill="both", expand=True)
        self.criar_widgets()
        self.carregar_clientes()

    # ----------------------------------------------------
    # Widgets da interface
    # ----------------------------------------------------
    def criar_widgets(self):
        # Frame superior de busca
        frame_busca = tk.Frame(self)
        frame_busca.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_busca, text="Buscar:").pack(side="left", padx=(0, 5))
        self.entry_busca = tk.Entry(frame_busca, width=30)
        self.entry_busca.pack(side="left", padx=(0, 5))
        tk.Button(frame_busca, text="🔍", command=self.buscar_clientes).pack(side="left")

        # Frame para Treeview
        frame_tree = tk.Frame(self)
        frame_tree.pack(fill="both", expand=True, padx=10, pady=5)

        colunas = ("id", "nome", "email", "telefone")
        self.tree = ttk.Treeview(frame_tree, columns=colunas, show="headings", height=10)
        self.tree.heading("id", text="ID")
        self.tree.heading("nome", text="Nome")
        self.tree.heading("email", text="E-mail")
        self.tree.heading("telefone", text="Telefone")
        self.tree.column("id", width=50, anchor="center")
        self.tree.column("nome", width=150)
        self.tree.column("email", width=180)
        self.tree.column("telefone", width=100, anchor="center")
        self.tree.pack(side="left", fill="both", expand=True)

        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_tree, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Frame inferior de botões
        frame_botoes = tk.Frame(self)
        frame_botoes.pack(fill="x", pady=10)

        tk.Button(frame_botoes, text="Novo", width=10, command=self.novo_cliente).pack(side="left", padx=10)
        tk.Button(frame_botoes, text="Editar", width=10, command=self.editar_cliente).pack(side="left", padx=10)
        tk.Button(frame_botoes, text="Excluir", width=10, command=self.excluir_cliente).pack(side="left", padx=10)

    # ----------------------------------------------------
    # Carregar e exibir lista de clientes
    # ----------------------------------------------------
    def carregar_clientes(self, filtro=""):
        """Carrega os clientes no Treeview."""
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

    # ----------------------------------------------------
    # Ações de CRUD
    # ----------------------------------------------------
    def buscar_clientes(self):
        """Busca clientes pelo termo informado."""
        termo = self.entry_busca.get().strip()
        self.carregar_clientes(termo)

    def novo_cliente(self):
        """Abre o formulário para cadastrar novo cliente."""
        abrir_form_cliente(self.master)
        self.after(300, self.carregar_clientes)  # Recarrega após fechar o form

    def editar_cliente(self):
        """Abre o formulário para editar cliente selecionado."""
        selecionado = self.tree.focus()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione um cliente para editar.")
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
        """Exclui o cliente selecionado após confirmação."""
        selecionado = self.tree.focus()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione um cliente para excluir.")
            return

        valores = self.tree.item(selecionado, "values")
        cliente_id = valores[0]

        if not messagebox.askyesno("Confirmação", f"Deseja excluir o cliente '{valores[1]}'?"):
            return

        sucesso = executar_comando("DELETE FROM clientes WHERE id = ?", (cliente_id,))
        if sucesso:
            messagebox.showinfo("Sucesso", "Cliente excluído com sucesso!")
            self.carregar_clientes()
        else:
            messagebox.showerror("Erro", "Não foi possível excluir o cliente.")
