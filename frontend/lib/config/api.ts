/**
 * Configurações de API - MÓDULO ÚNICO DE RESOLUÇÃO DE URL
 * 
 * REFATORAÇÃO DRY: Este arquivo é a única fonte de verdade para
 * resolução de URL da API. O gameApi.ts importa daqui.
 * 
 * Centraliza detecção de ambiente e resolução de URLs.
 * 
 * GRASP - Pure Fabrication: Utilitário de configuração
 */

import { DEFAULT_API_URL } from '@/types/game'

/**
 * Detecta se está executando em GitHub Codespaces
 */
export function isCodespace(): boolean {
  if (typeof window === 'undefined') return false
  return window.location.hostname.includes('app.github.dev')
}

/**
 * Retorna a URL base do backend
 * 
 * REFATORAÇÃO DRY: Lógica centralizada, usada por gameApi.ts e hooks legados.
 * 
 * Suporta:
 * - GitHub Codespaces (traduz porta automaticamente)
 * - Ambiente local (localhost:8000)
 * - Variável de ambiente NEXT_PUBLIC_API_URL
 * 
 * @param port - Porta do backend (padrão: 8000)
 * @returns URL base do backend
 */
export function getBackendUrl(port: string = '8000'): string {
  // 1. Verifica variável de ambiente primeiro (prioridade máxima)
  const envUrl = process.env.NEXT_PUBLIC_API_URL
  if (envUrl && envUrl.length > 0) {
    return envUrl
  }

  // 2. Suporte para GitHub Codespaces (client-side)
  if (typeof window !== 'undefined' && isCodespace()) {
    const baseUrl = window.location.hostname.replace(/-300[0-9]/, `-${port}`)
    return `${window.location.protocol}//${baseUrl}`
  }

  // 3. Fallback para localhost ou DEFAULT_API_URL
  return DEFAULT_API_URL || `http://localhost:${port}`
}

/**
 * Alias para compatibilidade - usado por gameApi.ts
 * 
 * @deprecated Use getBackendUrl() diretamente
 */
export const resolveApiBaseUrl = getBackendUrl
