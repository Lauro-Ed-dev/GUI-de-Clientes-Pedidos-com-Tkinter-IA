import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from db import consultar, conectar
from log_utils import registrar_acao
from estilo import ThemeManager, BG, TX, HI

def abrir_form_pedido(root):
    janela = tk.Toplevel(root)
    janela.title("Novo Pedido")
    janela.geometry("720x520")
    janela.configure(bg=BG())
    janela.grab_set()
    janela.resizable(False, False)

    frame_top = tk.Frame(janela, bg=BG())
    frame_top.pack(fill="x", padx=15, pady=10)

    tk.Label(frame_top, text="Cliente:", bg=BG(), fg=TX()).grid(row=0, column=0, sticky="w")
    clientes = consultar("SELECT id, nome FROM clientes ORDER BY nome")
    nomes_clientes = [c[1] for c in clientes]
    cb_cliente = ttk.Combobox(frame_top, values=nomes_clientes, state="readonly", width=40)
    cb_cliente.grid(row=0, column=1, padx=5)
    if nomes_clientes:
        cb_cliente.current(0)

    tk.Label(frame_top, text="Data:", bg=BG(), fg=TX()).grid(row=0, column=2, sticky="w", padx=(20, 0))
    entry_data = tk.Entry(frame_top, width=12)
    entry_data.grid(row=0, column=3)
    entry_data.insert(0, date.today().isoformat())

    frame_itens = tk.LabelFrame(janela, text="Itens do Pedido", bg=BG(), fg=TX())
    frame_itens.pack(fill="both", expand=True, padx=15, pady=10)

    colunas = ("produto", "quantidade", "preco_unit", "subtotal")
    tree = ttk.Treeview(frame_itens, columns=colunas, show="headings", height=10)
    for c in colunas:
        tree.heading(c, text=c.capitalize())
        tree.column(c, width=160 if c != "produto" else 240, anchor="center" if c != "produto" else "w")
    ThemeManager.style_treeview(tree)
    tree.pack(side="left", fill="both", expand=True)

    scrollbar = ttk.Scrollbar(frame_itens, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    frame_add = tk.Frame(janela, bg=BG())
    frame_add.pack(fill="x", padx=15, pady=5)

    tk.Label(frame_add, text="Produto:", bg=BG(), fg=TX()).grid(row=0, column=0, padx=5, pady=5)
    entry_produto = tk.Entry(frame_add, width=25)
    entry_produto.grid(row=0, column=1)

    tk.Label(frame_add, text="Qtd:", bg=BG(), fg=TX()).grid(row=0, column=2)
    entry_qtd = tk.Entry(frame_add, width=6)
    entry_qtd.grid(row=0, column=3)

    tk.Label(frame_add, text="Preço Unit.:", bg=BG(), fg=TX()).grid(row=0, column=4)
    entry_preco = tk.Entry(frame_add, width=10)
    entry_preco.grid(row=0, column=5)

    lbl_total = tk.Label(janela, text="Total: R$ 0.00", font=("Arial", 13, "bold"), bg=BG(), fg=HI())
    lbl_total.pack(pady=6)

    btn_add = tk.Button(frame_add, text="Adicionar Item",
                        command=lambda: adicionar_item(tree, entry_produto, entry_qtd, entry_preco, lbl_total))
    ThemeManager.style_button(btn_add)
    btn_add.grid(row=0, column=6, padx=10)

    btn_remove = tk.Button(frame_add, text="Remover Selecionado",
                           command=lambda: remover_item(tree, lbl_total))
    ThemeManager.style_button(btn_remove)
    btn_remove.grid(row=0, column=7, padx=5)

    frame_bottom = tk.Frame(janela, bg=BG())
    frame_bottom.pack(fill="x", padx=15, pady=12)

    btn_salvar = tk.Button(frame_bottom, text="Salvar Pedido", width=15,
                           command=lambda: salvar_pedido(janela, cb_cliente, clientes, entry_data, tree))
    ThemeManager.style_button(btn_salvar)
    btn_salvar.pack(side="right", padx=10)

    btn_cancelar = tk.Button(frame_bottom, text="Cancelar", width=10,
                             command=lambda: janela.destroy())
    ThemeManager.style_button(btn_cancelar)
    btn_cancelar.pack(side="right")

def adicionar_item(tree, entry_produto, entry_qtd, entry_preco, lbl_total):
    produto = entry_produto.get().strip()
    try:
        qtd = int(entry_qtd.get())
        preco = float(entry_preco.get().replace(",", "."))
    except ValueError:
        messagebox.showerror("Erro", "Quantidade e preço devem ser numéricos.")
        return
    if not produto or qtd <= 0 or preco <= 0:
        messagebox.showerror("Erro", "Preencha todos os campos corretamente.")
        return
    subtotal = qtd * preco
    tree.insert("", "end", values=(produto, qtd, f"{preco:.2f}", f"{subtotal:.2f}"))
    entry_produto.delete(0, tk.END)
    entry_qtd.delete(0, tk.END)
    entry_preco.delete(0, tk.END)
    atualizar_total(tree, lbl_total)

def remover_item(tree, lbl_total):
    sel = tree.selection()
    if not sel:
        messagebox.showinfo("Atenção", "Selecione um item.")
        return
    for item in sel:
        tree.delete(item)
    atualizar_total(tree, lbl_total)

def atualizar_total(tree, lbl_total):
    total = 0
    for item in tree.get_children():
        subtotal = float(tree.item(item, "values")[3])
        total += subtotal
    lbl_total.config(text=f"Total: R$ {total:.2f}")

def salvar_pedido(janela, cb_cliente, clientes, entry_data, tree):
    if not clientes:
        messagebox.showerror("Erro", "Nenhum cliente cadastrado.")
        return
    cliente_nome = cb_cliente.get()
    cliente_id = next((c[0] for c in clientes if c[1] == cliente_nome), None)
    data = entry_data.get().strip()
    itens = [tree.item(i, "values") for i in tree.get_children()]
    if not itens:
        messagebox.showerror("Erro", "Adicione itens antes de salvar.")
        return
    total = sum(float(i[3]) for i in itens)

    conn = conectar()
    if conn is None:
        messagebox.showerror("Erro", "Banco indisponível.")
        return

    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO pedidos (cliente_id, data, total) VALUES (?, ?, ?)",
            (cliente_id, data, total)
        )
        pedido_id = cur.lastrowid
        for item in itens:
            cur.execute(
                "INSERT INTO itens_pedido (pedido_id, produto, quantidade, preco_unit) VALUES (?, ?, ?, ?)",
                (pedido_id, item[0], int(item[1]), float(item[2]))
            )
        conn.commit()
        registrar_acao("Criar", "Pedido", f"Cliente:{cliente_nome} Data:{data} Total:{total:.2f}")
        messagebox.showinfo("Sucesso", "Pedido salvo!")
        janela.destroy()
    except Exception as e:
        conn.rollback()
        messagebox.showerror("Erro", f"Falha ao salvar: {e}")
    finally:
        conn.close()