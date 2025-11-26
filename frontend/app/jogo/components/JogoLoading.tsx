/**
 * JogoLoading - Tela de carregamento do jogo
 * 
 * Responsabilidade única: Exibir spinner enquanto carrega dados do jogo
 */

'use client';

export function JogoLoading() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="text-center">
        <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-blue-600 mx-auto mb-4"></div>
        <p className="text-xl text-gray-700">Carregando jogo...</p>
      </div>
    </div>
  );
}
