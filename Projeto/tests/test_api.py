from fastapi.testclient import TestClient
import pytest
from gestor_tarefas import GestorTarefas
from main import app, get_gestor

@pytest.fixture
def client():
    gestor_teste = GestorTarefas(":memory:")

    def override_get_gestor():
        return gestor_teste
    
    app.dependency_overrides[get_gestor] = override_get_gestor

    yield TestClient(app)

    app.dependency_overrides.clear()

def adicionar_tarefa_aux(client):
    client.post("/tarefas", json={
        "titulo": "Teste API",
        "prioridade": "Média"
    })

    response = client.get("/tarefas")
    return response.json()[0]["id"]

def test_get_tarefas(client):
    response = client.get("/tarefas")
    assert response.status_code == 200
    assert response.json() == []

def test_post_tarefas(client, caplog):
    caplog.set_level("INFO")

    response = client.post("/tarefas", json={
        "titulo": "Teste API Adicionar",
        "prioridade": "Média"
    })

    assert response.status_code == 201
    assert any(
        "Tarefa criada com sucesso" in message
        for message in caplog.text.splitlines()
    )

def test_put_tarefas(client):
    tarefa_id = adicionar_tarefa_aux(client)

    response = client.put(f"/tarefas/{tarefa_id}", json={
            "titulo": "Teste Bem Sucedido", 
            "prioridade": "Baixa"
    })

    assert response.status_code == 200

    response = client.get("/tarefas")
    tarefa = response.json()[0]

    assert tarefa["titulo"] == "Teste Bem Sucedido"
    assert tarefa["prioridade"] == "Baixa"

def test_marcar_concluida_api(client):
    tarefa_id = adicionar_tarefa_aux(client)

    response = client.put(f"/tarefas/{tarefa_id}")

    assert response.status_code == 200

    response = client.get("/tarefas")
    tarefa = response.json()[0]

    assert tarefa["estado"] == "Concluída"

def test_delete_tarefa(client):
    tarefa_id = adicionar_tarefa_aux(client)

    response = client.delete(f"/tarefas/{tarefa_id}")

    assert response.status_code == 204

    response = client.get("/tarefas")
    assert len(response.json()) == 0

def test_post_sem_titulo(client):
    response = client.post("/tarefas", json={
        "prioridade": "Alta"
    })
    assert response.status_code == 422

def test_post_nao_permite_titulo_duplicado(client, caplog):
    caplog.set_level("WARNING")

    response = client.post("/tarefas", json={
        "titulo": "Teste API Adicionar",
        "prioridade": "Média"
    })

    response = client.post("/tarefas", json={
        "titulo": "Teste API Adicionar",
        "prioridade": "Média"
    })

    assert response.status_code == 409
    assert response.json()["detail"] == "Título já existe"
    assert "Tentativa de criar tarefa duplicada" in caplog.text

def test_put_id_invalido(client):
    response = client.put("/tarefas/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Tarefa 999 não encontrada"

def test_delete_id_invalido(client):
    response = client.delete("/tarefas/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Tarefa 999 não encontrada"

def test_log_404(client, caplog):
    caplog.set_level("WARNING")

    client.delete("/tarefas/999")

    assert "HTTPException 404 em DELETE /tarefas/999" in caplog.text