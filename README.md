# ⚙️ GuardControl - API Central & Integrações (Back-end)

Este repositório contém a **API Central** da plataforma **GuardControl**, desenvolvida para orquestrar a comunicação entre as aplicações Web/Mobile, gerir o banco de dados e fornecer serviços em tempo real via WebSockets.

---

## 🛠️ Tecnologias Utilizadas

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![Socket.io](https://img.shields.io/badge/Socket.io-010101?style=for-the-badge&logo=socketdotio&logoColor=white)
![Uvicorn](https://img.shields.io/badge/Uvicorn-499885?style=for-the-badge&logo=uvicorn&logoColor=white)

---

## 🚀 Funcionalidades do Back-end

* **Comunicação REST:** Endpoints para operações CRUD de utilizadores, registo de rondas, pontos de controlo e ocorrências.
* **Transmissão em Tempo Real (WebSockets):** Conexão ativa via `python-socketio` para envio contínuo das coordenadas GPS dos vigilantes para o mapa da central.
* **Arquitetura Modular:** Separação de rotas utilizando `APIRouter` do FastAPI.
* **Validação de Dados:** Utilização de modelos Pydantic para garantir integridade das requisições e respostas.
* **Documentação Automática:** Endpoints mapeados automaticamente via Swagger UI e ReDoc.

---

## 📂 Estrutura das Rotas da API

| Módulo | Ficheiro | Função |
| :--- | :--- | :--- |
| **Autenticação** | `usuarios.py` | Gestão de perfis de acesso, login e utilizadores. |
| **Geolocalização** | `localizacao.py` | Receção e retransmissão de coordenadas GPS em tempo real. |
| **Ocorrências** | `ocorrencias.py` | Registo de emergências e disparos do botão de pânico. |
| **Rondas** | `rondas.py` | Validação de checkpoints (QR Code/NFC) e estado das rotas. |
| **Dashboard** | `dashboard.py` | Métricas agregadas e consolidação de dados para o painel web. |
| **Notificações** | `notificacoes.py` | Envio de avisos da central para a aplicação dos vigilantes. |

---

## ⚙️ Como Executar a API Localmente

### Pré-requisitos
* Python 3.10 ou superior.

### 1. Clonar o repositório

---

## 👥 Responsáveis pelo Back-end & API

* **Gabriel Schmidt** — *Redes & DevOps*
  * [![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=flat-square&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/gabrielschimidtt/)

* **Henrique Sanda Nitsche** — *Engenheiro de Software & Desenvolvedor Back-end*
  * [![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=flat-square&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/hsnitsche)
---bash
