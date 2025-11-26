# Testes do Frontend

## Configuração

Os arquivos de teste estão preparados para uso com **Vitest** e **Testing Library**.
Para habilitar os testes, siga os passos abaixo:

### 1. Instalar dependências

```bash
npm install -D vitest @testing-library/react @testing-library/jest-dom jsdom @vitejs/plugin-react
```

### 2. Criar arquivo de configuração vitest.config.ts

```typescript
import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    setupFiles: ['./vitest.setup.ts'],
    globals: true,
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './'),
    },
  },
})
```

### 3. Criar vitest.setup.ts

```typescript
import '@testing-library/jest-dom'
```

### 4. Adicionar scripts ao package.json

```json
{
  "scripts": {
    "test": "vitest",
    "test:coverage": "vitest --coverage",
    "test:ui": "vitest --ui"
  }
}
```

### 5. Renomear arquivos de teste

Após a configuração, renomeie os arquivos:

```bash
mv __tests__/hooks/useGameSetup.test.ts.example __tests__/hooks/useGameSetup.test.ts
mv __tests__/components/RotaDetalhes.test.tsx.example __tests__/components/RotaDetalhes.test.tsx
```

### 6. Executar testes

```bash
npm test
```

## Estrutura dos Testes

```
__tests__/
├── hooks/
│   └── useGameSetup.test.ts.example    # Testes do hook de setup
├── components/
│   └── RotaDetalhes.test.tsx.example   # Testes dos componentes de rota
└── README.md                            # Este arquivo
```

## Cobertura de Testes

Os arquivos de exemplo cobrem:

### useGameSetup.test.ts
- Estado inicial do hook
- Criação de jogo com sucesso
- Tratamento de erros de rede
- Tratamento de erros HTTP
- Limpeza de dados anteriores
- Salvamento de dados do jogo

### RotaDetalhes.test.tsx
- RotaConquistada: mensagem de rota já conquistada
- RotaBloqueada: bloqueio por cartas e bilhetes
- RotaAguardando: mensagem de aguardo
- RotaSemCartas: mensagem de falta de cartas
- RotaSelecaoCartas: seleção de cartas e ações
- RotaDetalhesPanel: orquestração de estados
