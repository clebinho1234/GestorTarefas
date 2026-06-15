import pytest
from gestor_tarefas import GestorTarefas

@pytest.fixture
def gestor():
    gestor = GestorTarefas(":memory:")
    yield gestor
    gestor.fechar_ligacao()

def adicionar_tarefa_aux(gestor):
    gestor.adicionar_tarefa("Teste", "Alta")
    return gestor.listar_tarefas()[0]

def test_adicionar_tarefa(gestor):
    gestor.adicionar_tarefa("Teste Adicionar", "Alta")

    tarefas = gestor.listar_tarefas()
    assert len(tarefas) > 0

def test_ordem_prioridade(gestor):
    gestor.adicionar_tarefa("Teste Baixa", "Baixa")
    gestor.adicionar_tarefa("Teste Alta", "Alta")
    gestor.adicionar_tarefa("Teste Media", "Média")

    tarefas = gestor.listar_tarefas()

    assert tarefas[0].prioridade == "Alta"
    assert tarefas[1].prioridade == "Média"
    assert tarefas[2].prioridade == "Baixa"

def test_remover_tarefa(gestor):
    tarefa = adicionar_tarefa_aux(gestor)
    gestor.remover_tarefa(tarefa.id)

    tarefas_novas = gestor.listar_tarefas()
    assert tarefa.id not in [t.id for t in tarefas_novas]

def test_marcar_concluida(gestor):
    tarefa = adicionar_tarefa_aux(gestor)

    gestor.marcar_tarefa_concluida(tarefa.id)

    tarefa_marcada = gestor.listar_tarefas()[0]
    assert tarefa_marcada.estado == "Concluída"

def test_contar_por_estado(gestor):
    gestor.adicionar_tarefa("T1", "Alta")
    gestor.adicionar_tarefa("T2", "Alta")

    tarefa = gestor.listar_tarefas()[0]
    gestor.marcar_tarefa_concluida(tarefa.id)

    assert gestor.contar_tarefas_por_estado("Concluída") == 1
    assert gestor.contar_tarefas_por_estado("Pendente") == 1
    assert gestor.contar_tarefas_por_estado() == 2

def test_editar_tarefa(gestor):
    tarefa = adicionar_tarefa_aux(gestor)

    gestor.editar_tarefa(tarefa.id, "Teste Editar Concluido", "Média")

    tarefa_editada = gestor.listar_tarefas()[0]
    assert tarefa_editada.titulo == "Teste Editar Concluido"
    assert tarefa_editada.prioridade == "Média"

def test_nao_permite_titulo_duplicado(gestor):
    gestor.adicionar_tarefa("Teste", "Alta")
    with pytest.raises(Exception):
        gestor.adicionar_tarefa("Teste", "Alta")

def test_editar_tarefa_inexistente(gestor):
    gestor.editar_tarefa(999, "Novo", "Alta")
    tarefas = gestor.listar_tarefas()
    assert len(tarefas) == 0

def test_prioridade_invalida():
    gestor = GestorTarefas(":memory:")
    with pytest.raises(ValueError):
        gestor.adicionar_tarefa("Teste", "Errada")