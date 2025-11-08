import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
from datetime import datetime
import csv
import logging
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

logging.basicConfig(filename="relatorios.log", level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

class Relatorios(tk.Toplevel):
    def __init__(self, master=None, db_path="app.db"):
        super().__init__(master)
        self.title("Relatórios")
        self.db_path = db_path
        self.geometry("700x500")
        self.resizable(False, False)

        # Filtros
        filtro_frame = tk.Frame(self)
        filtro_frame.pack(pady=10)

        tk.Label(filtro_frame, text="Data Inicial (YYYY-MM-DD):").grid(row=0, column=0)
        self.entry_data_ini = tk.Entry(filtro_frame, width=12)
        self.entry_data_ini.grid(row=0, column=1)

        tk.Label(filtro_frame, text="Data Final (YYYY-MM-DD):").grid(row=0, column=2)
        self.entry_data_fim = tk.Entry(filtro_frame, width=12)
        self.entry_data_fim.grid(row=0, column=3)

        tk.Label(filtro_frame, text="Cliente:").grid(row=0, column=4)
        self.combo_cliente = ttk.Combobox(filtro_frame, state="readonly", width=22)
        self.combo_cliente.grid(row=0, column=5)

        btn_filtrar = tk.Button(filtro_frame, text="Filtrar", command=self.filtrar)
        btn_filtrar.grid(row=0, column=6, padx=15)

        # Treeview
        columns = ("cliente", "data", "itens", "total")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, minwidth=50, width=140)
        self.tree.pack(fill="both", expand=True, padx=8, pady=6)

        # Botões de Exportação
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=12)
        tk.Button(btn_frame, text="Exportar CSV", command=self.exportar_csv).pack(side="left", padx=8)
        tk.Button(btn_frame, text="Exportar PDF", command=self.exportar_pdf).pack(side="left", padx=8)

        self.carregar_clientes()

    def carregar_clientes(self):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT nome FROM clientes ORDER BY nome")
            nomes = [row[0] for row in cursor.fetchall()]
            self.combo_cliente['values'] = ["Todos"] + nomes
            self.combo_cliente.set("Todos")
            conn.close()
        except Exception as e:
            logging.error(f"Erro ao carregar clientes: {e}")
            messagebox.showerror("Erro", "Não foi possível carregar os clientes.")

    def filtrar(self):
        self.tree.delete(*self.tree.get_children())
        try:
            data_ini = self.entry_data_ini.get().strip()
            data_fim = self.entry_data_fim.get().strip()
            cliente = self.combo_cliente.get()

            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Monta consulta dinâmica
            query = """
            SELECT c.nome, p.data, GROUP_CONCAT(ip.produto || ' (Qtd: ' || ip.quantidade || ')', ', '), p.total
            FROM pedidos p
            JOIN clientes c ON p.cliente_id = c.id
            LEFT JOIN itens_pedido ip ON p.id = ip.pedido_id
            WHERE 1=1
            """
            params = []
            if cliente != "Todos":
                query += " AND c.nome = ?"
                params.append(cliente)
            if data_ini:
                query += " AND p.data >= ?"
                params.append(data_ini)
            if data_fim:
                query += " AND p.data <= ?"
                params.append(data_fim)

            query += " GROUP BY p.id ORDER BY p.data DESC"

            cursor.execute(query, params)
            for nome, data, itens, valor in cursor.fetchall():
                self.tree.insert("", "end", values=(nome, data, itens, f"R$ {valor:.2f}"))
            conn.close()
            logging.info("Filtro realizado com sucesso.")
        except Exception as e:
            logging.error(f"Erro ao filtrar pedidos: {e}")
            messagebox.showerror("Erro", f"Não foi possível filtrar os pedidos.\n{e}")

    def exportar_csv(self):
        try:
            file = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files","*.csv")])
            if file:
                with open(file, "w", newline='', encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerow(["Cliente", "Data", "Itens", "Total"])
                    for row in self.tree.get_children():
                        writer.writerow(self.tree.item(row)['values'])
                logging.info(f"Relatório exportado para CSV: {file}")
                os.startfile(file)
                messagebox.showinfo("Exportação", "Relatório CSV gerado e aberto com sucesso!")
        except Exception as e:
            logging.error(f"Erro na exportação CSV: {e}")
            messagebox.showerror("Erro", f"Não foi possível exportar para CSV.\n{e}")

    def exportar_pdf(self):
        try:
            file = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files","*.pdf")])
            if file:
                c = canvas.Canvas(file, pagesize=letter)
                width, height = letter
                c.setFont("Helvetica", 11)
                c.drawString(30, height-40, "Relatório de Pedidos")
                y = height - 70
                c.setFont("Helvetica-Bold", 9)
                c.drawString(30, y, "Cliente")
                c.drawString(150, y, "Data")
                c.drawString(240, y, "Itens")
                c.drawString(500, y, "Total")
                c.setFont("Helvetica", 9)
                y -= 15
                for row in self.tree.get_children():
                    cliente, data, itens, total = self.tree.item(row)['values']
                    c.drawString(30, y, str(cliente))
                    c.drawString(150, y, str(data))
                    c.drawString(240, y, str(itens))
                    c.drawString(500, y, str(total))
                    y -= 15
                    if y < 50:
                        c.showPage()
                        y = height - 50
                c.save()
                logging.info(f"Relatório exportado para PDF: {file}")
                os.startfile(file)
                messagebox.showinfo("Exportação", "Relatório PDF gerado e aberto com sucesso!")
        except Exception as e:
            logging.error(f"Erro na exportação PDF: {e}")
            messagebox.showerror("Erro", f"Não foi possível exportar para PDF.\n{e}")

# Exemplo de uso
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    rel = Relatorios(master=root, db_path="app.db")
    rel.mainloop()