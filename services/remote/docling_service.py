from EP4UServices.clients.http_client import HTTPClient
from EP4UServices.services.interfaces import ParseInterface

class DoclingService(HTTPClient, ParseInterface):
    def __init__(self, url, endpoint = "/"):
        super().__init__(url, endpoint)
        
    def run(self, payload):
        resp = self.post(file=payload['file'])
        return resp
