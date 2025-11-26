/**
 * useMapaLoader - Hook para carregar dados do mapa
 * 
 * GRASP - Information Expert: Encapsula lógica de carregamento do mapa
 */

'use client';

import { useState, useEffect } from 'react';
import { anexarCoordenadasMapa, type MapaApiResponse, type MapaComCoordenadas } from '@/app/data/mapaBrasil';
import { gameApi } from '@/lib/services/gameApi';

interface UseMapaLoaderReturn {
  mapa: MapaComCoordenadas | null;
  carregandoMapa: boolean;
  erroMapa: string | null;
}

export function useMapaLoader(): UseMapaLoaderReturn {
  const [mapa, setMapa] = useState<MapaComCoordenadas | null>(null);
  const [carregandoMapa, setCarregandoMapa] = useState(true);
  const [erroMapa, setErroMapa] = useState<string | null>(null);

  useEffect(() => {
    const carregarMapa = async () => {
      setCarregandoMapa(true);
      setErroMapa(null);
      
      try {
        const mapaApi = await gameApi.getMapConfig() as unknown as MapaApiResponse;
        setMapa(anexarCoordenadasMapa(mapaApi));
      } catch (error) {
        console.error("Erro ao carregar mapa:", error);
        setMapa(null);
        setErroMapa("Não foi possível carregar o mapa.");
      } finally {
        setCarregandoMapa(false);
      }
    };
    
    carregarMapa();
  }, []);

  return {
    mapa,
    carregandoMapa,
    erroMapa
  };
}
