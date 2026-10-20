from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

router = APIRouter(prefix="/api/v1/notificacoes", tags=["Notificações & Comunicados"])

# Lista temporária em memória para guardar os avisos
notificacoes_enviadas: List[dict] = []


class NotificacaoSchema(BaseModel):
    titulo: str
    mensagem: str
    destinatarioId: Optional[str] = "TODOS"  # 'TODOS' ou o ID de um vigilante específico
    tipo: Optional[str] = "INFORMATIVO"  # 'INFORMATIVO', 'ALERTA', 'URGENTE'


@router.post("/enviar", status_code=201)
async def enviar_notificacao(dados: NotificacaoSchema):
    """
    Dispara um comunicado da Central para a App Mobile dos vigilantes.
    """
    payload_notificacao = {
        "id": len(notificacoes_enviadas) + 1,
        "titulo": dados.titulo,
        "mensagem": dados.mensagem,
        "destinatarioId": dados.destinatarioId,
        "tipo": dados.tipo,
        "dataHora": datetime.utcnow().isoformat(),
        "lida": False
    }

    notificacoes_enviadas.append(payload_notificacao)

    return {
        "status": "sucesso",
        "mensagem": "Notificação enviada com sucesso!",
        "notificacao": payload_notificacao
    }


@router.get("/historico", status_code=200)
async def listar_notificacoes():
    """ Retorna o histórico de todas as notificações enviadas pela central """
    return notificacoes_enviadas