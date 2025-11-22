/**
 * Dados do mapa Ticket to Ride - Brasil
 * Posições das cidades no canvas (x, y em pixels)
 */

export const CORES = {
  VERMELHO: '#DC2626',
  AZUL: '#2563EB',
  VERDE: '#16A34A',
  AMARELO: '#FBBF24',
  PRETO: '#1F2937',
  LARANJA: '#EA580C',
  ROXO: '#8B5CF6',
  BRANCO: '#ffffffff',
  CINZA: '#b7b7b7ff',

};

export interface Cidade {
  id: string;
  nome: string;
  x: number;
  y: number;
}

export interface Rota {
  id: string;
  cidadeA: string;
  cidadeB: string;
  cor: keyof typeof CORES;
  comprimento: number;
}

export const CIDADES: Cidade[] = [
  { id: 'PORTO_ALEGRE', nome: 'Porto Alegre', x: 430, y: 580 },
  //{ id: 'CURITIBA', nome: 'Curitiba', x: 420, y: 550 },
  { id: 'BAURU', nome: 'Bauru', x: 465, y: 455 },
  { id: 'RIO_DE_JANEIRO', nome: 'Rio de Janeiro', x: 565, y: 465 },
  //{ id: 'BELO_HORIZONTE', nome: 'Belo Horizonte', x: 530, y: 410 },
  //{ id: 'VITORIA', nome: 'Vitória', x: 570, y: 450 },
  { id: 'BRASILIA', nome: 'Brasília', x: 480, y: 370 },
  //{ id: 'GOIANIA', nome: 'Goiânia', x: 330, y: 410 },
  { id: 'CAMPO_GRANDE', nome: 'Campo Grande', x: 385, y: 435 },
  { id: 'CUIABA', nome: 'Cuiabá', x: 350, y: 340 },
  { id: 'SALVADOR', nome: 'Salvador', x: 605, y: 320 },
  { id: 'RECIFE', nome: 'Recife', x: 670, y: 240 },
  { id: 'FORTALEZA', nome: 'Fortaleza', x: 620, y: 190 },
  { id: 'BELEM', nome: 'Belém', x: 480, y: 140 },
  { id: 'MANAUS', nome: 'Manaus', x: 300, y: 160 },
  { id: 'RIO_BRANCO', nome: 'Rio Branco', x: 190, y: 280 },
  { id: 'PALMAS', nome: 'Palmas', x: 470, y: 280 },
];

export const ROTAS: Rota[] = [
  // Sul
  { id: 'R01', cidadeA: 'PORTO_ALEGRE', cidadeB: 'BAURU', cor: 'VERDE', comprimento: 4 },
  { id: 'R02', cidadeA: 'PORTO_ALEGRE', cidadeB: 'CAMPO_GRANDE', cor: 'AMARELO', comprimento: 4 },
  
  // Sudeste
  { id: 'R03', cidadeA: 'BAURU', cidadeB: 'BRASILIA', cor: 'VERMELHO', comprimento: 3 },
  { id: 'R04', cidadeA: 'BAURU', cidadeB: 'RIO_DE_JANEIRO', cor: 'AZUL', comprimento: 3 },
  { id: 'R05', cidadeA: 'BAURU', cidadeB: 'CAMPO_GRANDE', cor: 'PRETO', comprimento: 2 },
  { id: 'R06', cidadeA: 'RIO_DE_JANEIRO', cidadeB: 'SALVADOR', cor: 'AMARELO', comprimento: 4 },
  { id: 'R07', cidadeA: 'RIO_DE_JANEIRO', cidadeB: 'BRASILIA', cor: 'ROXO', comprimento: 3 },
  
  // Centro-Oeste

  { id: 'R08', cidadeA: 'CAMPO_GRANDE', cidadeB: 'CUIABA', cor: 'LARANJA', comprimento: 3 },
  { id: 'R09', cidadeA: 'CAMPO_GRANDE', cidadeB: 'BRASILIA', cor: 'BRANCO', comprimento: 3 },
  { id: 'R09B', cidadeA: 'CUIABA', cidadeB: 'BRASILIA', cor: 'PRETO', comprimento: 4 },
  { id: 'R10', cidadeA: 'PALMAS', cidadeB: 'BRASILIA', cor: 'VERDE', comprimento: 3 },
  { id: 'R11', cidadeA: 'PALMAS', cidadeB: 'CUIABA', cor: 'AMARELO', comprimento: 5 },
  { id: 'R12', cidadeA: 'PALMAS', cidadeB: 'MANAUS', cor: 'ROXO', comprimento: 6 },
  { id: 'R13', cidadeA: 'PALMAS', cidadeB: 'BELEM', cor: 'VERMELHO', comprimento: 5 },
  { id: 'R14', cidadeA: 'PALMAS', cidadeB: 'FORTALEZA', cor: 'PRETO', comprimento: 5 },
  { id: 'R15', cidadeA: 'PALMAS', cidadeB: 'RECIFE', cor: 'AZUL', comprimento: 5 },
  { id: 'R16', cidadeA: 'PALMAS', cidadeB: 'SALVADOR', cor: 'LARANJA', comprimento: 4 },
  
  // Nordeste
  { id: 'R17', cidadeA: 'BRASILIA', cidadeB: 'SALVADOR', cor: 'VERDE', comprimento: 4 },
  { id: 'R18', cidadeA: 'SALVADOR', cidadeB: 'RECIFE', cor: 'BRANCO', comprimento: 4 },
  { id: 'R19', cidadeA: 'RECIFE', cidadeB: 'FORTALEZA', cor: 'BRANCO', comprimento: 2 },
  
  // Norte
  { id: 'R20', cidadeA: 'FORTALEZA', cidadeB: 'BELEM', cor: 'CINZA', comprimento: 5 },
  { id: 'R21', cidadeA: 'BELEM', cidadeB: 'MANAUS', cor: 'CINZA', comprimento: 6 },
  { id: 'R22', cidadeA: 'MANAUS', cidadeB: 'CUIABA', cor: 'CINZA', comprimento: 5 },
  { id: 'R23', cidadeA: 'RIO_BRANCO', cidadeB: 'MANAUS', cor: 'LARANJA', comprimento: 5 },
  { id: 'R24', cidadeA: 'RIO_BRANCO', cidadeB: 'CUIABA', cor: 'ROXO', comprimento: 5 },
  
  // Rotas duplas
  //{ id: 'R19', cidadeA: 'PORTO_ALEGRE', cidadeB: 'CURITIBA', cor: 'AZUL', comprimento: 3 },
  //{ id: 'R20', cidadeA: 'BAURU', cidadeB: 'RIO_DE_JANEIRO', cor: 'VERMELHO', comprimento: 2 },
];
