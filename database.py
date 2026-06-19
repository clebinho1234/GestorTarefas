import sqlite3

class Database:
    def __init__(self, nome_db):
        self.conn = sqlite3.connect(nome_db, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._criar_tabela()

    def _criar_tabela(self):
        query = """
        CREATE TABLE IF NOT EXISTS tarefas(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL UNIQUE,
            prioridade TEXT NOT NULL,
            data_criacao TEXT NOT NULL,
            estado TEXT NOT NULL
        )
        """

        cursor = self.conn.cursor()
        cursor.execute(query)

        self.conn.commit()

    def contar_tarefas_por_estado(self, estado=None):
        cursor = self.conn.cursor()

        if estado is None:
            cursor.execute("SELECT COUNT(*) FROM tarefas")
        else:
            cursor.execute("SELECT COUNT(*) FROM tarefas WHERE estado = ?", (estado,))

        return cursor.fetchone()[0]

    def listar_tarefas(self, estado=None):
        cursor = self.conn.cursor()
        valores =[]

        query = """SELECT * FROM tarefas"""

        if estado is not None:
            query += """ WHERE estado = ?"""
            valores.append(estado)
        
        query += """
        ORDER BY 
            CASE prioridade
                WHEN 'Alta' THEN 1
                WHEN 'Média' THEN 2
                WHEN 'Baixa' THEN 3
            END
        """

        cursor.execute(query, valores)
        return cursor.fetchall()
    
    def obter_tarefa(self, id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM tarefas WHERE id = ?", (id,))
        return cursor.fetchone()

    def inserir_tarefa(self, titulo, prioridade, data_criacao, estado):
        query = """
        INSERT INTO tarefas (titulo, prioridade, data_criacao, estado) 
        VALUES (?,?,?,?)
        """

        cursor = self.conn.cursor()
        cursor.execute(query, (titulo, prioridade, data_criacao, estado))

        self.conn.commit()

    def remover_tarefa(self, id):
        query = """
        DELETE FROM tarefas WHERE id = ?
        """

        cursor = self.conn.cursor()
        cursor.execute(query, (id,))

        self.conn.commit()

    def atualizar_tarefa(self, id, novo_titulo=None, nova_prioridade=None, novo_estado=None):
        campos = []
        valores = []

        print(f"{nova_prioridade}, {novo_titulo}")

        if novo_titulo is not None:
            campos.append("titulo = ?")
            valores.append(novo_titulo)

        if nova_prioridade is not None:
            campos.append("prioridade = ?")
            valores.append(nova_prioridade)

        if novo_estado is not None:
            campos.append("estado = ?")
            valores.append(novo_estado)

        if not campos:
            return

        query =f"""
        UPDATE tarefas
        SET {', '.join(campos)}
        WHERE id = ?
        """

        valores.append(id)

        cursor = self.conn.cursor()
        cursor.execute(query, valores)
        self.conn.commit()

    def fechar_ligacao(self):
        self.conn.close()
