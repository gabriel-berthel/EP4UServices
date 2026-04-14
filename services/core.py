from abc import ABC, abstractmethod
from PIL.Image import Image as PILImage
from typing import Generic, List

from annotated_types import T

# CORE SERVICES INTERFACES
    
class CoreInterface(ABC):
    pass

class ParseInterface(CoreInterface):
    @abstractmethod
    def parse(self, in_file) -> bytes:
        pass
    
class LLMChatInterface(CoreInterface):
    @abstractmethod
    def chat(self, user, system, parameters) -> dict: # the whole response for json validation & retry dowstream.
        pass
    
class OCRInterface(CoreInterface):
    @abstractmethod
    def ocr(self, images: List[PILImage]) -> List[str]:
        pass

class TTSEngineInterface(ABC):
    @abstractmethod
    def synthesize(self, speech:str):
        """Return raw MP3 bytes. It's reponsible for normalizing to MP3."""
        pass
    
class AsyncTTSEngineInterface(ABC):
    @abstractmethod
    async def synthesize(self, speech:str):
        """Return raw MP3 bytes. It's reponsible for normalizing to MP3."""
        pass