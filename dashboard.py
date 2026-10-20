from fastapi import APIRouter
from typing import Dict, List
from datetime import datetime

router = APIRouter(prefix="/api/v1/dashboard", tags=["Dashboard & Relatórios"])


@router.get("/resumo", status_code=200)
async def obter_resumo_dashboard():
    """ Retorna os indicadores principais (KPIs) para os cartões do Dashboard Web """
    return {
        "dataHoraConsulta": datetime.utcnow().isoformat(),
        "kpis": {
            "vigilantesEmRonda": 8,
            "vigilantesInativos": 2,
            "totalOcorrenciasHoje": 3,
            "ocorrenciasCriticasPendentes": 1,
            "rondasConcluidasHoje": 14,
            "taxaCoberturaPatrulhamento": "94%"
        }
    }


@router.get("/ocorrencias-por-tipo", status_code=200)
async def obter_ocorrencias_por_tipo():
    """ Retorna a contagem de ocorrências por categoria para gráficos """
    return [
        {"tipo": "Botão de Pânico", "quantidade": 2},
        {"tipo": "Invasão / Suspeito", "quantidade": 1},
        {"tipo": "Porta / Portão Aberto", "quantidade": 5},
        {"tipo": "Iluminação / Avaria", "quantidade": 3}
    ]


@router.get("/desempenho-rondas", status_code=200)
async def obter_desempenho_rondas():
    """ Retorna o volume de rondas realizadas ao longo dos dias """
    return [
        {"dia": "Seg", "concluidas": 18, "canceladas": 1},
        {"dia": "Ter", "concluidas": 22, "canceladas": 0},
        {"dia": "Qua", "concluidas": 20, "canceladas": 2},
        {"dia": "Qui", "concluidas": 25, "canceladas": 1},
        {"dia": "Sex", "concluidas": 24, "canceladas": 0}
    ]