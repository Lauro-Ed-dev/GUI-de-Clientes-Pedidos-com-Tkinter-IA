# Gerenciamento de temas e estilos centralizados (Tk + ttk) com suporte Light/Dark

import tkinter as tk
from tkinter import ttk

THEMES = {
    "light": {
        "BG_COLOR": "#F8F9FA",
        "MENU_COLOR": "#344955",
        "HIGHLIGHT_COLOR": "#F9AA33",
        "BTN_ACTIVE_COLOR": "#4A6572",
        "BTN_COLOR": "#F9AA33",
        "TEXT_COLOR": "#232F34",
        "TEXT_BG": "#FFFFFF",
        "TREE_BG": "#FFFFFF",
        "TREE_FG": "#232F34",
        "TREE_SEL_BG": "#F9AA33",
        "TREE_SEL_FG": "#FFFFFF",
        "BORDER_COLOR": "#D9D9D9",
    },
    "dark": {
        "BG_COLOR": "#1F2428",
        "MENU_COLOR": "#14181B",
        "HIGHLIGHT_COLOR": "#FFB347",
        "BTN_ACTIVE_COLOR": "#2E3A40",
        "BTN_COLOR": "#FF8C42",
        "TEXT_COLOR": "#E1E5EA",
        "TEXT_BG": "#2A3136",
        "TREE_BG": "#2A3136",
        "TREE_FG": "#E1E5EA",
        "TREE_SEL_BG": "#FF8C42",
        "TREE_SEL_FG": "#14181B",
        "BORDER_COLOR": "#3A444A",
    }
}

TITLE_FONT = ("Arial", 18, "bold")
NORMAL_FONT = ("Arial", 13)
SMALL_FONT = ("Arial", 11)
BTN_FONT = ("Arial", 13, "bold")
BTN_FONT_SMALL = ("Arial", 10, "bold")

