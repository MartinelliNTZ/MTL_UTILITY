import json
from pathlib import Path
from typing import Any, Dict
from utils.ToolKey import ToolKey
from utils.LogUtils import logger


import os

class Preferences:
    """Gerencia preferências da aplicação salvas em JSON."""
    TOOL_KEY = ToolKey.PREFERENCES
    """Gerencia preferências da aplicação salvas em JSON."""

    # Novo diretório fixo para preferências no AppData do usuário
    APPDATA_PREF_DIR = Path(os.getenv('LOCALAPPDATA', str(Path.home() / 'AppData' / 'Local'))) / 'MTL_UTIL' / 'preferences'

    def __init__(self, config_file: str = None):
        """
        Inicializa o gerenciador de preferências.

        Args:
            config_file: Nome do arquivo de configuração JSON (opcional)
        """
        if config_file is None:
            self.APPDATA_PREF_DIR.mkdir(parents=True, exist_ok=True)
            config_file = str(self.APPDATA_PREF_DIR / 'preferences.json')
        self.config_file = Path(config_file)
        self._data: Dict[str, Any] = {}
        self._load()
    
    def _load(self) -> None:
        """Carrega as preferências do arquivo JSON."""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self._data = json.load(f)
            else:
                self._data = self._get_defaults()
                self._save()
        except (json.JSONDecodeError, IOError) as e:
            print(f"Erro ao carregar preferências: {e}")
            self._data = self._get_defaults()
    
    def _save(self) -> None:
        """Salva as preferências no arquivo JSON."""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self._data, f, indent=2, ensure_ascii=False)
        except IOError as e:
            print(f"Erro ao salvar preferências: {e}")
    
    @staticmethod
    def _get_defaults() -> Dict[str, Any]:
        """Retorna as preferências padrão."""
        return {
            "base_path": "C:/",
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Obtém um valor de preferência.
        
        Args:
            key: Chave da preferência
            default: Valor padrão se a chave não existir
            
        Returns:
            Valor da preferência ou default
        """
        return self._data.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """
        Define um valor de preferência e salva.
        
        Args:
            key: Chave da preferência
            value: Novo valor
        """
        self._data[key] = value
        self._save()
    
    def get_base_path(self) -> str:
        """Retorna o caminho base."""
        return self.get("base_path", "C:/")
    
    def set_base_path(self, path: str) -> None:
        """Define o caminho base."""
        self.set("base_path", path)
    
    def reset(self) -> None:
        """Reseta as preferências para os valores padrão."""
        self._data = self._get_defaults()
        self._save()
