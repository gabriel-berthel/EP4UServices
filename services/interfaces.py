from abc import ABC, abstractmethod
from PIL.Image import Image as PILImage
from typing import Generic, List

from annotated_types import T

# MISC.

class PromptBuilderBase(ABC):
    @abstractmethod
    def build_system(self, **kwargs) -> str:
        pass
    
    @abstractmethod
    def build_user(self, **kwargs) -> str:
        pass

    @property
    @abstractmethod
    def parameters(self) -> dict:
        pass
    
    @abstractmethod
    def extract(self, response: str) -> str:
        pass
    
# CORE SERVICES INTERFACES

class CoreService(ABC):
    pass

class ParseInterface(CoreService):
    @abstractmethod
    def run(self, in_file) -> bytes:
        pass
    
class LLMChatInterface(CoreService):
    @abstractmethod
    def run(self, user, system, parameters) -> dict: # the whole response for json validation & retry dowstream.
        pass
    
class LLMGenerateInterface(CoreService):
    @abstractmethod
    def run(self, prompt, parameters):
        pass
    
class OCRInterface(CoreService):
    @abstractmethod
    def run(self, images: List[PILImage]) -> List[str]:
        pass
    
# FEATURED

class FeaturedService(ABC):
    pass    

class NarrationServiceBase(FeaturedService, Generic[T]):
    @abstractmethod
    def run(self, t: T) -> str:
        pass