class ThemeManager:
    current = "light"
    vars = THEMES[current]
    registered_buttons = []
    registered_menu_buttons = []
    root_ref = None
    style = None

    @classmethod
    def set_root(cls, root):
        cls.root_ref = root
        cls.style = ttk.Style()
        cls.apply_ttk_style()

    @classmethod
    def switch_theme(cls, theme_name: str):
        if theme_name not in THEMES:
            return
        cls.current = theme_name
        cls.vars = THEMES[theme_name]
        cls._apply_to_all()
        cls.apply_ttk_style()

    @classmethod
    def get(cls, key):
        return cls.vars.get(key)

    @classmethod
    def register_button(cls, btn, menu=False):
        if menu:
            cls.registered_menu_buttons.append(btn)
        else:
            cls.registered_buttons.append(btn)

    @classmethod
    def style_button(cls, btn):
        btn.configure(
            bg=cls.get("BTN_COLOR"),
            fg="white",
            font=BTN_FONT,
            relief="flat",
            activebackground=cls.get("BTN_ACTIVE_COLOR"),
            activeforeground=cls.get("HIGHLIGHT_COLOR"),
            padx=10,
            pady=6,
            cursor="hand2"
        )
        cls.register_button(btn, menu=False)

    @classmethod
    def style_menu_button(cls, btn):
        btn.configure(
            fg="white",
            bg=cls.get("MENU_COLOR"),
            font=BTN_FONT,
            relief="flat",
            activebackground=cls.get("BTN_ACTIVE_COLOR"),
            activeforeground=cls.get("HIGHLIGHT_COLOR"),
            padx=12,
            pady=12,
            anchor="w",
            cursor="hand2"
        )
        cls.register_button(btn, menu=True)

    @classmethod
    def apply_ttk_style(cls):
        if cls.style is None:
            cls.style = ttk.Style()
        try:
            cls.style.theme_use("clam")
        except Exception:
            pass

        # Fallbacks seguros para campos de texto (ttk Entry/Combobox)
        text_fg = cls.vars.get("TEXT_FG", cls.vars.get("TEXT_COLOR"))
        text_bg = cls.vars.get("TEXT_BG", cls.vars.get("BG_COLOR"))

        # Treeview base
        cls.style.configure(
            "Treeview",
            background=cls.get("TREE_BG"),
            foreground=cls.get("TREE_FG"),
            fieldbackground=cls.get("TREE_BG"),
            rowheight=24,
            bordercolor=cls.get("BORDER_COLOR"),
            borderwidth=0,
        )
        cls.style.map(
            "Treeview",
            background=[("selected", cls.get("TREE_SEL_BG"))],
            foreground=[("selected", cls.get("TREE_SEL_FG"))],
        )

        # Cabeçalho do Treeview
        cls.style.configure(
            "Treeview.Heading",
            background=cls.get("MENU_COLOR"),
            foreground="white",
            relief="flat",
            font=("Arial", 11, "bold")
        )
        cls.style.layout(
            "Treeview.Heading",
            [
                ("Treeheading.cell", {"sticky": "nswe"}),
                ("Treeheading.border", {"sticky": "nswe", "children":
                    [("Treeheading.padding", {"sticky": "nswe", "children":
                        [("Treeheading.image", {"side": "right", "sticky": ""}),
                         ("Treeheading.text", {"sticky": "we"})]})]})
            ]
        )

        # Estilo alternativo usado pelos frames
        base = "Themed.Treeview"
        cls.style.configure(
            base,
            background=cls.get("TREE_BG"),
            foreground=cls.get("TREE_FG"),
            fieldbackground=cls.get("TREE_BG"),
            rowheight=24,
            bordercolor=cls.get("BORDER_COLOR"),
            borderwidth=0,
        )
        cls.style.map(
            base,
            background=[("selected", cls.get("TREE_SEL_BG"))],
            foreground=[("selected", cls.get("TREE_SEL_FG"))],
        )
        cls.style.configure(
            f"{base}.Heading",
            background=cls.get("MENU_COLOR"),
            foreground="white",
            relief="flat",
            font=("Arial", 11, "bold")
        )
        cls.style.layout(
            f"{base}.Heading",
            cls.style.layout("Treeview.Heading")
        )

        # Estilo de campos (ttk)
        cls.style.configure(
            "TEntry",
            fieldbackground=text_bg,
            foreground=text_fg,
            background=text_bg,
            bordercolor=cls.get("BORDER_COLOR"),
        )
        cls.style.configure(
            "TCombobox",
            fieldbackground=text_bg,
            foreground=text_fg,
            background=text_bg,
            bordercolor=cls.get("BORDER_COLOR"),
            arrowsize=16
        )
        cls.style.map("TCombobox",
            fieldbackground=[("readonly", text_bg)],
            foreground=[("readonly", text_fg)]
        )

    @classmethod
    def style_treeview(cls, tree: ttk.Treeview):
        tree.configure(style="Themed.Treeview")

    @classmethod
    def _apply_to_all(cls):
        if cls.root_ref is not None:
            cls.root_ref.configure(bg=cls.get("BG_COLOR"))
        for b in cls.registered_buttons:
            b.configure(
                bg=cls.get("BTN_COLOR"),
                fg="white",
                activebackground=cls.get("BTN_ACTIVE_COLOR"),
                activeforeground=cls.get("HIGHLIGHT_COLOR"),
            )
        for mb in cls.registered_menu_buttons:
            mb.configure(
                bg=cls.get("MENU_COLOR"),
                fg="white",
                activebackground=cls.get("BTN_ACTIVE_COLOR"),
                activeforeground=cls.get("HIGHLIGHT_COLOR"),
            )
        if cls.root_ref is not None:
            cls._recursive_bg_update(cls.root_ref)

    @classmethod
    def _recursive_bg_update(cls, widget):
        if isinstance(widget, (tk.Frame, tk.Label, tk.Toplevel, tk.LabelFrame)):
            try:
                widget.configure(bg=cls.get("BG_COLOR"))
            except Exception:
                pass
        for child in widget.winfo_children():
            cls._recursive_bg_update(child)

# Helpers
def BG(): return ThemeManager.get("BG_COLOR")
def MENU(): return ThemeManager.get("MENU_COLOR")
def TX(): return ThemeManager.get("TEXT_COLOR")
def HI(): return ThemeManager.get("HIGHLIGHT_COLOR")
def BTN(): return ThemeManager.get("BTN_COLOR")
def TBG(): return ThemeManager.get("TEXT_BG")