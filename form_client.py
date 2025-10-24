import re
import tkinter as tk
from tkinter import messagebox
from db import executar_comando

# --------------------------------------------------------
# Validações
# --------------------------------------------------------
def validar_dados(nome, email, telefone):
    """Valida os campos do formulário."""
    if not nome.strip():
        messagebox.showerror("Erro de validação", "O campo Nome é obrigatório.")
        return False

    if email and not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
        messagebox.showerror("Erro de validação", "E-mail inválido.")
        return False

    if telefone and not re.match(r"^\d{8,15}$", telefone):
        messagebox.showerror("Erro de validação", "Telefone deve conter entre 8 e 15 dígitos numéricos.")
        return False

    return True


# --------------------------------------------------------
# Função callback de salvar
# --------------------------------------------------------
def salvar_cliente(entry_nome, entry_email, entry_telefone, janela, cliente_id=None):
    """Callback para salvar ou atualizar cliente."""
    nome = entry_nome.get().strip()
    email = entry_email.get().strip()
    telefone = entry_telefone.get().strip()

    if not validar_dados(nome, email, telefone):
        return

    if cliente_id:  # Modo edição
        sql = "UPDATE clientes SET nome = ?, email = ?, telefone = ? WHERE id = ?"
        params = (nome, email, telefone, cliente_id)
    else:  # Novo cadastro
        sql = "INSERT INTO clientes (nome, email, telefone) VALUES (?, ?, ?)"
        params = (nome, email, telefone)

    sucesso = executar_comando(sql, params)

    if sucesso:
        messagebox.showinfo("Sucesso", "Cliente salvo com sucesso!")
        janela.destroy()
    else:
        messagebox.showerror("Erro", "Não foi possível salvar o cliente.")


# --------------------------------------------------------
# Função callback de cancelar
# --------------------------------------------------------
def cancelar(janela):
    """Fecha a janela sem salvar."""
    if messagebox.askyesno("Cancelar", "Deseja realmente cancelar?"):
        janela.destroy()


# --------------------------------------------------------
# Formulário Tkinter
# --------------------------------------------------------
def abrir_form_cliente(root, cliente=None):
    """
    Abre uma janela Toplevel para cadastrar/editar cliente.
    cliente: dicionário opcional com dados para edição (id, nome, email, telefone)
    """
    janela = tk.Toplevel(root)
    janela.title("Cadastro de Cliente")
    janela.geometry("350x250")
    janela.resizable(False, False)
    janela.grab_set()  # Bloqueia interação com janela principal

    # Labels e entradas
    tk.Label(janela, text="Nome:").pack(anchor="w", padx=20, pady=(15, 0))
    entry_nome = tk.Entry(janela, width=40)
    entry_nome.pack(padx=20, pady=5)

    tk.Label(janela, text="E-mail:").pack(anchor="w", padx=20, pady=(10, 0))
    entry_email = tk.Entry(janela, width=40)
    entry_email.pack(padx=20, pady=5)

    tk.Label(janela, text="Telefone:").pack(anchor="w", padx=20, pady=(10, 0))
    entry_telefone = tk.Entry(janela, width=40)
    entry_telefone.pack(padx=20, pady=5)

    # Se for modo edição, preencher os campos
    cliente_id = None
    if cliente:
        cliente_id = cliente.get("id")
        entry_nome.insert(0, cliente.get("nome", ""))
        entry_email.insert(0, cliente.get("email", ""))
        entry_telefone.insert(0, cliente.get("telefone", ""))

    # Botões
    frame_botoes = tk.Frame(janela)
    frame_botoes.pack(pady=20)

    btn_salvar = tk.Button(
        frame_botoes,
        text="Salvar",
        width=10,
        command=lambda: salvar_cliente(entry_nome, entry_email, entry_telefone, janela, cliente_id)
    )
    btn_salvar.pack(side="left", padx=10)

    btn_cancelar = tk.Button(
        frame_botoes,
        text="Cancelar",
        width=10,
        command=lambda: cancelar(janela)
    )
    btn_cancelar.pack(side="left", padx=10)

    janela.mainloop()
