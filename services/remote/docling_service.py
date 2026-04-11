

from EP4UServices.services.remote.interfaces import RemoteParseService


class DoclingService(RemoteParseService):
    def __init__(self, url, endpoint = "/"):
        super().__init__(url, endpoint)
        
    def run(self, file_path):
        resp = self.post(file=file_path)
        
        return resp
