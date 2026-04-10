from abc import ABC, abstractmethod
from PIL.Image import Image as PILImage
from typing import List

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
    
# CORE SERVICES INTERFACES

class ParseInterface(ABC):
    @abstractmethod
    def run(self, in_file) -> bytes:
        pass
    
class LLMChatInterface(ABC):
    @abstractmethod
    def run(self, user, system, parameters) -> dict: # the whole response for json validation & retry dowstream.
        pass
    
class LLMGenerateInterface(ABC):
    @abstractmethod
    def run(self, prompt, parameters):
        pass
    
class OCRInterface(ABC):
    @abstractmethod
    def run(self, images: List[PILImage]) -> List[str]:
        pass