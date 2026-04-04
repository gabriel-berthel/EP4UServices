from clients.http_client import HTTPClient
from interfaces import ParseInterface

class DoclingService(HTTPClient, ParseInterface):
    def __init__(self, url, endpoint = "/"):
        super().__init__(url, endpoint)
        
    def run(self, file):
        resp = self.put(file)
        return resp
