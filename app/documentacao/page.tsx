export default function DocumentacaoPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-12">
      <div className="container mx-auto px-4 max-w-4xl">
        <div className="bg-white rounded-lg shadow-xl p-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-6">Documentação do Projeto</h1>

          <section className="mb-8">
            <h2 className="text-2xl font-bold text-gray-800 mb-4">Estrutura do Backend</h2>
            <p className="text-gray-600 mb-4">
              O backend foi desenvolvido em Python seguindo fielmente o diagrama de classes fornecido. Todas as 14
              classes foram implementadas com seus respectivos atributos e métodos.
            </p>

            <h3 className="text-xl font-semibold text-gray-800 mb-2">Classes Principais:</h3>
            <ul className="list-disc list-inside space-y-2 text-gray-600 mb-4">
              <li>
                <strong>Jogo:</strong> Gerencia o estado geral do jogo
              </li>
              <li>
                <strong>Jogador:</strong> Representa cada jogador com suas cartas e pontuação
              </li>
              <li>
                <strong>Tabuleiro:</strong> Contém cidades e rotas do jogo
              </li>
              <li>
                <strong>Placar:</strong> Calcula e gerencia pontuações
              </li>
            </ul>

            <h3 className="text-xl font-semibold text-gray-800 mb-2">Gerenciadores:</h3>
            <ul className="list-disc list-inside space-y-2 text-gray-600 mb-4">
              <li>
                <strong>GerenciadorDeTurnos:</strong> Controla a ordem dos jogadores
              </li>
              <li>
                <strong>GerenciadorDeBaralho:</strong> Gerencia baralhos de cartas e bilhetes
              </li>
            </ul>
          </section>

          <section className="mb-8">
            <h2 className="text-2xl font-bold text-gray-800 mb-4">Como Jogar</h2>
            <ol className="list-decimal list-inside space-y-2 text-gray-600">
              <li>Configure o jogo adicionando de 2 a 5 jogadores</li>
              <li>Cada jogador começa com 45 vagões e 4 cartas</li>
              <li>
                No seu turno, você pode:
                <ul className="list-disc list-inside ml-6 mt-2">
                  <li>Comprar 2 cartas de vagão</li>
                  <li>Reivindicar uma rota usando cartas e vagões</li>
                </ul>
              </li>
              <li>Ganhe pontos ao reivindicar rotas</li>
              <li>O jogo termina quando um jogador tem 2 ou menos vagões</li>
            </ol>
          </section>

          <section className="mb-8">
            <h2 className="text-2xl font-bold text-gray-800 mb-4">Arquivos Importantes</h2>
            <ul className="list-disc list-inside space-y-2 text-gray-600">
              <li>
                <strong>backend/app/models/:</strong> Todas as classes do modelo
              </li>
              <li>
                <strong>backend/app/main.py:</strong> Exemplo de uso do sistema
                <strong>backend/README.md:</strong> Documentação detalhada do backend
              </li>
            </ul>
          </section>

          <a
            href="/"
            className="inline-block bg-blue-600 hover:bg-blue-700 text-white font-semibold px-6 py-3 rounded-lg transition-colors"
          >
            Voltar para Início
          </a>
        </div>
      </div>
    </div>
  )
}
