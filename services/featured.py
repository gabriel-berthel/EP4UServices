    
# FEATURED

from abc import ABC, abstractmethod
from typing import Generic

from annotated_types import T

from EP4UServices.services.remote.interfaces import RemoteService

class FeaturedService(ABC):
    def __init__(self, remote_service: RemoteService):
        self.core_service = remote_service
    
class NarrationServiceBase(FeaturedService, Generic[T]):
    @abstractmethod
    def run(self, t: T) -> str:
        pass

class TTSServiceBase(ABC):
    @abstractmethod
    def generate(self, text: str) -> bytes:
        pass
    