import tkinter as tk
from estilo import ThemeManager, TITLE_FONT, NORMAL_FONT, SMALL_FONT, BG, TX, HI

class ConfiguracoesFrame(tk.Frame):
    def __init__(self, master=None, on_theme_change=None):
        super().__init__(master, bg=BG())
        self.on_theme_change = on_theme_change
        self.pack(fill="both", expand=True)  # ESSENCIAL: sem isso o frame não aparece
        self._criar_ui()

    def _criar_ui(self):
        tk.Label(
            self,
            text="Configurações",
            font=TITLE_FONT,
            bg=BG(),
            fg=TX()
        ).pack(pady=15)

        # Tema atual
        self.lbl_tema_atual = tk.Label(
            self,
            text=f"Tema atual: {ThemeManager.current.capitalize()}",
            font=NORMAL_FONT,
            bg=BG(),
            fg=HI()
        )
        self.lbl_tema_atual.pack(pady=5)

        # Seção de troca de tema
        frame_tema = tk.Frame(self, bg=BG())
        frame_tema.pack(pady=10)

        tk.Label(
            frame_tema,
            text="Alterar tema:",
            font=NORMAL_FONT,
            bg=BG(),
            fg=TX()
        ).grid(row=0, column=0, padx=8)

        btn_light = tk.Button(
            frame_tema,
            text="Light",
            command=lambda: self._alterar_tema("light")
        )
        ThemeManager.style_button(btn_light)
        btn_light.grid(row=0, column=1, padx=6)

        btn_dark = tk.Button(
            frame_tema,
            text="Dark",
            command=lambda: self._alterar_tema("dark")
        )
        ThemeManager.style_button(btn_dark)
        btn_dark.grid(row=0, column=2, padx=6)

        # Preview de cores principais
        preview = tk.Frame(self, bg=BG())
        preview.pack(pady=20)

        tk.Label(preview, text="Preview de Cores", font=NORMAL_FONT, bg=BG(), fg=TX()).pack(pady=4)

        cores = {
            "BG_COLOR": BG(),
            "MENU_COLOR": ThemeManager.get("MENU_COLOR"),
            "HIGHLIGHT_COLOR": HI(),
            "BTN_COLOR": ThemeManager.get("BTN_COLOR"),
            "TEXT_COLOR": TX(),
            "TEXT_BG": ThemeManager.get("TEXT_BG"),
        }

        grid = tk.Frame(preview, bg=BG())
        grid.pack()

        for i, (nome, cor) in enumerate(cores.items()):
            cell = tk.Frame(grid, bg=cor, width=120, height=40, highlightthickness=1,
                            highlightbackground=ThemeManager.get("BTN_ACTIVE_COLOR"))
            cell.grid(row=i // 3, column=i % 3, padx=6, pady=6)
            tk.Label(cell, text=nome, bg=cor,
                     fg=("white" if nome in ("MENU_COLOR", "BTN_COLOR", "HIGHLIGHT_COLOR") and ThemeManager.current == "dark"
                         else ("white" if nome in ("MENU_COLOR", "BTN_COLOR") else TX())),
                     font=("Arial", 9, "bold")).pack(expand=True)

        tk.Label(
            self,
            text="A mudança de tema afeta toda a aplicação instantaneamente.",
            font=SMALL_FONT,
            bg=BG(),
            fg=TX()
        ).pack(pady=10)

    def _alterar_tema(self, tema):
        if tema == ThemeManager.current:
            return
        ThemeManager.switch_theme(tema)
        # Atualiza label
        self.lbl_tema_atual.config(text=f"Tema atual: {ThemeManager.current.capitalize()}")
        # Re-renderiza esta tela (limpar e recriar)
        for w in self.winfo_children():
            w.destroy()
        self._criar_ui()
        # Callback para main atualizar barras/top
        if self.on_theme_change:
            self.on_theme_change()