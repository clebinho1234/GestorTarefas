from tarefa import Tarefa


def test_criar_tarefa():
    tarefa = Tarefa("Teste", "Alta")

    assert tarefa.titulo == "Teste"
    assert tarefa.prioridade == "Alta"
    assert tarefa.estado == "Pendente"
    assert tarefa.id is None
    assert tarefa.data_criacao is not None

def test_tarefa_to_dict():
    tarefa = Tarefa("Teste To Dict", "Média")
    tarefa_dict = tarefa.to_dict()
    
    assert tarefa_dict["titulo"] == "Teste To Dict"
    assert tarefa_dict["prioridade"] == "Média"
    assert tarefa_dict["estado"] == "Pendente"
    assert tarefa_dict["id"] is None
    assert tarefa_dict["data_criacao"] is not None

def test_tarefa_from_dict():
    dados = {
        "id": 1,
        "titulo": "Teste Dict",
        "prioridade": "Baixa",
        "data_criacao": "01-01-2026, 10:00:00",
        "estado": "Concluída"
    }
    tarefa = Tarefa.from_dict(dados)

    assert tarefa.titulo == "Teste Dict"
    assert tarefa.prioridade == "Baixa"
    assert tarefa.estado == "Concluída"
    assert tarefa.id == 1
    assert tarefa.data_criacao == "01-01-2026, 10:00:00"

def test_marcar_concluida():
    tarefa = Tarefa("Teste Concluida", "Média")
    tarefa.marcar_concluida()

    assert tarefa.estado == "Concluída"

def test_str():
    tarefa = Tarefa("Teste Str", "Média")
    tarefa_str = str(tarefa)

    assert "Teste Str" in tarefa_str
    assert "Média" in tarefa_str
    assert "⏳" in tarefa_str # Pendente

    tarefa.marcar_concluida()
    tarefa_str2 = str(tarefa)

    assert "✅" in tarefa_str2 # Concluída