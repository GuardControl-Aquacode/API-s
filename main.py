from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import socketio
import uvicorn

# Importa os módulos/roteadores que criaste
from localizacao import router as localizacao_router
from ocorrencias import router as ocorrencias_router
from dashboard import router as dashboard_router
from usuarios import router as usuarios_router
from ronda import router as rondas_router
from notificacoes import router as notificacoes_router
# Registo do router no FastAPI
# 1. Instância Principal do FastAPI
app = FastAPI(
    title="GuardControl - API Central",
    description="Backend unificado para gestão de geolocalização e ocorrências de segurança",
    version="1.0.0"
)

# Configuração de CORS (Permite que o Front-end comunique com a API sem bloqueios)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Configuração do Servidor WebSocket (Socket.io)
sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')
socket_app = socketio.ASGIApp(sio, app)

# 3. Registo dos Módulos (Routers)
app.include_router(localizacao_router)
app.include_router(ocorrencias_router)
app.include_router(dashboard_router)
app.include_router(usuarios_router)
app.include_router(rondas_router)
app.include_router(notificacoes_router)
# Rota de teste inicial para confirmar que a API está online
# Rota de teste inicial para confirmar que a API está online
@app.get("/")
async def root():
    return {
        "sistema": "GuardControl API",
        "status": "Online",
        "modulos": [
            "Usuários & Autenticação",
            "Geolocalização",
            "Ocorrências & Pânico",
            "Rondas & Checkpoints",
            "Dashboard",
            "Notificações"
        ]
    }

# Eventos Globais de Conexão em Tempo Real
@sio.event
async def connect(sid, environ):
    print(f"🟢 Novo cliente conectado ao Socket.io! ID: {sid}")

@sio.event
async def disconnect(sid):
    print(f"🔴 Cliente desconectado. ID: {sid}")


if __name__ == "__main__":
    # Arranca o servidor unificado apontando para o socket_app
    uvicorn.run("main:socket_app", host="0.0.0.0", port=8000, reload=True)