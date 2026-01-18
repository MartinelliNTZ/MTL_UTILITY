from PySide6.QtCore import QObject, Signal
from typing import Callable, Dict, List
from utils.ToolKey import ToolKey
from utils.LogUtils import logger


class SignalManager(QObject):
    """Gerencia sinais/eventos para comunicação entre main window e plugins."""
    TOOL_KEY = ToolKey.SIGNAL_MANAGER
    """Gerencia sinais/eventos para comunicação entre main window e plugins."""
    
    # Sinais
    base_path_changed = Signal(str)  # Emitido quando o caminho base muda
    
    _instance = None
    
    def __new__(cls):
        """Implementa padrão singleton."""
        if cls._instance is None:
            cls._instance = super(SignalManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Inicializa o gerenciador de sinais (apenas uma vez)."""
        if self._initialized:
            return
        
        super().__init__()
        self._callbacks: Dict[str, List[Callable]] = {}
        self._initialized = True
    
    def subscribe(self, signal_name: str, callback: Callable) -> None:
        """
        Inscreve uma callback a um sinal customizado.
        
        Args:
            signal_name: Nome do sinal
            callback: Função a ser chamada quando o sinal for emitido
        """
        if signal_name not in self._callbacks:
            self._callbacks[signal_name] = []
        self._callbacks[signal_name].append(callback)
    
    def unsubscribe(self, signal_name: str, callback: Callable) -> None:
        """
        Desinscreve uma callback de um sinal.
        
        Args:
            signal_name: Nome do sinal
            callback: Função a remover
        """
        if signal_name in self._callbacks:
            if callback in self._callbacks[signal_name]:
                self._callbacks[signal_name].remove(callback)
    
    def emit(self, signal_name: str, *args, **kwargs) -> None:
        """
        Emite um sinal customizado chamando todas as callbacks inscritas.
        
        Args:
            signal_name: Nome do sinal
            *args: Argumentos posicionais para a callback
            **kwargs: Argumentos nomeados para a callback
        """
        if signal_name in self._callbacks:
            for callback in self._callbacks[signal_name]:
                try:
                    callback(*args, **kwargs)
                except Exception as e:
                    print(f"Erro ao executar callback para '{signal_name}': {e}")
    
    def emit_base_path_changed(self, new_path: str) -> None:
        """Emite o sinal de mudança de caminho base."""
        self.base_path_changed.emit(new_path)
        self.emit("base_path_changed", new_path)
