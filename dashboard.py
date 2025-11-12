import tkinter as tk
import sqlite3
from datetime import datetime
from estilo import ThemeManager, TITLE_FONT, NORMAL_FONT, TX, BG, HI

class Dashboard(tk.Frame):
    def __init__(self, master=None, db_path="app.db"):
        super().__init__(master, bg=BG())
        self.db_path = db_path
        self.pack(fill="both", expand=True)
        self._criar_ui()
        self.atualizar_dados()

    def _criar_ui(self):
        titulo = tk.Label(self, text="Dashboard", font=TITLE_FONT, bg=BG(), fg=TX())
        titulo.pack(pady=15)

        self.lbl_total_clientes = tk.Label(self, font=NORMAL_FONT, bg=BG(), fg=TX())
        self.lbl_total_clientes.pack(pady=5)

        self.lbl_total_pedidos = tk.Label(self, font=NORMAL_FONT, bg=BG(), fg=TX())
        self.lbl_total_pedidos.pack(pady=5)

        self.lbl_ticket_medio = tk.Label(self, font=NORMAL_FONT, bg=BG(), fg=TX())
        self.lbl_ticket_medio.pack(pady=5)

        self.btn_atualizar = tk.Button(self, text="Recalcular", command=self.atualizar_dados)
        ThemeManager.style_button(self.btn_atualizar)
        self.btn_atualizar.pack(pady=15)

    def atualizar_dados(self):
        try:
            conn = sqlite3.connect(self.db_path)
            cur = conn.cursor()

            cur.execute("SELECT COUNT(*) FROM clientes")
            total_clientes = cur.fetchone()[0]

            mes = datetime.now().strftime("%Y-%m")
            cur.execute("SELECT COUNT(*) FROM pedidos WHERE strftime('%Y-%m', data) = ?", (mes,))
            total_pedidos_mes = cur.fetchone()[0]

            cur.execute("SELECT AVG(total) FROM pedidos WHERE strftime('%Y-%m', data) = ?", (mes,))
            ticket_medio = cur.fetchone()[0] or 0

            self.lbl_total_clientes.config(text=f"Total de clientes: {total_clientes}")
            self.lbl_total_pedidos.config(text=f"Pedidos neste mês: {total_pedidos_mes}")
            self.lbl_ticket_medio.config(text=f"Ticket médio (mês): R$ {ticket_medio:.2f}")
        except Exception as e:
            self.lbl_ticket_medio.config(text=f"Erro ao calcular: {e}")
        finally:
            try:
                conn.close()
            except Exception:
                pass