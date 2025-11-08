import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime

class Dashboard(tk.Toplevel):
    def __init__(self, master=None, db_path="app.db"):
        super().__init__(master)
        self.title("Dashboard")
        self.db_path = db_path
        self.geometry("350x220")
        self.resizable(False, False)

        self.lbl_total_clientes = tk.Label(self, text="Total de clientes: ", font=("Arial", 14))
        self.lbl_total_clientes.pack(pady=10)

        self.lbl_total_pedidos = tk.Label(self, text="Total de pedidos no mês: ", font=("Arial", 14))
        self.lbl_total_pedidos.pack(pady=10)

        self.lbl_ticket_medio = tk.Label(self, text="Ticket médio: ", font=("Arial", 14))
        self.lbl_ticket_medio.pack(pady=10)

        btn_atualizar = tk.Button(self, text="Atualizar", font=("Arial", 12), command=self.atualizar)
        btn_atualizar.pack(pady=10)

        self.atualizar()

    def atualizar(self):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Total de clientes
            cursor.execute("SELECT COUNT(*) FROM clientes")
            total_clientes = cursor.fetchone()[0]

            # Total de pedidos no mês (coluna data em pedidos, formato 'YYYY-MM-DD')
            mes = datetime.now().strftime("%Y-%m")
            cursor.execute(
                "SELECT COUNT(*) FROM pedidos WHERE strftime('%Y-%m', data) = ?",
                (mes,))
            total_pedidos_mes = cursor.fetchone()[0]

            # Ticket médio (média do campo total dos pedidos no mês)
            cursor.execute(
                "SELECT AVG(total) FROM pedidos WHERE strftime('%Y-%m', data) = ?",
                (mes,))
            ticket_medio = cursor.fetchone()[0]
            if ticket_medio is None:
                ticket_medio = 0

            self.lbl_total_clientes.config(text=f"Total de clientes: {total_clientes}")
            self.lbl_total_pedidos.config(text=f"Total de pedidos no mês: {total_pedidos_mes}")
            self.lbl_ticket_medio.config(text=f"Ticket médio: R$ {ticket_medio:.2f}")

            messagebox.showinfo("Atualizado!", "Dados recalculados com sucesso.")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao atualizar os dados.\n{e}")
        finally:
            if 'conn' in locals():
                conn.close()

# Exemplo de uso:
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    dash = Dashboard(master=root, db_path="app.db")
    dash.mainloop()