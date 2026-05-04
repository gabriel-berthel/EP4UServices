    
# FEATURED

from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from EP4UServices.services.core import AsyncTTSEngineInterface, LLMChatInterface, ParseInterface, TTSEngineInterface

T = TypeVar("T")
class LLMMathsSpeechBase(Generic[T]):
    def __init__(self, service: LLMChatInterface):
        super().__init__()
        self.service = service
    
    @abstractmethod
    def run(self, t: T) -> str:
        pass
    
class ParseServiceBase(ABC):
    def __init__(self, service: ParseInterface):
        super().__init__()
        self.service = service
    
    @abstractmethod
    def parse(self, file_path):
        pass
    
class TTSServiceBase(ABC):
    def __init__(self, service: TTSEngineInterface):
        super().__init__()
        self.service = service
    
    @abstractmethod
    def generate(self, script: str) -> bytes:
        pass
    
    @abstractmethod
    def save(self, script: str, file_path) -> None:
        pass
    
class AsyncTTSServiceBase(ABC):
    def __init__(self, service: AsyncTTSEngineInterface):
        super().__init__()
        self.service = service
    
    @abstractmethod
    async def generate(self, script: str) -> bytes:
        pass
    
    @abstractmethod
    async def save(self, script: str, file_path) -> None:
        pass