import sqlite3
from sqlite3 import Error

DB_NAME = "app.db"

# --------------------------------------------------------
# Função para conectar ao banco
# --------------------------------------------------------
def conectar():
    """Cria e retorna uma conexão com o banco de dados SQLite."""
    try:
        conn = sqlite3.connect(DB_NAME)
        return conn
    except Error as e:
        print(f"Erro ao conectar ao banco: {e}")
        return None


# --------------------------------------------------------
# Inicializar banco e criar tabelas
# --------------------------------------------------------
def inicializar_banco():
    """Cria as tabelas se ainda não existirem."""
    conn = conectar()
    if conn is None:
        return

    cursor = conn.cursor()

    try:
        cursor.executescript("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE,
            telefone TEXT
        );

        CREATE TABLE IF NOT EXISTS pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER NOT NULL,
            data TEXT NOT NULL,
            total REAL NOT NULL,
            FOREIGN KEY (cliente_id) REFERENCES clientes(id)
        );

        CREATE TABLE IF NOT EXISTS itens_pedido (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pedido_id INTEGER NOT NULL,
            produto TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            preco_unit REAL NOT NULL,
            FOREIGN KEY (pedido_id) REFERENCES pedidos(id)
        );
        """)
        conn.commit()
        print("Banco inicializado com sucesso!")
    except Error as e:
        print(f"Erro ao criar tabelas: {e}")
    finally:
        conn.close()


# --------------------------------------------------------
# Função genérica para executar comandos INSERT, UPDATE, DELETE
# --------------------------------------------------------
def executar_comando(sql, params=()):
    """Executa um comando SQL (INSERT, UPDATE, DELETE) de forma segura."""
    conn = conectar()
    if conn is None:
        return False

    try:
        cursor = conn.cursor()
        cursor.execute(sql, params)
        conn.commit()
        return True
    except Error as e:
        print(f"Erro ao executar comando: {e}")
        return False
    finally:
        conn.close()


# --------------------------------------------------------
# Função genérica para consultar dados (SELECT)
# --------------------------------------------------------
def consultar(sql, params=()):
    """Executa uma consulta SQL e retorna os resultados."""
    conn = conectar()
    if conn is None:
        return []

    try:
        cursor = conn.cursor()
        cursor.execute(sql, params)
        resultados = cursor.fetchall()
        return resultados
    except Error as e:
        print(f"Erro ao consultar dados: {e}")
        return []
    finally:
        conn.close()


# --------------------------------------------------------
# Exemplo de uso direto (para testes)
# --------------------------------------------------------
if __name__ == "__main__":
    inicializar_banco()

    # Inserir cliente de teste
    executar_comando(
        "INSERT INTO clientes (nome, email, telefone) VALUES (?, ?, ?)",
        ("Maria Souza", "maria@email.com", "1199999999")
    )

    # Buscar clientes
    clientes = consultar("SELECT * FROM clientes")
    for c in clientes:
        print(c)
