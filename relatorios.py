import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import sqlite3
import csv
import logging
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from estilo import ThemeManager, TITLE_FONT, SMALL_FONT, NORMAL_FONT, BG, TX, HI

logging.basicConfig(filename="relatorios.log", level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

class Relatorios(tk.Frame):
    def __init__(self, master=None, db_path="app.db"):
        super().__init__(master, bg=BG())
        self.db_path = db_path
        self.pack(fill="both", expand=True)
        self._criar_ui()
        self.carregar_clientes()

    def _criar_ui(self):
        titulo = tk.Label(self, text="Relatórios", font=TITLE_FONT, bg=BG(), fg=TX())
        titulo.pack(pady=10)

        filtro_frame = tk.Frame(self, bg=BG())
        filtro_frame.pack(pady=8)

        tk.Label(filtro_frame, text="Data Inicial (YYYY-MM-DD):", bg=BG(), fg=TX(), font=SMALL_FONT).grid(row=0, column=0, padx=4, pady=4, sticky="w")
        self.entry_data_ini = tk.Entry(filtro_frame, width=12)
        self.entry_data_ini.grid(row=0, column=1, padx=4, pady=4)

        tk.Label(filtro_frame, text="Data Final (YYYY-MM-DD):", bg=BG(), fg=TX(), font=SMALL_FONT).grid(row=0, column=2, padx=4, pady=4, sticky="w")
        self.entry_data_fim = tk.Entry(filtro_frame, width=12)
        self.entry_data_fim.grid(row=0, column=3, padx=4, pady=4)

        tk.Label(filtro_frame, text="Cliente:", bg=BG(), fg=TX(), font=SMALL_FONT).grid(row=0, column=4, padx=4, pady=4, sticky="w")
        self.combo_cliente = ttk.Combobox(filtro_frame, state="readonly", width=20)
        self.combo_cliente.grid(row=0, column=5, padx=4, pady=4)

        self.btn_filtrar = tk.Button(filtro_frame, text="Filtrar", command=self.filtrar)
        ThemeManager.style_button(self.btn_filtrar)
        self.btn_filtrar.grid(row=0, column=6, padx=10)

        # Treeview
        cols = ("cliente", "data", "itens", "total")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=14)
        for c in cols:
            self.tree.heading(c, text=c.capitalize())
            self.tree.column(c, width=150 if c != "itens" else 280, anchor="w")
        ThemeManager.style_treeview(self.tree)
        self.tree.pack(fill="both", expand=True, padx=12, pady=10)

        scroll = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scroll.set)
        scroll.pack(side="right", fill="y")

        btn_frame = tk.Frame(self, bg=BG())
        btn_frame.pack(pady=10)
        self.btn_csv = tk.Button(btn_frame, text="Exportar CSV", command=self.exportar_csv)
        self.btn_pdf = tk.Button(btn_frame, text="Exportar PDF", command=self.exportar_pdf)
        ThemeManager.style_button(self.btn_csv)
        ThemeManager.style_button(self.btn_pdf)
        self.btn_csv.pack(side="left", padx=8)
        self.btn_pdf.pack(side="left", padx=8)

        self.lbl_status = tk.Label(self, text="", bg=BG(), fg=HI(), font=SMALL_FONT)
        self.lbl_status.pack(pady=4)

    def carregar_clientes(self):
        try:
            conn = sqlite3.connect(self.db_path)
            cur = conn.cursor()
            cur.execute("SELECT nome FROM clientes ORDER BY nome")
            nomes = [row[0] for row in cur.fetchall()]
            self.combo_cliente["values"] = ["Todos"] + nomes
            self.combo_cliente.set("Todos")
        except Exception as e:
            self.lbl_status.config(text=f"Erro clientes: {e}")
            logging.error(f"Erro ao carregar clientes: {e}")
        finally:
            try:
                conn.close()
            except Exception:
                pass

    def filtrar(self):
        self.tree.delete(*self.tree.get_children())
        try:
            data_ini = self.entry_data_ini.get().strip()
            data_fim = self.entry_data_fim.get().strip()
            cliente = self.combo_cliente.get()

            conn = sqlite3.connect(self.db_path)
            cur = conn.cursor()

            query = """
            SELECT c.nome, p.data, GROUP_CONCAT(ip.produto || ' (Qtd:' || ip.quantidade || ')', ', '), p.total
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

            cur.execute(query, params)
            rows = cur.fetchall()
            for nome, data, itens, total in rows:
                self.tree.insert("", "end", values=(nome, data, itens or "-", f"R$ {total:.2f}"))
            self.lbl_status.config(text=f"{len(rows)} registro(s) encontrado(s).")
            logging.info("Filtro realizado com sucesso.")
        except Exception as e:
            logging.error(f"Erro ao filtrar pedidos: {e}")
            self.lbl_status.config(text=f"Erro ao filtrar: {e}")
        finally:
            try:
                conn.close()
            except Exception:
                pass

    def exportar_csv(self):
        try:
            file = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV","*.csv")])
            if not file:
                return
            with open(file, "w", newline="", encoding="utf-8") as f:
                w = csv.writer(f)
                w.writerow(["Cliente", "Data", "Itens", "Total"])
                for row in self.tree.get_children():
                    w.writerow(self.tree.item(row)["values"])
            logging.info(f"Exportado CSV: {file}")
            self.lbl_status.config(text=f"CSV gerado: {os.path.basename(file)}")
            try:
                os.startfile(file)
            except Exception:
                pass
        except Exception as e:
            logging.error(f"Erro CSV: {e}")
            self.lbl_status.config(text=f"Erro CSV: {e}")

    def exportar_pdf(self):
        try:
            file = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF","*.pdf")])
            if not file:
                return
            c = canvas.Canvas(file, pagesize=letter)
            width, height = letter
            c.setFont("Helvetica-Bold", 14)
            c.drawString(30, height - 40, "Relatório de Pedidos")
            c.setFont("Helvetica", 9)
            y = height - 70
            for row in self.tree.get_children():
                cliente, data, itens, total = self.tree.item(row)["values"]
                c.drawString(30, y, f"Cliente: {cliente}")
                c.drawString(200, y, f"Data: {data}")
                c.drawString(300, y, f"Itens: {str(itens)[:55]}")
                c.drawString(520, y, f"{total}")
                y -= 14
                if y < 60:
                    c.showPage()
                    y = height - 60
            c.save()
            logging.info(f"Exportado PDF: {file}")
            self.lbl_status.config(text=f"PDF gerado: {os.path.basename(file)}")
            try:
                os.startfile(file)
            except Exception:
                pass
        except Exception as e:
            logging.error(f"Erro PDF: {e}")
            self.lbl_status.config(text=f"Erro PDF: {e}")