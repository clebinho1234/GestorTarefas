from datetime import datetime

class Tarefa:
    def __init__(self, titulo, prioridade, data_criacao=None, estado="Pendente", id=None):
        self.id = id
        self.titulo = titulo.strip().title()
        self.prioridade = prioridade
        self.data_criacao = data_criacao if data_criacao else datetime.now().strftime("%d-%m-%Y, %H:%M:%S")
        self.estado = estado

    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "prioridade": self.prioridade,
            "data_criacao": self.data_criacao,
            "estado": self.estado
        }
    
    @classmethod
    def from_dict(cls, dados):
        return cls(
            dados["titulo"],
            dados["prioridade"],
            dados["data_criacao"],
            dados["estado"],
            id=dados["id"]
        )

    def marcar_concluida(self):
        self.estado = "Concluída"

    def __str__(self):
        estado_icone = "✅" if self.estado == "Concluída" else "⏳"
        return f"{self.titulo} | {self.prioridade} | {self.data_criacao} | {estado_icone}"