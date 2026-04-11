

from EP4UServices.services.http.interfaces import RemoteParseServiceBase


class RemoteParseService(RemoteParseServiceBase):
    def __init__(self, url, endpoint = "/"):
        super().__init__(url, endpoint)
        
    def parse(self, file_path):
        resp = self.post(file=file_path)
        
        return resp
