from abc import ABC, abstractmethod
from typing import Generic

from annotated_types import T

class HTTPClientBase(ABC, Generic[T]):
    @abstractmethod
    def get(self, *args, **kwargs) -> T:
        pass
    
    @abstractmethod
    def post(self, *args, **kwargs) -> T:
            pass    
        
    @abstractmethod
    def run(self, *args, **kwargs):
        pass

class SSHInterface(ABC):
    @abstractmethod
    def start(self):
        pass
    
    @abstractmethod
    def close(self):
        pass
    
    @abstractmethod
    def port_forward(self, local_port, remote_port):
        pass