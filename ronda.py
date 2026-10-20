from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

router = APIRouter(prefix="/api/v1/rondas", tags=["Gestão de Rondas & Checkpoints"])

# Base de dados temporária em memória
checkpoints_registados: List[dict] = []
rondas_agendadas = [
    {
        "rondaId": "RND-101",
        "nomeRonda": "Ronda Perimetral Setor Norte",
        "vigilanteDesignado": "Henrique Sanda",
        "horarioInicio": "22:00",
        "horarioFim": "02:00",
        "status": "EM_ANDAMENTO",
        "totalCheckpoints": 5,
        "checkpointsConcluidos": 2
    },
    {
        "rondaId": "RND-102",
        "nomeRonda": "Inspeção de Bloco Principal",
        "vigilanteDesignado": "Henrique Sanda",
        "horarioInicio": "03:00",
        "horarioFim": "05:00",
        "status": "PENDENTE",
        "totalCheckpoints": 4,
        "checkpointsConcluidos": 0
    }
]


# --- SCHEMAS (Modelos de Dados) ---

class CheckpointSchema(BaseModel):
    rondaId: str
    vigilanteId: str
    pontoId: str  # ex: 'PONTO-PORTARIA-NORTE'
    nomePonto: str
    latitude: float
    longitude: float
    observacao: Optional[str] = "Ponto verificado sem alterações."


# --- ROTAS REST (HTTP) ---

@router.get("/agendadas", status_code=200)
async def listar_rondas_agendadas():
    """ Retorna a lista de rondas programadas para o turno do vigilante """
    return rondas_agendadas


@router.post("/checkpoint", status_code=201)
async def registrar_checkpoint(dados: CheckpointSchema):
    """
    Regista a leitura de um QR Code / Tag NFC feita pelo vigilante num ponto de controlo.
    """
    payload_checkpoint = {
        "id": len(checkpoints_registados) + 1,
        "rondaId": dados.rondaId,
        "vigilanteId": dados.vigilanteId,
        "pontoId": dados.pontoId,
        "nomePonto": dados.nomePonto,
        "latitude": dados.latitude,
        "longitude": dados.longitude,
        "observacao": dados.observacao,
        "dataHora": datetime.utcnow().isoformat()
    }

    checkpoints_registados.append(payload_checkpoint)

    # Atualiza o progresso da ronda correspondente
    for ronda in rondas_agendadas:
        if ronda["rondaId"] == dados.rondaId:
            ronda["checkpointsConcluidos"] += 1
            if ronda["checkpointsConcluidos"] >= ronda["totalCheckpoints"]:
                ronda["status"] = "CONCLUIDA"

    return {
        "status": "sucesso",
        "mensagem": f"Checkpoint '{dados.nomePonto}' registado com sucesso!",
        "checkpoint": payload_checkpoint
    }


@router.get("/historico/{vigilanteId}", status_code=200)
async def obter_historico_vigilante(vigilanteId: str):
    """
    Retorna todos os checkpoints e registos de travessia do vigilante para desenhar a rota no mapa.
    """
    historico = [c for c in checkpoints_registados if c["vigilanteId"] == vigilanteId]
    return {
        "vigilanteId": vigilanteId,
        "totalCheckpointsRealizados": len(historico),
        "historico": historico
    }