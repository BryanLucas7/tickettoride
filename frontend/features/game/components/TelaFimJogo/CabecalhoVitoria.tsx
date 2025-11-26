/**
 * CabecalhoVitoria - Header da tela de fim de jogo
 * 
 * Responsabilidade única: Exibir informações do vencedor/empate
 */

'use client';

interface CabecalhoVitoriaProps {
  vencedorNome: string;
  vencedorPontuacao: number;
  empate: boolean;
}

export function CabecalhoVitoria({ 
  vencedorNome, 
  vencedorPontuacao, 
  empate 
}: CabecalhoVitoriaProps) {
  return (
    <div className="bg-gradient-to-r from-yellow-400 to-amber-500 p-6 text-center border-b-4 border-yellow-600">
      <h1 className="text-5xl font-bold text-white mb-2 drop-shadow-lg">
        🏆 FIM DE JOGO 🏆
      </h1>
      
      {empate ? (
        <p className="text-2xl font-bold text-yellow-900">
          🤝 EMPATE! 🤝
        </p>
      ) : (
        <p className="text-2xl font-bold text-yellow-900">
          🎉 Vencedor: {vencedorNome} 🎉
        </p>
      )}
      
      <p className="text-lg text-yellow-800 mt-1">
        {vencedorPontuacao} pontos
      </p>
    </div>
  );
}
