export default function Page() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-16">
        <div className="max-w-4xl mx-auto text-center">
          <h1 className="text-6xl font-bold text-gray-900 mb-6">Ticket to Ride</h1>
          <p className="text-xl text-gray-600 mb-12">Aventure-se em uma jornada épica de trens pelo Brasil</p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <a
              href="/setup"
              className="bg-blue-600 hover:bg-blue-700 text-white font-semibold text-lg px-8 py-3 rounded-lg transition-colors"
            >
              Iniciar Novo Jogo
            </a>
            <a
              href="/entrar"
              className="bg-white text-blue-700 border border-blue-200 hover:border-blue-400 font-semibold text-lg px-8 py-3 rounded-lg transition-colors shadow-sm"
            >
              Entrar na partida
            </a>
          </div>
        </div>
      </div>
    </div>
  )
}
