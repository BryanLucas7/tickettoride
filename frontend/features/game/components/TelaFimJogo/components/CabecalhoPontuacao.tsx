/**
 * CabecalhoPontuacao - Cabeçalho clicável do card de pontuação
 * 
 * Responsabilidade única: Exibir posição, nome e total do jogador
 */

'use client';

interface CabecalhoPontuacaoProps {
  posicao: number;
  nome: string;
  pontuacaoTotal: number;
  ehVencedor: boolean;
  expandido: boolean;
  coresText: string;
  onClick: () => void;
}

export function CabecalhoPontuacao({
  posicao,
  nome,
  pontuacaoTotal,
  ehVencedor,
  expandido,
  coresText,
  onClick
}: CabecalhoPontuacaoProps) {
  return (
    <div
      className="p-4 cursor-pointer hover:bg-opacity-80 transition-colors"
      onClick={onClick}
    >
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <span className="text-3xl font-bold text-gray-700">
            {posicao}°
          </span>
          
          {ehVencedor && <span className="text-3xl">👑</span>}
          
          <div>
            <h3 className={`text-xl font-bold ${ehVencedor ? 'text-yellow-900' : coresText}`}>
              {nome}
            </h3>
            <p className="text-sm text-gray-600">
              Clique para ver detalhes
            </p>
          </div>
        </div>
        
        <div className="flex items-center gap-3">
          <div className="text-right">
            <div className={`text-3xl font-bold ${ehVencedor ? 'text-yellow-800' : 'text-gray-800'}`}>
              {pontuacaoTotal}
            </div>
            <div className="text-sm text-gray-600">pontos</div>
          </div>
          
          <span className={`text-2xl transition-transform ${expandido ? 'rotate-180' : ''}`}>
            ▼
          </span>
        </div>
      </div>
    </div>
  );
}
