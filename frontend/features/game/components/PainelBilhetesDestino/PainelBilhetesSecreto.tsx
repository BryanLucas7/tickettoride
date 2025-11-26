/**
 * PainelBilhetesSecreto - Modo secreto do painel de bilhetes
 * 
 * Responsabilidade única: Exibir versão oculta dos bilhetes
 */

'use client';

interface PainelBilhetesSecretoProps {
  jogadorNome: string;
  totalBilhetes: number;
}

export function PainelBilhetesSecreto({ jogadorNome, totalBilhetes }: PainelBilhetesSecretoProps) {
  return (
    <div className="bg-gradient-to-br from-amber-50 to-yellow-100 rounded-lg shadow-md p-4 border-2 border-amber-300">
      <div className="flex items-center gap-2">
        <span className="text-2xl">🎫</span>
        <div>
          <h3 className="font-bold text-amber-900">Bilhetes de Destino</h3>
          <p className="text-sm text-amber-700">
            {jogadorNome} possui {totalBilhetes} bilhetes secretos
          </p>
        </div>
        <div className="ml-auto">
          <span className="text-3xl">🔒</span>
        </div>
      </div>
    </div>
  );
}
