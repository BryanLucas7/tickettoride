# 🚂 Como Rodar o Projeto Ticket to Ride

## 📋 Pré-requisitos

Antes de rodar o projeto, certifique-se de ter instalado:

- **Node.js** (v18 ou superior)
- **Python** (v3.10 ou superior)
- **npm** (geralmente vem com Node.js)
- **pip** (geralmente vem com Python)

## 🔧 Instalação (Apenas na Primeira Vez)

Execute apenas este comando para instalar **TODAS** as dependências (Node.js + Python):

```bash
npm install
```

Este comando automaticamente instala:
- ✅ Dependências do frontend (React, Next.js, etc.)
- ✅ Dependências do backend (FastAPI, Uvicorn, Python-multipart)

## 🚀 Como Rodar o Projeto

Apenas rode:
```
    npm run dev
```

Este único comando inicia **frontend** (porta 3000) e **backend** (porta 8000) **simultaneamente**! 🎉

## 🌐 URLs de Acesso

- **Frontend (Jogo)**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Documentação API**: http://localhost:8000/docs (Swagger UI automático)

## ⚙️ Comandos Opcionais (Caso Precise)

Se por algum motivo você quiser rodar apenas um dos servidores:

### Apenas Frontend
```bash
npm run dev:frontend
```

### Apenas Backend
```bash
npm run dev:backend
```

## ❓ Por Que Preciso Rodar Duas Coisas?

Este projeto usa uma arquitetura **Full Stack** com:

1. **Frontend (Next.js/React)** 
   - Interface visual do jogo
   - Gerenciado pelo Node.js/npm
   - Porta 3000

2. **Backend (Python/FastAPI)**
   - Lógica do jogo e regras de negócio
   - Gerenciado pelo Python/pip
   - Porta 8000


## 📝 Scripts Disponíveis

| Comando | Descrição |
|---------|-----------|
| `npm install` | Instala TODAS as dependências (Node.js + Python) |
| `npm run dev` | 🌟 **Inicia frontend + backend juntos** |
| `npm run dev:frontend` | Inicia apenas o frontend |
| `npm run dev:backend` | Inicia apenas o backend |
| `npm run build` | Cria build de produção do frontend |
| `npm run start` | Inicia servidor de produção |
| `npm run lint` | Verifica código por erros |

## 🎮 Resumo Rápido

```bash
# 1ª vez - Instalar tudo
npm install

# Sempre que for desenvolver
npm run dev

# Acesse o jogo em:
# http://localhost:3000
```

Pronto! Divirta-se! 🚂🎲✨
