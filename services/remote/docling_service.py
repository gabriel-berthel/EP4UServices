from EP4UServices.clients.http_client import HTTPClient
from EP4UServices.services.interfaces import ParseInterface

class DoclingService(HTTPClient, ParseInterface):
    def __init__(self, url, endpoint = "/"):
        super().__init__(url, endpoint)
        
    def run(self, file_path):
        resp = self.post(file=file_path)
        
        return resp
