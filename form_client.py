import re
import tkinter as tk
from tkinter import messagebox
from db import executar_comando
from log_utils import registrar_acao
from estilo import ThemeManager, BG, TX, HI

def validar_dados(nome, email, telefone):
    if not nome.strip():
        messagebox.showerror("Validação", "Nome é obrigatório.")
        return False
    if email and not re.match(r"^[\\w\\.-]+@[\\w\\.-]+\\.\\w+$", email):
        messagebox.showerror("Validação", "E-mail inválido.")
        return False
    if telefone and not re.match(r"^\\d{8,15}$", telefone):
        messagebox.showerror("Validação", "Telefone deve ter 8–15 dígitos.")
        return False
    return True

def salvar_cliente(entry_nome, entry_email, entry_telefone, janela, cliente_id=None):
    nome = entry_nome.get().strip()
    email = entry_email.get().strip()
    telefone = entry_telefone.get().strip()
    if not validar_dados(nome, email, telefone):
        return
    if cliente_id:
        sql = "UPDATE clientes SET nome = ?, email = ?, telefone = ? WHERE id = ?"
        params = (nome, email, telefone, cliente_id)
    else:
        sql = "INSERT INTO clientes (nome, email, telefone) VALUES (?, ?, ?)"
        params = (nome, email, telefone)

    sucesso = executar_comando(sql, params)
    if sucesso:
        acao = "Editar" if cliente_id else "Criar"
        registrar_acao(acao, "Cliente", f"Nome:{nome} Email:{email}")
        messagebox.showinfo("Sucesso", "Cliente salvo!")
        janela.destroy()
    else:
        messagebox.showerror("Erro", "Falha ao salvar cliente.")

def cancelar(janela):
    if messagebox.askyesno("Cancelar", "Cancelar operação?"):
        janela.destroy()

def abrir_form_cliente(root, cliente=None):
    janela = tk.Toplevel(root)
    janela.title("Cadastro de Cliente")
    janela.geometry("360x270")
    janela.configure(bg=BG())
    janela.resizable(False, False)
    janela.grab_set()

    tk.Label(janela, text="Nome:", bg=BG(), fg=TX()).pack(anchor="w", padx=20, pady=(15, 0))
    entry_nome = tk.Entry(janela, width=42)
    entry_nome.pack(padx=20, pady=5)

    tk.Label(janela, text="E-mail:", bg=BG(), fg=TX()).pack(anchor="w", padx=20, pady=(10, 0))
    entry_email = tk.Entry(janela, width=42)
    entry_email.pack(padx=20, pady=5)

    tk.Label(janela, text="Telefone:", bg=BG(), fg=TX()).pack(anchor="w", padx=20, pady=(10, 0))
    entry_telefone = tk.Entry(janela, width=42)
    entry_telefone.pack(padx=20, pady=5)

    cliente_id = None
    if cliente:
        cliente_id = cliente.get("id")
        entry_nome.insert(0, cliente.get("nome", ""))
        entry_email.insert(0, cliente.get("email", ""))
        entry_telefone.insert(0, cliente.get("telefone", ""))

    botoes = tk.Frame(janela, bg=BG())
    botoes.pack(pady=18)
    btn_salvar = tk.Button(botoes, text="Salvar",
                           command=lambda: salvar_cliente(entry_nome, entry_email, entry_telefone, janela, cliente_id))
    ThemeManager.style_button(btn_salvar)
    btn_salvar.pack(side="left", padx=10)
    btn_cancelar = tk.Button(botoes, text="Cancelar", command=lambda: cancelar(janela))
    ThemeManager.style_button(btn_cancelar)
    btn_cancelar.pack(side="left", padx=10)

    janela.mainloop()