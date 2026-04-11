
from EP4UServices.clients.http_client import HTTPClient
from EP4UServices.services.core import LLMChatInterface, ParseInterface, TTSEngineInterface

class RemoteService(HTTPClient):
    def __init__(self, url, endpoint = "/"):
        super().__init__(url, endpoint)
        
class RemoteChatServiceBase(RemoteService, LLMChatInterface):
    def __init__(self, url, endpoint, model):
        super().__init__(url, endpoint)
        self.model = model
    
class RemoteParseServiceBase(RemoteService, ParseInterface):
    def __init__(self, url, endpoint):
        super().__init__(url, endpoint)
        
class RemoteTTSEngineBase(RemoteService, TTSEngineInterface):
    def __init__(self, url, endpoint):
        super().__init__(url, endpoint)