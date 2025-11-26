"""
BackupManager - Gerenciador de backup para arquivos de cache.

Padrão GRASP: Pure Fabrication
- Extraído de PickleJogoRepository para responsabilidade única
- Repository: operações CRUD
- BackupManager: gerenciamento de backup e recuperação

Responsabilidades:
- Criar backup de arquivos antes de modificações
- Restaurar backup em caso de falha
- Escrita atômica usando arquivo temporário
"""

import os
import shutil
import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


class BackupManager:
    """
    Gerenciador de backup para arquivos.
    
    Fornece operações atômicas de escrita com backup automático
    para garantir integridade dos dados.
    """
    
    def __init__(self, base_file: Path):
        """
        Inicializa o gerenciador de backup.
        
        Args:
            base_file: Caminho do arquivo principal a ser gerenciado
        """
        self.base_file = base_file
        self.backup_path = base_file.with_suffix(base_file.suffix + ".bak")
        self.temp_path = base_file.with_suffix(base_file.suffix + ".tmp")
    
    def criar_backup(self) -> bool:
        """
        Cria backup do arquivo principal.
        
        Returns:
            True se backup foi criado, False se arquivo não existe
        """
        if not self.base_file.exists():
            return False
        
        try:
            shutil.copy2(self.base_file, self.backup_path)
            logger.debug(f"Backup criado: {self.backup_path}")
            return True
        except Exception as exc:
            logger.warning(f"Não foi possível criar backup: {exc}")
            return False
    
    def restaurar_backup(self) -> bool:
        """
        Restaura arquivo principal a partir do backup.
        
        Returns:
            True se restauração foi bem-sucedida, False caso contrário
        """
        if not self.backup_path.exists():
            logger.warning("Backup não encontrado para restauração")
            return False
        
        try:
            shutil.copy2(self.backup_path, self.base_file)
            logger.info(f"Arquivo restaurado do backup: {self.base_file}")
            return True
        except Exception as exc:
            logger.error(f"Falha ao restaurar backup: {exc}")
            return False
    
    def escrever_atomico(self, write_func) -> None:
        """
        Escreve arquivo de forma atômica com backup.
        
        Processo:
        1. Cria backup do arquivo atual (se existir)
        2. Escreve em arquivo temporário
        3. Sincroniza para disco (fsync)
        4. Substitui arquivo principal pelo temporário (atômico)
        5. Limpa arquivo temporário se sobrar
        
        Args:
            write_func: Função que recebe file handle e escreve dados
                       Signature: write_func(file_handle) -> None
                       
        Raises:
            Exception: Se houver erro na escrita
        """
        # Garantir que diretório existe
        self.base_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Criar backup antes de modificar
        self.criar_backup()
        
        try:
            # Escrita em arquivo temporário
            with self.temp_path.open("wb") as f:
                write_func(f)
                f.flush()
                os.fsync(f.fileno())
            
            # Substituição atômica
            self.temp_path.replace(self.base_file)
            logger.debug(f"Arquivo atualizado: {self.base_file}")
            
        except Exception as exc:
            logger.error(f"Falha na escrita atômica: {exc}")
            raise
        finally:
            # Limpar temporário se sobrar
            self._limpar_temporario()
    
    def carregar_com_fallback(self, load_func) -> Optional[any]:
        """
        Carrega arquivo com fallback para backup.
        
        Tenta carregar do arquivo principal. Se falhar,
        tenta carregar do backup.
        
        Args:
            load_func: Função que recebe Path e retorna dados carregados
                       Signature: load_func(path: Path) -> any
                       
        Returns:
            Dados carregados ou None se ambos falharem
        """
        # Tenta arquivo principal
        resultado = self._tentar_carregar(self.base_file, load_func, "principal")
        if resultado is not None:
            return resultado
        
        # Tenta backup
        resultado = self._tentar_carregar(self.backup_path, load_func, "backup")
        return resultado
    
    def _tentar_carregar(self, path: Path, load_func, descricao: str) -> Optional[any]:
        """Tenta carregar de um arquivo específico."""
        if not path.exists():
            return None
        
        try:
            resultado = load_func(path)
            logger.info(f"Carregado do arquivo {descricao}: {path}")
            return resultado
        except Exception as exc:
            logger.warning(f"Falha ao carregar {descricao}: {exc}")
            return None
    
    def _limpar_temporario(self) -> None:
        """Remove arquivo temporário se existir."""
        if self.temp_path.exists():
            try:
                self.temp_path.unlink()
            except Exception:
                pass
    
    def limpar_backups(self) -> None:
        """Remove todos os arquivos de backup e temporários."""
        for path in [self.backup_path, self.temp_path]:
            if path.exists():
                try:
                    path.unlink()
                    logger.debug(f"Removido: {path}")
                except Exception as exc:
                    logger.warning(f"Não foi possível remover {path}: {exc}")
