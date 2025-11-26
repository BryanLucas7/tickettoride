/**
 * JogadorForm - Formulário individual para configurar um jogador
 * 
 * Responsabilidade única: Renderizar campos de nome e cor de um jogador
 * 
 * Extraído de setup/page.tsx para seguir SRP
 */

'use client';

import type { JogadorSetup, CorJogador } from '@/hooks/usePlayerSetup';

interface JogadorFormProps {
  jogador: JogadorSetup;
  index: number;
  coresDisponiveis: readonly CorJogador[];
  onUpdate: (index: number, campo: keyof JogadorSetup, valor: string) => void;
  onRemove: (index: number) => void;
  podeRemover: boolean;
  corEmUso: (cor: CorJogador, indexAtual?: number) => boolean;
}

export function JogadorForm({
  jogador,
  index,
  coresDisponiveis,
  onUpdate,
  onRemove,
  podeRemover,
  corEmUso
}: JogadorFormProps) {
  return (
    <div className="flex gap-3 items-center p-4 bg-gray-50 rounded-lg">
      {/* Campo Nome */}
      <div className="flex-1">
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Jogador {index + 1}
        </label>
        <input
          type="text"
          value={jogador.nome}
          onChange={(e) => onUpdate(index, "nome", e.target.value)}
          placeholder="Nome do jogador"
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>
      
      {/* Campo Cor */}
      <div className="w-40">
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Cor
        </label>
        <select
          value={jogador.cor}
          onChange={(e) => onUpdate(index, "cor", e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          {coresDisponiveis.map((cor) => {
            const corJaUsada = corEmUso(cor, index);
            return (
              <option key={cor} value={cor} disabled={corJaUsada}>
                {cor} {corJaUsada ? "(em uso)" : ""}
              </option>
            );
          })}
        </select>
      </div>
      
      {/* Botão Remover */}
      {podeRemover && (
        <button
          onClick={() => onRemove(index)}
          className="mt-6 px-3 py-2 text-red-600 hover:bg-red-50 rounded-md transition-colors"
        >
          Remover
        </button>
      )}
    </div>
  );
}
