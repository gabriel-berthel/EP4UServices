from abc import ABC, abstractmethod
from PIL.Image import Image as PILImage
from typing import Generic, List

from annotated_types import T

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
    
class OCRInterface(CoreService):
    @abstractmethod
    def run(self, images: List[PILImage]) -> List[str]:
        pass
    
class TTSEngineBase(CoreService):
    @abstractmethod
    def synthesize(self, text: str) -> bytes:
        """Return raw audio bytes (e.g. PCM or encoded)."""
        pass


