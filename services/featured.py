    
# FEATURED

from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from EP4UServices.services.core import LLMChatInterface, ParseInterface

T = TypeVar("T")
class NarrationServiceBase(Generic[T]):
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
    

    def parse(self, file_path):
        pass