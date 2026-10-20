from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

router = APIRouter(prefix="/api/v1/usuarios", tags=["Autenticação & Usuários"])

# Base de dados simulada em memória
usuarios_db = [
    {
        "id": "USR-001",
        "nome": "Henrique Sanda",
        "email": "henrique@guardcontrol.com",
        "senha": "123",  # Em produção, utilizar hash (ex: bcrypt)
        "cargo": "vigilante",  # 'vigilante' ou 'gestor'
        "ativo": True,
        "turno": "Noite"
    },
    {
        "id": "USR-002",
        "nome": "Gestor Central",
        "email": "admin@guardcontrol.com",
        "senha": "admin",
        "cargo": "gestor",
        "ativo": True,
        "turno": "Integral"
    }
]


# --- SCHEMAS (Modelos de Dados) ---

class LoginSchema(BaseModel):
    email: str
    senha: str

class UsuarioCriarSchema(BaseModel):
    nome: str
    email: str
    senha: str
    cargo: Optional[str] = "vigilante"
    turno: Optional[str] = "Dia"


# --- ROTAS REST (HTTP) ---

@router.post("/login", status_code=200)
async def login(dados: LoginSchema):
    """
    Valida as credenciais do utilizador e retorna os dados de sessão.
    """
    usuario = next((u for u in usuarios_db if u["email"] == dados.email and u["senha"] == dados.senha), None)
    
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou palavra-passe incorretos."
        )
    
    if not usuario["ativo"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Utilizador inativo no sistema."
        )

    return {
        "status": "sucesso",
        "mensagem": "Login efetuado com sucesso!",
        "token": f"fake-jwt-token-{usuario['id']}",
        "usuario": {
            "id": usuario["id"],
            "nome": usuario["nome"],
            "email": usuario["email"],
            "cargo": usuario["cargo"],
            "turno": usuario["turno"]
        }
    }


@router.get("", status_code=200)
async def listar_usuarios():
    """ Retorna a lista de todos os utilizadores registados """
    # Remove o campo senha por segurança antes de retornar
    return [{k: v for k, v in u.items() if k != "senha"} for u in usuarios_db]


@router.post("", status_code=201)
async def criar_usuario(dados: UsuarioCriarSchema):
    """ Regista um novo utilizador no sistema """
    if any(u["email"] == dados.email for u in usuarios_db):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este e-mail já está registado."
        )

    novo_usuario = {
        "id": f"USR-00{len(usuarios_db) + 1}",
        "nome": dados.nome,
        "email": dados.email,
        "senha": dados.senha,
        "cargo": dados.cargo,
        "ativo": True,
        "turno": dados.turno
    }

    usuarios_db.append(novo_usuario)
    return {
        "status": "sucesso",
        "mensagem": "Utilizador registado com sucesso!",
        "usuario": {k: v for k, v in novo_usuario.items() if k != "senha"}
    }