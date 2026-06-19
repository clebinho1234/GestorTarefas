from enum import Enum
import sqlite3
import time
from typing import Optional
from fastapi import Body, Depends, FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from gestor_tarefas import GestorTarefas
from logger_config import logger

class PrioridadeEnum(str, Enum):
    alta = "Alta"
    media = "Média"
    baixa = "Baixa"

class TarefaCreate(BaseModel):
    titulo: str
    prioridade: PrioridadeEnum
    
app = FastAPI()

def tarefa_para_dict(tarefa):
    estado_icone = "✅" if tarefa.estado == "Concluída" else "⏳"

    return {
        "id": tarefa.id,
        "titulo": tarefa.titulo,
        "prioridade": tarefa.prioridade,
        "data_criacao": tarefa.data_criacao,
        "estado": estado_icone
    }

app.mount("/static/css", StaticFiles(directory="static/css"), name="static")
app.mount("/static/scripts", StaticFiles(directory="static/scripts"), name="static")
templates = Jinja2Templates(directory="templates")

def get_gestor():
    return GestorTarefas()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()

    try:
        response = await call_next(request)
    except Exception as e:
        logger.error(f"Erro inesperado: {e} em {request.method} {request.url.path}")
        raise

    duration = time.time() - start_time

    if response.status_code < 400:
        logger.info(
            f"{request.method} {request.url.path} "
            f"Status: {response.status_code} "
            f"Tempo: {duration:.4f}s"
        )
    else:
        pass

    return response

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.warning(
        f"HTTPException {exc.status_code} em {request.method} {request.url.path}"
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(name="index.html", request=request)

@app.get("/tarefas")
def listar(gestor: GestorTarefas = Depends(get_gestor)):
    tarefas = gestor.listar_tarefas()
    return [tarefa_para_dict(t) for t in tarefas]

@app.get("/edit/{id}")
def obter(request: Request, id: int, gestor: GestorTarefas = Depends(get_gestor)):
    tarefa = gestor.obter_tarefa(id)
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return templates.TemplateResponse(name="edit.html", request=request, context={"tarefa": tarefa_para_dict(tarefa)})

@app.post("/tarefas", status_code=201)
def criar(
    tarefa: TarefaCreate, 
    gestor: GestorTarefas = Depends(get_gestor)
):
    try:
        gestor.adicionar_tarefa(tarefa.titulo, tarefa.prioridade)
        logger.info("Tarefa criada com sucesso")
    except sqlite3.IntegrityError:
        logger.warning(f"Tentativa de criar tarefa duplicada: {tarefa.titulo}")
        raise HTTPException(status_code=409, detail="Título já existe")
    except Exception as e:
        logger.error(f"Erro inesperado ao criar tarefa: {e}")
        raise HTTPException(status_code=500, detail="Erro interno")
    
    return {"mensagem": "Tarefa criada com sucesso"}

@app.put("/tarefas/{id}")
def editar(
    id: int, 
    tarefa: Optional[TarefaCreate] = Body(default=None), 
    gestor: GestorTarefas = Depends(get_gestor)
):
    gestor.verificar_existencia(id)

    if tarefa is None:
        gestor.marcar_tarefa_concluida(id)
        return {"mensagem": "Tarefa marcada como concluída"}
    
    gestor.editar_tarefa(
        id, 
        novo_titulo=tarefa.titulo, 
        nova_prioridade=tarefa.prioridade
    )

    return {"mensagem": "Tarefa atualizada"}

@app.delete("/tarefas/{id}", status_code=204)
def remover(id: int, gestor: GestorTarefas = Depends(get_gestor)):
    gestor.verificar_existencia(id)
    gestor.remover_tarefa(id)
    logger.info(f"Tarefa {id} removida com sucesso")