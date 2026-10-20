from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# Criamos o router para o módulo de ocorrências
router = APIRouter(prefix="/api/v1/ocorrencias", tags=["Ocorrências"])

# Lista em memória para guardar os registos de ocorrências
ocorrencias_registadas: List[dict] = []

# Modelo de Dados (Schema)
class OcorrenciaSchema(BaseModel):
    vigilanteId: str
    nomeVigilante: str
    tipo: str  # ex: 'panico', 'invasao', 'porta_aberta', 'suspeito'
    descricao: Optional[str] = "Alerta de emergência disparado!"
    latitude: float
    longitude: float
    nivelPrioridade: Optional[str] = "ALTA"  # 'BAIXA', 'MEDIA', 'ALTA', 'CRITICA'


@router.post("", status_code=201)
async def registrar_ocorrencia(dados: OcorrenciaSchema):
    payload_ocorrencia = {
        "id": len(ocorrencias_registadas) + 1,
        "vigilanteId": dados.vigilanteId,
        "nomeVigilante": dados.nomeVigilante,
        "tipo": dados.tipo,
        "descricao": dados.descricao,
        "latitude": dados.latitude,
        "longitude": dados.longitude,
        "nivelPrioridade": dados.nivelPrioridade,
        "dataHora": datetime.utcnow().isoformat(),
        "status": "ABERTA"
    }
    
    ocorrencias_registadas.append(payload_ocorrencia)

    # Nota: A integração com o WebSocket (sio.emit) pode ser chamada aqui para notificar o Painel Web
    return {
        "status": "sucesso",
        "mensagem": "Ocorrência registada com sucesso!",
        "ocorrencia": payload_ocorrencia
    }


@router.get("")
async def listar_ocorrencias():
    """ Retorna a lista de todas as ocorrências registadas """
    return ocorrencias_registadas