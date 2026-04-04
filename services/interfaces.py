from abc import ABC, abstractmethod


class ParseInterface(ABC):
    @abstractmethod
    def run(self, in_file) -> bytes:
        pass

class UploadInterface(ABC):
    @abstractmethod
    def run(self, file_path: str) -> int: # code
        pass
    
class DownloadInterface(ABC):
    @abstractmethod
    def run(self, filename: str, save_path: str = "") -> bytes: # the file as bytes
        pass
    
class LLMChatInterface(ABC):
    @abstractmethod
    def run(self, user, system, parameters) -> dict: # the whole response for json validation & retry dowstream.
        pass
    
class LLMGenerateInterface(ABC):
    @abstractmethod
    def run(self, prompt, parameters):
        pass