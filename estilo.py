# Arquivo para centralizar a estilização (cores, fontes, tamanhos, estilos de botão) do projeto.

BG_COLOR = "#F8F9FA"
MENU_COLOR = "#344955"
HIGHLIGHT_COLOR = "#F9AA33"
BTN_ACTIVE_COLOR = "#4A6572"
BTN_COLOR = "#F9AA33"
TEXT_COLOR = "#232F34"
TITLE_FONT = ("Arial", 18, "bold")
NORMAL_FONT = ("Arial", 13)
SMALL_FONT = ("Arial", 11)
BTN_FONT = ("Arial", 13, "bold")
BTN_FONT_SMALL = ("Arial", 10, "bold")
TEXT_BG = "#FBFBFB"

def btn_style(widget):
    widget.configure(
        bg=BTN_COLOR,
        fg="white",
        font=BTN_FONT,
        relief="flat",
        activebackground=BTN_ACTIVE_COLOR,
        activeforeground=HIGHLIGHT_COLOR,
        padx=10,
        pady=6
    )

def menu_btn_style(widget):
    widget.configure(
        fg="white",
        bg=MENU_COLOR,
        font=BTN_FONT,
        relief="flat",
        activebackground=BTN_ACTIVE_COLOR,
        activeforeground=HIGHLIGHT_COLOR,
        padx=10,
        pady=15
    )