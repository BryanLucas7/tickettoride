# 🚂 Ticket to Ride - Edição Brasil

[![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Next.js](https://img.shields.io/badge/Next.js-000000?style=for-the-badge&logo=next.js&logoColor=white)](https://nextjs.org/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)

## 📖 Sobre o Projeto

Este projeto é um trabalho acadêmico da disciplina de **Projeto de Software** que implementa uma versão digital do jogo de tabuleiro **Ticket to Ride**, adaptada para o contexto brasileiro. O jogo apresenta um mapa do Brasil com rotas entre cidades brasileiras, mantendo a mecânica original do jogo mas com uma identidade nacional.

### 🎯 Objetivos Acadêmicos

- Aplicar **princípios GRASP** no design de software
- Implementar **padrões de projeto GoF** (Gang of Four)
- Criar uma aplicação web interativa e responsiva
- Aplicar boas práticas de engenharia de software

---

## 🏗️ Arquitetura do Projeto

O projeto segue uma arquitetura **Full Stack** moderna:

### **Frontend**
- **Framework:** Next.js 14 (React)
- **Linguagem:** TypeScript
- **Estilização:** Tailwind CSS
- **Componentização:** Componentes reutilizáveis e modulares

### **Backend**
- **Framework:** FastAPI (Python)
- **Arquitetura:** REST API
- **Lógica de Negócio:** Implementação completa das regras do jogo

---

## 🎨 Padrões de Design Aplicados

Este projeto implementa rigorosamente princípios e padrões de design de software para garantir código limpo, manutenível e extensível.

### 📐 Princípios GRASP

Os **9 princípios GRASP** (General Responsibility Assignment Software Patterns) foram aplicados:

1. **Information Expert** - Atribuição de responsabilidades baseada em especialização de informação
2. **Creator** - Definição clara de quem cria quais objetos
3. **Controller** - Controladores para orquestrar casos de uso
4. **Low Coupling** - Baixo acoplamento entre módulos
5. **High Cohesion** - Alta coesão dentro de cada classe/módulo
6. **Polymorphism** - Uso de polimorfismo para comportamentos variáveis
7. **Pure Fabrication** - Classes de serviço que não representam conceitos do domínio
8. **Indirection** - Uso de intermediários para reduzir acoplamento direto
9. **Protected Variations** - Proteção contra variações através de interfaces estáveis


### 🔧 Padrões GoF (Gang of Four)

Os seguintes **padrões de projeto GoF** foram implementados:

1. **Strategy Pattern** - Estratégias de validação de rotas (coloridas vs. cinzas)
2. **Observer Pattern** - Sistema de notificação de eventos do jogo
3. **Template Method Pattern** - Fluxo de ações de turno padronizado
4. **Singleton Pattern** - Gerenciamento único da instância do jogo
5. **Factory Method Pattern** - Criação de baralhos e cartas
6. **State Pattern** - Gerenciamento de estados do turno

### ✅ Verificação de Conformidade

O projeto foi verificado quanto à implementação correta de todos os princípios e padrões:

- 📋 **[Checklist de Verificação](docs/CHECKLIST_VERIFICACAO.md)** - Análise detalhada da implementação
  - ✅ **GRASP:** 9/9 princípios (100%)
  - ✅ **GoF:** 6/6 padrões (100%)

---

## 🚀 Como Rodar o Projeto

### 📋 Pré-requisitos

Certifique-se de ter instalado:

- **Node.js** (v18 ou superior)
- **Python** (v3.10 ou superior)
- **npm** (geralmente vem com Node.js)
- **pip** (geralmente vem com Python)

### 🔧 Instalação

Execute apenas um comando para instalar **todas** as dependências:

```bash
npm install
```

Este comando instala automaticamente:
- ✅ Dependências do frontend (React, Next.js, Tailwind CSS, etc.)
- ✅ Dependências do backend (FastAPI, Uvicorn, Python-multipart, etc.)

### ▶️ Executando o Projeto

Inicie **frontend** e **backend** simultaneamente com um único comando:

```bash
npm run dev
```

### 🌐 URLs de Acesso

Após iniciar o projeto, acesse:

- **🎮 Jogo (Frontend)**: http://localhost:3000
- **🔌 API (Backend)**: http://localhost:8000
- **📖 Documentação da API**: http://localhost:8000/docs (Swagger UI)

### ⚙️ Comandos Alternativos

Se precisar rodar os servidores separadamente:

```bash
# Apenas Frontend
npm run dev:frontend

# Apenas Backend
npm run dev:backend
```

### 📝 Scripts Disponíveis

| Comando | Descrição |
|---------|-----------|
| `npm install` | Instala todas as dependências (Node.js + Python) |
| `npm run dev` | 🌟 **Inicia frontend + backend juntos** |
| `npm run dev:frontend` | Inicia apenas o frontend (porta 3000) |
| `npm run dev:backend` | Inicia apenas o backend (porta 8000) |
| `npm run build` | Cria build de produção do frontend |
| `npm run start` | Inicia servidor de produção |
| `npm run lint` | Verifica código por erros |

---
