from EP4UServices.clients.http_client import HTTPClient
from EP4UServices.services.interfaces import LLMChatInterface

class LLMChatService(HTTPClient, LLMChatInterface):
    def __init__(self, url, endpoint = "/", model="ministral-3"):
        super().__init__(url, endpoint)
        self.model = model
        
    def run(self, user, system, parameters):
        
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user}
            ],
            'stream': False,
            **parameters,
        }
        
        resp = self.post(payload)
        return resp.content.decode()
