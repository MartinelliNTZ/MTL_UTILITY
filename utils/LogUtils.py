"""
LogUtils - Sistema de logging para a aplicação MTL_UTIL.

Gerencia logs estruturados com rotação automática de arquivos.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any
from enum import Enum


class LogLevel(Enum):
    """Níveis de log disponíveis."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class TimeUtils:
    """Utilitários para manipulação de tempo e datas."""

    @staticmethod
    def get_current_timestamp() -> str:
        """Retorna timestamp atual no formato YYYY-MM-DD HH:MM:SS."""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def get_current_date() -> str:
        """Retorna data atual no formato YYYY-MM-DD."""
        return datetime.now().strftime("%Y-%m-%d")


import os

class LogUtils:
    """Sistema de logging com rotação automática de arquivos."""

    # Novo diretório de logs fixo no AppData do usuário
    APPDATA_LOG_DIR = Path(os.getenv('LOCALAPPDATA', str(Path.home() / 'AppData' / 'Local'))) / 'MTL_UTIL' / 'logs'
    MAX_LOG_FILES = 2  # Manter apenas 2 arquivos de log

    def __init__(self):
        self.LOG_DIR = self.APPDATA_LOG_DIR
        self.LOG_DIR.mkdir(parents=True, exist_ok=True)
        self._current_log_file = None
        self._rotate_logs()
        self._create_new_log_file()

    def _rotate_logs(self):
        """Remove logs antigos, mantendo apenas os mais recentes."""
        log_files = sorted(self.LOG_DIR.glob("mtl_util_*.log"), key=os.path.getmtime, reverse=True)

        # Manter apenas os 2 mais recentes
        for old_file in log_files[self.MAX_LOG_FILES:]:
            old_file.unlink()

    def _create_new_log_file(self):
        """Cria um novo arquivo de log com timestamp."""
        timestamp = TimeUtils.get_current_date().replace("-", "")
        time_part = datetime.now().strftime("%H%M%S")
        filename = f"mtl_util_{timestamp}_{time_part}.log"
        self._current_log_file = self.LOG_DIR / filename

        # Log inicial
        self.log(LogLevel.INFO, "system", "LogUtils", "Sistema de logging iniciado")

    def log(self, level: LogLevel, tool_key: str, class_name: str, message: str, extra_data: Dict[str, Any] = None):
        """
        Registra um log no arquivo atual.

        Args:
            level: Nível do log (DEBUG, INFO, etc.)
            tool_key: Identificador da ferramenta (ToolKey.xxx)
            class_name: Nome da classe que gerou o log
            message: Mensagem do log
            extra_data: Dados extras opcionais
        """
        if self._current_log_file is None:
            return

        log_entry = {
            "timestamp": TimeUtils.get_current_timestamp(),
            "level": level.value,
            "tool_key": tool_key,
            "class_name": class_name,
            "message": message,
            "extra_data": extra_data or {}
        }

        try:
            with open(self._current_log_file, 'a', encoding='utf-8') as f:
                json.dump(log_entry, f, ensure_ascii=False)
                f.write('\n')
        except Exception as e:
            print(f"Erro ao escrever log: {e}")

    # Métodos convenientes para diferentes níveis
    def debug(self, tool_key: str, class_name: str, message: str, extra_data=None):
        self.log(LogLevel.DEBUG, tool_key, class_name, message, extra_data)

    def info(self, tool_key: str, class_name: str, message: str, extra_data=None):
        self.log(LogLevel.INFO, tool_key, class_name, message, extra_data)

    def warning(self, tool_key: str, class_name: str, message: str, extra_data=None):
        self.log(LogLevel.WARNING, tool_key, class_name, message, extra_data)

    def error(self, tool_key: str, class_name: str, message: str, extra_data=None):
        self.log(LogLevel.ERROR, tool_key, class_name, message, extra_data)

    def critical(self, tool_key: str, class_name: str, message: str, extra_data=None):
        self.log(LogLevel.CRITICAL, tool_key, class_name, message, extra_data)


# Instância global do logger
logger = LogUtils()