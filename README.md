# 💼 Sistema de Clientes e Pedidos (Tkinter + SQLite)

Um sistema de gestão simples e funcional desenvolvido em **Python** com **Tkinter** e **SQLite**, que permite cadastrar clientes, registrar pedidos e gerenciar itens de forma integrada — tudo em uma interface amigável e intuitiva.

---

## 🧱 **Recursos Principais**

✅ **Clientes**
- Cadastro e edição de clientes  
- Validação de nome, e-mail e telefone  
- Busca por nome ou e-mail  
- Exclusão com confirmação  

✅ **Pedidos**
- Seleção de cliente por lista  
- Data automática (data atual)  
- Adição e remoção de itens (produto, quantidade, preço)  
- Cálculo automático do total  
- Armazenamento transacional (tabelas `pedidos` e `itens_pedido`)  
- Listagem de pedidos com busca e visualização de itens  

✅ **Interface e UX**
- Interface responsiva com **Tkinter + ttk.Treeview**  
- Janelas modais (`Toplevel`) para formulários  
- Confirmações antes de exclusões e fechamento  
- Mensagens amigáveis ao usuário (`messagebox`)  
- Logs automáticos de erros em `erros.log`  
- Validações simples e feedback visual  

---

## 🗂️ **Estrutura do Projeto**

sistema_clientes_pedidos/
│
├── db.py # Criação e manipulação do banco SQLite
├── form_cliente.py # Formulário para cadastro/edição de clientes
├── frame_clientes.py # Frame principal para listar e gerenciar clientes
├── form_pedido.py # Janela para criação de pedidos e itens
├── frame_pedidos.py # Frame principal para listar pedidos
├── main.py # Arquivo principal (interface e menus)
└── README.md # Este arquivo


---

## 🧩 **Banco de Dados (SQLite)**

### Esquema:

**Tabela `clientes`**
| Campo | Tipo | Descrição |
|-------|------|------------|
| id | INTEGER (PK) | Identificador único |
| nome | TEXT | Nome do cliente (obrigatório) |
| email | TEXT | E-mail único (opcional) |
| telefone | TEXT | Telefone (8–15 dígitos) |

**Tabela `pedidos`**
| Campo | Tipo | Descrição |
|-------|------|------------|
| id | INTEGER (PK) | Identificador do pedido |
| cliente_id | INTEGER (FK) | Cliente associado |
| data | TEXT | Data do pedido |
| total | REAL | Valor total do pedido |

**Tabela `itens_pedido`**
| Campo | Tipo | Descrição |
|-------|------|------------|
| id | INTEGER (PK) | Identificador do item |
| pedido_id | INTEGER (FK) | Pedido relacionado |
| produto | TEXT | Nome do produto |
| quantidade | INTEGER | Quantidade comprada |
| preco_unit | REAL | Preço unitário |

---

## ⚙️ **Como Executar o Projeto**

### 1️⃣ Instale o Python (3.10+)
Baixe e instale o [Python](https://www.python.org/downloads/).  
Durante a instalação, marque a opção **“Add Python to PATH”**.

### 2️⃣ Crie um ambiente virtual (opcional, mas recomendado)
```bash
python -m venv venv


Ative o ambiente:

Windows: venv\Scripts\activate

Linux/macOS: source venv/bin/activate

3️⃣ Instale dependências (se houver)

O projeto usa apenas bibliotecas padrão do Python, não requer pacotes externos.
Mas se desejar adicionar relatórios (futuros), poderá instalar:

pip install matplotlib

4️⃣ Execute o sistema

No terminal (dentro da pasta do projeto):

python main.py


O sistema criará automaticamente o arquivo app.db (banco SQLite) na primeira execução.

🧠 Uso Básico

Menu “Clientes”

➕ Novo Cliente: abre um formulário para cadastrar um novo cliente.

📋 Listar Clientes: mostra uma tabela com todos os clientes, com busca e opções de editar/excluir.

Menu “Pedidos”

➕ Novo Pedido: permite selecionar um cliente, adicionar produtos, definir quantidades e salvar o pedido.

📋 Listar Pedidos: exibe todos os pedidos cadastrados, com opção de visualizar os itens ou excluir.

Sair

❌ Fecha o sistema com confirmação para evitar perda de dados.

🧰 Validações

Nome: obrigatório

E-mail: precisa conter “@” e “.” (formato simples)

Telefone: apenas números (8 a 15 dígitos)

Pedido: precisa ter pelo menos 1 item antes de salvar

Mensagens de erro e confirmação são exibidas via messagebox.

🪵 Logs

Todos os erros inesperados são registrados no arquivo:

erros.log


com data, traceback e contexto.

🧑‍💻 Autor

Desenvolvido por: [Seu Nome Aqui]
💬 Contato: seuemail@exemplo.com

📅 Versão: 1.0
📘 Licença: MIT

💡 Próximas Melhorias (sugestões)

🔎 Filtros avançados por data/cliente nos pedidos

📈 Relatórios e gráficos de vendas (matplotlib)

📦 Exportação para CSV ou PDF

🌐 Interface Web (Flask ou FastAPI + SQLite)

✨ Divirta-se explorando e expandindo o sistema!


---

Deseja que eu adicione um **print (captura de tela)** da interface principal no README (gerado via DALL·E ou manualmente)?  
Isso deixa o projeto mais profissional para GitHub ou portfólio.