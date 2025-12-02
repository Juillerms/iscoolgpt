# ☁️ IsCoolGPT - Cloud Computing AI Assistant

![Python](https://img.shields.io/badge/Python-3.10-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688?style=for-the-badge&logo=fastapi)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?style=for-the-badge&logo=docker)
![AWS](https://img.shields.io/badge/AWS-EC2%20%2B%20CloudWatch-232F3E?style=for-the-badge&logo=amazon-aws)

> **Projeto Final da disciplina de Cloud Computing** > Um assistente inteligente Full-Stack, containerizado e monitorado na nuvem.

---

## 📖 Sobre o Projeto

O **IsCoolGPT** é uma aplicação web moderna projetada para auxiliar estudantes a tirar dúvidas sobre Computação em Nuvem. Diferente de chats comuns, este projeto implementa uma arquitetura **Cloud-Native** robusta, simulando um ambiente de produção real com pipelines de CI/CD, monitoramento de logs e orquestração de containers.

### ✨ Funcionalidades Principais
* 🤖 **Inteligência Artificial:** Integração com **Groq (Llama 3)** para respostas ultra-rápidas e precisas.
* 💻 **Interface High-Tech:** Frontend responsivo com design *Glassmorphism*, modo terminal e renderização de Markdown.
* 🐳 **Containerização:** Aplicação 100% isolada via Docker e Docker Compose.
* 🚀 **CI/CD Automatizado:** Pipeline no GitHub Actions que faz build e deploy automático no servidor.
* 📊 **Observabilidade:** Logs da aplicação enviados em tempo real para o **Amazon CloudWatch**.

---

## 🛠️ Stack Tecnológica

| Componente | Tecnologia | Motivo da Escolha |
|------------|------------|-------------------|
| **Backend** | Python + FastAPI | Alta performance (assíncrono), tipagem forte e fácil manutenção. |
| **Frontend** | HTML/JS (SSR) | Renderização leve no servidor, sem necessidade de build complexo de React/Vue. |
| **AI Engine** | Groq (Llama 3.3) | Baixa latência e limites gratuitos generosos (evita erros de quota). |
| **Infraestrutura** | AWS EC2 | Controle total do SO e persistência de dados. |
| **Logs** | AWS CloudWatch | Centralização de logs e auditoria sem acesso SSH. |
| **DevOps** | GitHub Actions | Automação completa de Build (Docker Hub) e Deploy (EC2). |

---

## 🚀 Como Rodar Localmente

### Pré-requisitos
* [Docker Desktop](https://www.docker.com/) instalado.
* Uma chave de API da [Groq](https://console.groq.com/).

### Passo a Passo

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/SEU_USUARIO/iscoolgpt.git](https://github.com/SEU_USUARIO/iscoolgpt.git)
    cd iscoolgpt
    ```

2.  **Crie o arquivo de configuração:**
    Crie um arquivo chamado `.env` na raiz do projeto e adicione sua chave:
    ```env
    GROQ_API_KEY=sua_chave_gsk_aqui
    ```

3.  **Suba o ambiente com Docker:**
    ```bash
    docker-compose up --build
    ```

4.  **Acesse:**
    Abra o navegador em `http://localhost:8000`.

---

## ☁️ Arquitetura de Deploy (CI/CD)

O projeto utiliza **GitHub Actions** para entrega contínua. O fluxo é dividido em dois workflows:

1.  **Build (`build.yaml`):**
    * Gera a imagem Docker baseada em `python:3.10-slim`.
    * Envia a imagem para o Docker Hub.

2.  **Deploy (`deploy.yaml`):**
    * Conecta-se à instância AWS EC2 via SSH.
    * Atualiza o arquivo `.env` com as *Secrets* do GitHub.
    * Reinicia os containers com a nova versão da imagem.

### Variáveis de Ambiente (GitHub Secrets)
Para o deploy funcionar, as seguintes *Secrets* foram configuradas no repositório:
* `GROQ_API_KEY`: Chave da IA.
* `DOCKER_USERNAME` / `DOCKER_PASSWORD`: Credenciais do Docker Hub.
* `EC2_HOST` / `EC2_USER` / `EC2_SSH_KEY`: Acesso ao servidor AWS.

---

## 📁 Estrutura do Projeto

```plaintext
iscoolgpt/
├── .github/workflows/    # Pipelines de Automação (CI/CD)
│   ├── build.yaml        # Build & Push para Docker Hub
│   └── deploy.yaml       # Deploy para AWS EC2
├── main.py               # Aplicação Backend e Frontend (SSR)
├── Dockerfile            # Definição da Imagem
├── docker-compose.yaml   # Orquestração e Configuração de Logs
├── requirements.txt      # Dependências Python
└── README.md             # Documentação
