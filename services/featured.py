    
# FEATURED

from abc import abstractmethod
from typing import Generic, TypeVar

from EP4UServices.services.core import LLMChatInterface

T = TypeVar("T")
class NarrationServiceBase(Generic[T]):
    
    def __init__(self, service: LLMChatInterface):
        super().__init__()
        self.service = service
    
    @abstractmethod
    def run(self, t: T) -> str:
        pass