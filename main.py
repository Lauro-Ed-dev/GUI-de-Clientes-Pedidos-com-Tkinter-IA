import tkinter as tk
from tkinter import messagebox

# Frames / componentes temáticos
from frame_client import FrameClientes
from frame_pedido import FramePedidos
from dashboard import Dashboard
from relatorios import Relatorios
from historico import Historico
from configuracoes import ConfiguracoesFrame

# Gerenciador de temas e helpers
from estilo import ThemeManager, TITLE_FONT, BG, MENU, TX, HI

class AppPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        # Registra raiz para que o ThemeManager possa atualizar dinamicamente
        ThemeManager.set_root(self)

        self.title("💼 Sistema de Clientes e Pedidos")
        self.geometry("1100x680")
        self.minsize(980, 620)
        self.configure(bg=BG())
        self.protocol("WM_DELETE_WINDOW", self.confirmar_saida)

        # Estado da barra lateral
        self.sidebar_visible = False
        self.current_section = "boas_vindas"

        self._criar_layout()
        self.show_frame("boas_vindas")

    # ------------------------------------------------------------------
    # Layout principal: Top Bar + (Sidebar dinâmica) + Área de conteúdo
    # ------------------------------------------------------------------
    def _criar_layout(self):
        # Top bar
        self.top_bar = tk.Frame(self, bg=MENU(), height=54)
        self.top_bar.pack(side="top", fill="x")

        self.btn_menu = tk.Button(
            self.top_bar,
            text="☰",
            command=self.toggle_sidebar,
            bg=MENU(),
            fg="white",
            relief="flat",
            font=("Arial", 20, "bold"),
            activebackground=MENU(),
            activeforeground=HI(),
            padx=18,
            cursor="hand2"
        )
        self.btn_menu.pack(side="left")

        self.lbl_title = tk.Label(
            self.top_bar,
            text="Sistema de Clientes e Pedidos",
            font=("Arial", 18, "bold"),
            bg=MENU(),
            fg="white"
        )
        self.lbl_title.pack(side="left", padx=10)

        # Container principal (sidebar + main_frame)
        self.container = tk.Frame(self, bg=BG())
        self.container.pack(fill="both", expand=True)

        # Sidebar (criada, mas inicialmente oculta)
        self.sidebar = tk.Frame(self.container, bg=MENU(), width=210)
        self._montar_sidebar()

        # Área de conteúdo
        self.main_frame = tk.Frame(self.container, bg=BG())
        self.main_frame.pack(side="right", fill="both", expand=True)

    # ------------------------------------------------------------------
    # Botões do menu lateral
    # ------------------------------------------------------------------
    def _montar_sidebar(self):
        btns_info = [
            ("👥 Clientes", "clientes"),
            ("🧾 Pedidos", "pedidos"),
            ("📊 Dashboard", "dashboard"),
            ("📈 Relatórios", "relatorios"),
            ("📝 Histórico", "historico"),
            ("⚙️ Configurações", "configuracoes"),
            ("❌ Sair", "sair"),
        ]
        for text, key in btns_info:
            b = tk.Button(
                self.sidebar,
                text=text,
                anchor="w",
                command=lambda k=key: self._sidebar_action(k),
                bg=MENU(),
                fg="white",
                relief="flat",
                font=("Arial", 13, "bold"),
                activebackground=MENU(),
                activeforeground=HI(),
                padx=14,
                pady=12,
                cursor="hand2"
            )
            b.pack(fill="x")

    # ------------------------------------------------------------------
    # Mostrar / ocultar sidebar
    # ------------------------------------------------------------------
    def toggle_sidebar(self):
        if self.sidebar_visible:
            self.sidebar.pack_forget()
            self.sidebar_visible = False
        else:
            self.sidebar.pack(side="left", fill="y")
            self.sidebar_visible = True

    # ------------------------------------------------------------------
    # Ação ao clicar em um item da sidebar
    # ------------------------------------------------------------------
    def _sidebar_action(self, key):
        if key == "sair":
            self.confirmar_saida()
            return
        self.show_frame(key)
        # Oculta a barra após escolha (opcional)
        self.toggle_sidebar()

    # ------------------------------------------------------------------
    # Navegação dinâmica: recria o conteúdo principal
    # ------------------------------------------------------------------
    def show_frame(self, secao):
        for w in self.main_frame.winfo_children():
            w.destroy()
        self.current_section = secao

        if secao == "boas_vindas":
            self._frame_boas_vindas()
        elif secao == "clientes":
            FrameClientes(self.main_frame)
        elif secao == "pedidos":
            FramePedidos(self.main_frame)
        elif secao == "dashboard":
            Dashboard(self.main_frame)
        elif secao == "relatorios":
            Relatorios(self.main_frame)
        elif secao == "historico":
            Historico(self.main_frame)
        elif secao == "configuracoes":
            ConfiguracoesFrame(self.main_frame, on_theme_change=self._on_theme_changed)

    # ------------------------------------------------------------------
    # Tela inicial
    # ------------------------------------------------------------------
    def _frame_boas_vindas(self):
        frame = tk.Frame(self.main_frame, bg=BG())
        frame.pack(expand=True)
        tk.Label(
            frame,
            text="Bem-vindo!",
            font=("Arial", 30, "bold"),
            bg=BG(),
            fg=TX()
        ).pack(pady=50)
        tk.Label(
            frame,
            text="Clique no ícone ☰ para abrir o menu lateral.",
            font=("Arial", 16),
            bg=BG(),
            fg=HI()
        ).pack(pady=10)

    # ------------------------------------------------------------------
    # Callback usado pela tela de Configurações após troca de tema
    # ------------------------------------------------------------------
    def _on_theme_changed(self):
        # Atualiza barras e componentes principais
        self.configure(bg=BG())
        self.top_bar.configure(bg=MENU())
        self.btn_menu.configure(bg=MENU())
        self.lbl_title.configure(bg=MENU())
        # Recria frame atual com o novo tema aplicado
        self.show_frame(self.current_section)

    # ------------------------------------------------------------------
    # Saída com confirmação
    # ------------------------------------------------------------------
    def confirmar_saida(self):
        if messagebox.askyesno("Sair", "Tem certeza que deseja fechar o sistema?"):
            self.destroy()

# ----------------------------------------------------------------------
# Execução
# ----------------------------------------------------------------------
if __name__ == "__main__":
    app = AppPrincipal()
    app.mainloop()