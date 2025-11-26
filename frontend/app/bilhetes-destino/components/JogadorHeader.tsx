/**
 * JogadorHeader - Header com informações do jogador atual
 * 
 * Responsabilidade única: Exibir informações do jogador e progresso
 */

'use client';

interface JogadorHeaderProps {
  jogadorNome: string;
  jogadorCor: string;
  jogadorAtualIndex: number;
  totalJogadores: number;
}

export function JogadorHeader({
  jogadorNome,
  jogadorCor,
  jogadorAtualIndex,
  totalJogadores
}: JogadorHeaderProps) {
  const mostrarProgresso = totalJogadores > 1
  const corNormalizada = (jogadorCor || "").toLowerCase()

  return (
    <div className="mb-8">
      <h1 className="text-4xl font-bold text-gray-900 mb-2">
        Escolha seus Bilhetes Destino
      </h1>
      <div className="flex items-center gap-3">
        <div 
          className="w-6 h-6 rounded-full" 
          style={{ backgroundColor: corNormalizada || "#e5e7eb" }}
        />
        <p className="text-xl text-gray-700">
          <span className="font-semibold">{jogadorNome}</span>
          {mostrarProgresso ? (
            <> - Jogador {jogadorAtualIndex + 1} de {totalJogadores}</>
          ) : (
            <span className="ml-1 text-lg text-gray-600">(sua tela)</span>
          )}
        </p>
      </div>
      <p className="text-gray-600 mt-2">
        Selecione <strong>2 ou 3 bilhetes</strong> para manter (mínimo 2, você pode ficar com os 3)
      </p>
    </div>
  );
}
