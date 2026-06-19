from fastapi import HTTPException
from logger_config import logger
from tarefa import Tarefa
from database import Database

class GestorTarefas:
    PRIORIDADES = {"Alta": 1, "Média": 2, "Baixa": 3}

    def __init__(self, nome_db="tarefas.db"):
        self.db = Database(nome_db=nome_db)
    
    def contar_tarefas_por_estado(self, estado=None):
        if estado is not None:
            return self.db.contar_tarefas_por_estado(estado)
        else:
            return self.db.contar_tarefas_por_estado()
        
    def verificar_existencia(self, id):
        tarefas = self.listar_tarefas()
        if not any(t.id == id for t in tarefas):
            raise HTTPException(status_code=404, detail=f"Tarefa {id} não encontrada")

    def listar_tarefas(self, estado=None):
        if estado is not None:
            resultado_db = self.db.listar_tarefas(estado)
        else:
            resultado_db = self.db.listar_tarefas()
        
        tarefas = [Tarefa.from_dict(t) for t in resultado_db]

        return tarefas
    
    def obter_tarefa(self, id):
        resultado_db = self.db.obter_tarefa(id)
        if resultado_db is None:
            return None
        return Tarefa.from_dict(resultado_db)
    
    def adicionar_tarefa(self, titulo, prioridade):
        if prioridade not in ["Alta", "Média", "Baixa"]:
            raise ValueError("Prioridade inválida")
        
        nova_tarefa = Tarefa(titulo, prioridade)

        logger.info(f"A adicionar tarefa: {titulo} ({prioridade})")

        self.db.inserir_tarefa(nova_tarefa.titulo, nova_tarefa.prioridade, nova_tarefa.data_criacao, nova_tarefa.estado)

    def remover_tarefa(self, id):
        logger.info(f"A remover tarefa {id}")
        self.db.remover_tarefa(id)
    
    def marcar_tarefa_concluida(self, id):
        logger.info(f"A marcar tarefa {id} como concluída")
        self.db.atualizar_tarefa(id, novo_estado="Concluída")

    def editar_tarefa(self, id, novo_titulo=None, nova_prioridade=None):
        if novo_titulo is None and nova_prioridade is None:
            return

        self.db.atualizar_tarefa(
            id,
            novo_titulo=novo_titulo,
            nova_prioridade=nova_prioridade
        )
    
    def fechar_ligacao(self):
        self.db.fechar_ligacao()
