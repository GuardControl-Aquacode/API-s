from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime

# Router do módulo de localização
router = APIRouter(prefix="/api/v1/localizacao", tags=["Geolocalização"])

# Dicionário em memória para guardar as posições atuais
localizacoes_vigilantes: Dict[str, dict] = {}


class LocalizacaoSchema(BaseModel):
    vigilanteId: str
    nome: str
    latitude: float
    longitude: float
    status: Optional[str] = "em_ronda"


@router.post("", status_code=200)
async def atualizar_localizacao(dados: LocalizacaoSchema):
    payload = {
        "vigilanteId": dados.vigilanteId,
        "nome": dados.nome,
        "latitude": dados.latitude,
        "longitude": dados.longitude,
        "status": dados.status,
        "ultimaAtualizacao": datetime.utcnow().isoformat()
    }
    
    localizacoes_vigilantes[dados.vigilanteId] = payload
    
    # Notificação WebSocket enviada no main.py se necessário
    return {"status": "sucesso", "mensagem": "Localização atualizada!", "dados": payload}


@router.get("/ativos")
async def obter_vigilantes_ativos():
    """ Retorna a posição atual de todos os vigilantes ativos """
    return list(localizacoes_vigilantes.values())