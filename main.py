import tkinter as tk
from tkinter import ttk, messagebox
import traceback

from db import inicializar_banco
from frame_client import FrameClientes
from form_client import abrir_form_cliente
from form_pedido import abrir_form_pedido
from frame_pedido import FramePedidos


# --------------------------------------------------------
# Log de erros simples
# --------------------------------------------------------
def registrar_erro(e):
    with open("erros.log", "a", encoding="utf-8") as f:
        f.write("\n" + "-" * 60 + "\n")
        f.write(traceback.format_exc())
    print("Erro registrado:", e)


# --------------------------------------------------------
# Classe principal do aplicativo
# --------------------------------------------------------
class AppPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("💼 Sistema de Clientes e Pedidos")
        self.geometry("850x600")
        self.protocol("WM_DELETE_WINDOW", self.confirmar_saida)
        self.criar_interface()
        self.configure(bg="#f5f5f5")

    # ----------------------------------------------------
    # Interface principal
    # ----------------------------------------------------
    def criar_interface(self):
        menu_bar = tk.Menu(self)
        self.config(menu=menu_bar)

        # MENU CLIENTES
        menu_clientes = tk.Menu(menu_bar, tearoff=0)
        menu_clientes.add_command(label="Listar Clientes", command=self.mostrar_clientes)
        menu_clientes.add_command(label="Novo Cliente", command=self.novo_cliente)
        menu_bar.add_cascade(label="👥 Clientes", menu=menu_clientes)

        # MENU PEDIDOS
        menu_pedidos = tk.Menu(menu_bar, tearoff=0)
        menu_pedidos.add_command(label="Novo Pedido", command=self.novo_pedido)
        menu_pedidos.add_command(label="Listar Pedidos", command=self.mostrar_pedidos)
        menu_bar.add_cascade(label="🧾 Pedidos", menu=menu_pedidos)

        # MENU SAIR
        menu_bar.add_command(label="❌ Sair", command=self.confirmar_saida)

        # FRAME DE CONTEÚDO PRINCIPAL
        self.frame_conteudo = tk.Frame(self, bg="#f5f5f5")
        self.frame_conteudo.pack(fill="both", expand=True)

        self.mostrar_boas_vindas()

    # ----------------------------------------------------
    # Seções de conteúdo
    # ----------------------------------------------------
    def limpar_conteudo(self):
        for widget in self.frame_conteudo.winfo_children():
            widget.destroy()

    def mostrar_boas_vindas(self):
        self.limpar_conteudo()
        tk.Label(
            self.frame_conteudo,
            text="Bem-vindo ao Sistema de Clientes e Pedidos!",
            font=("Arial", 16, "bold"),
            bg="#f5f5f5",
            fg="#333"
        ).pack(pady=50)

        tk.Label(
            self.frame_conteudo,
            text="Use o menu acima para gerenciar clientes ou criar pedidos.",
            bg="#f5f5f5",
            fg="#666"
        ).pack(pady=10)

    def mostrar_clientes(self):
        self.limpar_conteudo()
        try:
            self.frame_clientes = FrameClientes(self.frame_conteudo)
            self.frame_clientes.pack(fill="both", expand=True)
        except Exception as e:
            registrar_erro(e)
            messagebox.showerror("Erro", "Não foi possível carregar a lista de clientes.")

    def mostrar_pedidos(self):
        self.limpar_conteudo()
        try:
            frame = FramePedidos(self.frame_conteudo)
            frame.pack(fill="both", expand=True)
        except Exception as e:
            registrar_erro(e)
            messagebox.showerror("Erro", "Não foi possível carregar a lista de pedidos.")

    # ----------------------------------------------------
    # Ações do menu
    # ----------------------------------------------------
    def novo_cliente(self):
        try:
            abrir_form_cliente(self)
            # Após fechar o form, recarregar se a lista estiver visível
            self.after(500, self.recarregar_clientes)
        except Exception as e:
            registrar_erro(e)
            messagebox.showerror("Erro", "Falha ao abrir o formulário de cliente.")

    def novo_pedido(self):
        try:
            abrir_form_pedido(self)
            self.after(500, self.recarregar_pedidos)
        except Exception as e:
            registrar_erro(e)
            messagebox.showerror("Erro", "Falha ao abrir o formulário de pedido.")

    # ----------------------------------------------------
    # Recarregar dados quando o usuário volta de uma janela
    # ----------------------------------------------------
    def recarregar_clientes(self):
        if hasattr(self, "frame_clientes"):
            try:
                self.frame_clientes.carregar_clientes()
            except Exception:
                pass

    def recarregar_pedidos(self):
        if hasattr(self, "frame_pedidos"):
            try:
                self.frame_pedidos.carregar_pedidos()
            except Exception:
                pass

    # ----------------------------------------------------
    # Fechamento seguro
    # ----------------------------------------------------
    def confirmar_saida(self):
        """Prevenção de fechamento acidental."""
        if messagebox.askyesno("Sair", "Tem certeza que deseja fechar o sistema?"):
            self.destroy()


# --------------------------------------------------------
# Função principal
# --------------------------------------------------------
def main():
    try:
        inicializar_banco()
    except Exception as e:
        registrar_erro(e)
        messagebox.showerror("Erro crítico", "Falha ao inicializar o banco de dados.")
        return

    try:
        app = AppPrincipal()
        messagebox.showinfo(
            "Bem-vindo!",
            "Sistema iniciado com sucesso.\n\nUse o menu 'Clientes' para gerenciar clientes\nou 'Pedidos' para registrar vendas."
        )
        app.mainloop()
    except Exception as e:
        registrar_erro(e)
        messagebox.showerror("Erro inesperado", "Ocorreu um erro fatal. Veja erros.log para detalhes.")


if __name__ == "__main__":
    main()
